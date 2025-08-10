import os, json
import httpx
from pyspark.sql import DataFrame, functions as F, types as T

LLM_URL = os.getenv("LLM_SERVICE_URL", "http://localhost:8000/v1/reason")
LLM_TIMEOUT = float(os.getenv("LLM_TIMEOUT_S", "2.0"))

@F.udf(returnType=T.StringType())
def _enrich_json_udf(row_json: str) -> str:
    row = json.loads(row_json)
    if int(row.get("is_fraud", 0)) != 1:
        row.update({"llm_reason": None, "llm_actions": None, "llm_confidence": None})
        return json.dumps(row)
    payload = {
        "txn_json": {k: row.get(k) for k in ["txn_id","user_id","amount","merchant","geo","country","ts"] if k in row},
        "features": row.get("features", {}),
        "risk_score": float(row.get("risk_score", 0.0)),
        "customer_context": row.get("customer_context",""),
    }
    try:
        with httpx.Client(timeout=LLM_TIMEOUT) as c:
            r = c.post(LLM_URL, json=payload)
        r.raise_for_status()
        resp = r.json()
    except Exception as e:
        resp = {"reason": f"LLM error: {e}", "actions": [], "confidence": 0.0}
    row.update({
        "llm_reason": resp.get("reason"),
        "llm_actions": resp.get("actions"),
        "llm_confidence": float(resp.get("confidence", 0.6)),
    })
    return json.dumps(row)

def attach_llm(scored_df: DataFrame) -> DataFrame:
    """
    Input columns expected:
      txn_id,user_id,amount,merchant,geo,country,ts,features,risk_score,is_fraud[,customer_context]
    Output: same + llm_reason,llm_actions,llm_confidence
    """
    enriched_json = (
        scored_df
        .withColumn("row_json", F.to_json(F.struct("*")))
        .withColumn("enriched_json", _enrich_json_udf(F.col("row_json")))
        .select("enriched_json")
    )
    # Re-materialize to original schema + 3 new columns
    out_schema = T.StructType(scored_df.schema.fields + [
        T.StructField("llm_reason", T.StringType()),
        T.StructField("llm_actions", T.ArrayType(T.StringType())),
        T.StructField("llm_confidence", T.DoubleType()),
    ])
    return (enriched_json
            .select(F.from_json("enriched_json", out_schema).alias("r"))
            .select("r.*"))

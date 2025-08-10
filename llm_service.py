# llm/service.py
import os, json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class LLMClient:
    def __init__(self):
        self.backend = os.getenv("LLM_BACKEND", "mock").lower()
        self.model = os.getenv("LLM_MODEL", "")
        if self.backend == "openai":
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
            except Exception as e:
                raise RuntimeError(f"OpenAI init failed: {e}")
        elif self.backend == "bedrock":
            try:
                import boto3
                self.client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION","us-east-1"))
            except Exception as e:
                raise RuntimeError(f"Bedrock init failed: {e}")

    def generate(self, prompt: str) -> str:
        if self.backend == "mock":
            # Keep it predictable for demos/interviews
            return json.dumps({
                "reason": "Amount and velocity patterns indicate possible card-not-present fraud; geolocation deviates from customer norm.",
                "actions": ["Send SMS OTP", "Hold transaction for manual review"],
                "confidence": 0.82
            })
        elif self.backend == "openai":
            # Tiny call; safe to keep as reference (not required to run)
            resp = self.client.chat.completions.create(
                model=self.model or "gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=220
            )
            return resp.choices[0].message.content
        else:  # bedrock
            body = {
                "anthropic_version":"bedrock-2023-05-31",
                "max_tokens":220,
                "temperature":0.2,
                "messages":[{"role":"user","content":[{"type":"text","text":prompt}]}],
            }
            out = self.client.invoke_model(
                modelId=self.model or "anthropic.claude-3-sonnet-20240229-v1:0",
                body=json.dumps(body),
                contentType="application/json",
                accept="application/json",
            )
            import json as _json
            return _json.loads(out["body"].read())["content"][0]["text"]

class ReasonReq(BaseModel):
    txn_json: dict
    features: dict
    risk_score: float
    customer_context: str = ""

class ReasonResp(BaseModel):
    reason: str
    actions: list
    confidence: float

PROMPT = (
    "You are a risk analyst. Using the JSON and features, output JSON with keys "
    "`reason` (<=120 words), `actions` (2-3 bullets), `confidence` in [0,1].\n\n"
    "Transaction: {TXN}\nFeatures:\n{FEATS}\nRisk score: {SCORE}\nContext: {CTX}"
)

app = FastAPI(title="Fraud LLM (minimal)")
client = LLMClient()

@app.post("/v1/reason", response_model=ReasonResp)
def reason(req: ReasonReq):
    try:
        prompt = PROMPT.format(
            TXN=json.dumps(req.txn_json, ensure_ascii=False),
            FEATS="\n".join([f"{k}: {v}" for k, v in req.features.items()]),
            SCORE=round(req.risk_score, 3),
            CTX=req.customer_context or "N/A",
        )
        text = client.generate(prompt)
        try:
            data = json.loads(text)  # prefer JSON if backend returns it
        except Exception:
            data = {"reason": text.strip(), "actions": [], "confidence": 0.6}
        return ReasonResp(**data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

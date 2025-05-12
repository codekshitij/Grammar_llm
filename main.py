from fastapi import FastAPI
from pydantic import BaseModel
import httpx
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class TextRequest(BaseModel):
    text: str

@app.post("/proofread")
async def proofread(req: TextRequest):
    prompt = f"Proofread this for grammar, spelling, and clarity: \"{req.text}\""

    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": True
    }

    final_output = ""

    async with httpx.AsyncClient() as client:
        async with client.stream("POST", "http://localhost:11434/api/generate", json=payload) as response:
            async for line in response.aiter_lines():
                if line.strip():
                    try:
                        data = json.loads(line)
                        final_output += data.get("response", "")
                    except json.JSONDecodeError:
                        continue

    return {"suggestion": final_output.strip()}

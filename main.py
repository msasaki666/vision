from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# デコレータ(この@hogehogeのこと)
# このデコレーターは直下の関数がオペレーション getを使用したパス/に対応することをFastAPI に通知します。
@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}

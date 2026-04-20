from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi.responses import RedirectResponse
from google import genai


class Settings(BaseSettings):
    # 如果環境變數中沒有 GEMINI_API_KEY，會報錯提醒
    gemini_api_key: str
    gemini_model: str = "gemini-2.5-flash"

    model_config = SettingsConfigDict(env_file=".env")


# 初始化設定與 Gemini 用戶端
try:
    settings = Settings()
    client = genai.Client(api_key=settings.gemini_api_key)
except Exception as e:
    # 預防沒有設定 API Key 導致啟動失敗
    print(f"Configuration Error: {e}")
    settings = None


app = FastAPI(
    title="IT Helpdesk AI Agent (LLM Powered)",
    description="企業內部 IT 報修 AI 分類助理 - 實測 LLM 驅動版",
    version="0.2.0"
)


# 資料模型定義
class TicketRequest(BaseModel):
    description: str


class TicketResponse(BaseModel):
    category: str
    suggestion: str


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["System"])
def health_check():
    # 增加檢查 AI 用戶端是否就緒
    status = "ok" if settings else "api_key_missing"
    return {"status": status, "message": "Service is running."}


@app.post(
    "/api/v1/classify",
    response_model=TicketResponse,
    tags=["AI Agent"]
)
def classify_ticket(ticket: TicketRequest):
    if not settings:
        raise HTTPException(
            status_code=500,
            detail="Gemini API Key is not configured."
        )

    # 建立 AI 的指令 (Prompt)
    prompt = (
        "你是一個企業 IT 專業客服助手。\n"
        "請根據使用者的報修描述，將其歸類為以下類別之一：\n"
        "[Email 系統, 硬體設備, 帳號權限, 軟體安裝, 其他]。\n"
        "並給出一個簡短且具備專業感的初步排除建議。\n\n"
        f"使用者描述：{ticket.description}"
    )

    try:
        # 使用 Gemini 進行結構化生成
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
                'response_schema': TicketResponse,
            }
        )
        return response.parsed

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI Generation Error: {str(e)}"
        )

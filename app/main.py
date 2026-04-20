from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import RedirectResponse


app = FastAPI(
    title="IT Helpdesk AI Agent",
    description="企業內部 IT 報修 AI 分類助理微服務",
    version="0.1.0"
)


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
    return {"status": "ok", "message": "Service is running perfectly."}


@app.post("/api/v1/classify", response_model=TicketResponse, tags=["AI Agent"])
def classify_ticket(ticket: TicketRequest):
    text = ticket.description

    if "信箱" in text or "郵件" in text:
        return TicketResponse(
            category="Email 系統",
            suggestion="請確認您是否有修改過密碼，若有請重新登入 Outlook。"
        )
    elif "螢幕" in text or "黑屏" in text:
        return TicketResponse(
            category="硬體設備",
            suggestion="請先檢查螢幕電源線與訊號線是否鬆脫，並確認電源燈號。"
        )
    else:
        return TicketResponse(
            category="未分類/一般問題",
            suggestion="已為您記錄問題，IT 人員將於 15 分鐘內與您聯繫。"
        )

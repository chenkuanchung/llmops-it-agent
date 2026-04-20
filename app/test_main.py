from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """測試系統健康端點是否正常運作"""
    response = client.get("/health")
    assert response.status_code == 200

    # 配合新版 main.py 的回傳值，移除了 perfectly
    expected_response = {
        "status": "ok",
        "message": "Service is running."
    }
    assert response.json() == expected_response


def test_classify_ticket():
    """測試報修分類 API 是否能正確辨識硬體問題 (透過 LLM 推理)"""
    response = client.post(
        "/api/v1/classify",
        json={"description": "我的螢幕突然黑屏，怎麼辦？"}
    )
    # 🕵️‍♂️ 關鍵修改：如果不是 200，就把 API 內部的報錯訊息直接印在 Log 上
    assert response.status_code == 200, f"API 發生錯誤: {response.text}"
    assert response.json()["category"] == "硬體設備"

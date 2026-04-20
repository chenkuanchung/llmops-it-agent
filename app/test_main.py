from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """測試系統健康端點是否正常運作"""
    response = client.get("/health")
    assert response.status_code == 200

    # 這裡斷行以避免 E501 line too long
    expected_response = {
        "status": "ok",
        "message": "Service is running perfectly."
    }
    assert response.json() == expected_response


def test_classify_ticket_mock():
    """測試報修分類 API 是否能正確辨識硬體問題"""
    response = client.post(
        "/api/v1/classify",
        json={"description": "我的螢幕突然黑屏，怎麼辦？"}
    )
    assert response.status_code == 200
    assert response.json()["category"] == "硬體設備"

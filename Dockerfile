# 1. 使用官方的 Python 3.10 輕量版作為基礎映像檔 (Image)
FROM python:3.10-slim

# 2. 設定容器內的工作目錄
WORKDIR /code

# 3. 先複製 requirements.txt 到容器內
# 企業級細節：先複製套件清單而非全部程式碼，可以善用 Docker 緩存 (Cache)。
# 只要套件沒變，未來重新打包的速度就會非常快！
COPY requirements.txt .

# 4. 安裝 Python 依賴套件 (--no-cache-dir 有助於縮小 Image 體積)
RUN pip install --no-cache-dir -r requirements.txt

# 5. 將本機的 app 資料夾內容複製到容器內的 /code/app 目錄
COPY ./app ./app

# 6. 宣告服務預計使用的 Port (這只是說明作用，實際綁定在 run 指令設定)
EXPOSE 8000

# 7. 設定容器啟動時預設要執行的指令
# 注意這裡 host 設定為 0.0.0.0，才能讓容器外的請求連進來
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
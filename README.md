# 🚀 LLMOps IT Agent: Enterprise-Grade CI/CD Pipeline 實作

![CI/CD Pipeline Status](https://img.shields.io/badge/Pipeline-Passed-success?style=for-the-badge&logo=gitlab)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue?style=for-the-badge&logo=docker)
![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)

> **專案核心目標：** 從零搭建符合業界標準的六階段自動化管線，解決 AI 應用在開發（Dev）與營運（Ops）間的斷層，並成功實作「雲端控管、本地執行」的混合式部署架構。

---

## 📋 目錄
1. [專案動機與目的](#專案動機與目的)
2. [CI/CD 全自動管線架構](#cicd-全自動管線架構)
3. [六大階段詳解](#六大階段詳解)
4. [真實世界 vs. 本機模擬：架構對應圖](#真實世界-vs-本機模擬)
5. [技術細節與問題解決 (Troubleshooting)](#技術細節與問題解決)
6. [如何重現此專案 (Getting Started)](#如何重現此專案)

---

## 1. 專案動機與目的
在 AI 應用快速迭代的時代，單純編寫模型邏輯已不足夠。本專案旨在透過 **LLMOps** 的實踐，建立一套專業的軟體交付流程：
* **實踐 LLMOps 精神：** 確保 AI 代理在更新邏輯或模型後，能透過自動化測試與部署，降低人為出貨錯誤。
* **技術力證明：** * 掌握 **GitLab CI/CD** 語法與階段規劃 (Pipeline as Code)。
    * 實作 **Docker** 容器化封裝 與 Container Registry 管理。
    * 解決 Windows 複雜環境下的自動化部署難點，確保「環境一致性」。

---

## 2. CI/CD 全自動管線架構


本專案採用 6-Stage 流水線設計，模擬企業從程式碼提交到正式上線的完整生命週期：
`Lint` ➔ `Test` ➔ `Build` ➔ `Deploy (Staging)` ➔ `Verify` ➔ `Deploy (Prod)`

---

## 3. 六大階段詳解

### Stage 1: Lint (品質審查)
使用 `flake8` 進行靜態程式碼分析，確保團隊開發規範一致，避免潛在語法錯誤。

### Stage 2: Test (自動化測試)
利用 `pytest` 執行單元測試，驗證 AI 分類邏輯與系統健康檢查端點是否運作正常。

### Stage 3: Build (建置打包)
根據 `Dockerfile` 自動建置 Python 3.10 輕量化映像檔，並推送至 GitLab Container Registry 儲存。

### Stage 4: Deploy to Staging (自動化部署)
透過安裝在本地端的 **GitLab Runner**，自動執行 `docker-compose` 指令，將最新的映像檔拉取至本機環境運行。

### Stage 5: Verify (系統整合測試)
實作「網路穿透測試」，利用 PowerShell 指令對本機運行的 API 進行真實網路請求，確保服務不僅啟動，且路由正確。

### Stage 6: Deploy to Production (生產發布)
設定 **Manual Trigger (手動核准)** 機制，模擬企業最後審核流程。只有在開發者點擊確認後，系統才會執行正式環境的發布指令。

---

## 4. 真實世界 vs. 本機模擬

| 流程階段 | 真實企業環境 (AWS/GCP) | 本專案模擬方案 |
| :--- | :--- | :--- |
| **Runner 執行環境** | 雲端託管機器人 (SaaS Runners) | **Local Windows Runner (Hybrid)** |
| **部署目標** | 遠端雲端伺服器 (EC2 / K8s) | **本機 Docker 容器** |
| **網路驗證** | 公網域名 / 內網負載平衡測試 | **PowerShell 內網穿透測試** |
| **AI 邏輯** | 串接 OpenAI / 自建 LLM 叢集 | **Mock AI 分類邏輯 (關鍵字推理)** |

---

## 5. 技術細節與問題解決 (Troubleshooting)
在本專案實作中，最大的挑戰在於處理 **Windows 環境下的 CI/CD 執行衝突**：

* **PowerShell 編碼崩潰：** 傳統 PowerShell 5.1 對 UTF-8 支援不佳，導致 CI 腳本亂碼。解決方案為升級至 **PowerShell 7 (pwsh)** 並將 Runner 設定檔改為 `shell = "pwsh"`。
* **Git Index Lock：** 當 CI 指令意外中斷時，會留下鎖定檔。實作了自動化的 `Remove-Item` 腳本，確保每一次 Pipeline 運行前工作區都是乾淨的。
* **Docker 網路隔離：** 解決了容器內部無法訪問主機 `localhost` 的問題，確保 Stage 5 的整合測試能真實打向本機 API。

---

## 6. 如何重現此專案 (Getting Started)

### 🛠️ 必備工具
* **Windows 使用者：**
    * 安裝 [Docker Desktop](https://www.docker.com/products/docker-desktop/)。
    * 安裝 [PowerShell 7](https://github.com/PowerShell/PowerShell)。
    * 下載 [GitLab Runner for Windows](https://docs.gitlab.com/runner/install/windows.html)。
* **Linux 使用者：**
    * 安裝 `docker` 與 `docker-compose-plugin`。

### 🚀 快速啟動

1. **Clone 專案與替換環境參數 (重要)：** 下載本專案後，請打開 `deployment/docker-compose.staging.yml` 檔案，將 `image:` 屬性中的 `<YOUR_GITLAB_USERNAME>` 替換為你自己的 GitLab 或 Docker Hub 帳號名稱，否則將無法正確拉取映像檔。
2. **註冊 Runner：** 在 GitLab 專案中建立 Runner，並獲得 Registration Token。
3. **設定設定檔：** 修改本機的 `C:\GitLab-Runner\config.toml`，設定 `executor = "shell"` 與 `shell = "pwsh"`。
4. **環境變數：** 確保 Runner 具備操作 Docker 的權限。
5. **推送程式碼：** 執行 `git push` 後即可在 GitLab 介面觀察全自動流水線。

---

### 技術棧 (Tech Stack)
* **Backend:** FastAPI
* **Testing:** Pytest, Flake8
* **DevOps:** GitLab CI/CD, Docker, Docker-Compose
* **Infrastructure:** GitLab Local Runner (Windows)

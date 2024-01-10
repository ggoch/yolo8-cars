車牌與車子種類辨識
===

### 第一步 安裝所需套件

假設你已安裝完python3，在專案目錄下用CMD開啟(絕對路徑不能有中文)

```cmd
建立虛擬環境病雞依賴安裝在橡木資料夾，避免汙染全域環境
python -m venv cuda

cuda\Scripts\activate

安裝yolov8框架工具
pip install ultralytics

如果要使用gpu加速運行請額外安裝pytorch工具
這行指令由pyTroch官網獲得
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

(torchvision有可能會不是gpu版本，安裝後請用pip list 確認後面是否有+cu11x)
```

### 第二步 下載車牌資料集

//車牌資料位置
https://www.kaggle.com/datasets/andrewmvd/car-plate-detection?resource=download

下載後請解壓縮放在項目內，並檢查底下應該會有annotations和images資料夾

### 第三步 執行main.py 該程式會把kaggle轉成標籤並分成資料及做訓練，訓練後會用影片作驗證

### 備註(影片和模型在github的Releases)

### 第三步 用jupyter開發(未完成)

```
jupyter notebook

python -m ipykernel install --user --name=cuda --display-name "cuda-gpt"
```

LLM學習
===

### 第一步 安裝所需套件

假設你已安裝完python3，在專案目錄下用CMD開啟(絕對路徑不能有中文)

```cmd
用cuda運行
python -m venv cuda

cuda\Scripts\activate


//這行指令由pyTroch官網獲得
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

pip install ultralytics
```

### 第二步 用jupyter讀取學習資料

```
jupyter notebook

python -m ipykernel install --user --name=cuda --display-name "cuda-gpt"
```

//車牌資料位置
https://www.kaggle.com/datasets/andrewmvd/car-plate-detection?resource=download
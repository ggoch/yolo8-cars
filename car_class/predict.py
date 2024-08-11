from ultralytics import YOLO

class PredictCarClass():
    def __init__(self,model_path,task):
        self.model = YOLO(model_path, task=task)

    def predict(self,img):
        results = self.model.predict(img, save=False)
        probs = results[0].probs
        names = self.model.names
        img = results[0].plot()
        
        if probs.top1conf < 0.9:
            return None,img

        return names[probs.top1],img

    def plot(self,img):
        results = self.model.predict(img, save=False)
        return results[0].plot()
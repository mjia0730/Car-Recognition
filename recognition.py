import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO
from PIL import Image
from classifier import predict

detector = YOLO('best.pt')

def data_loading(result):
    car_info = pd.read_csv('car_data.csv')
    return car_info.loc[car_info['model_name'] == result].values

def recognition(img_path):
    detection_results = detector(img_path)
    image = cv2.imread(img_path)
    for res in detection_results:
        for box in res.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy.numpy()[0])
            roi = image[y1:y2, x1:x2]
            pil_roi = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))

            result = predict(pil_roi)
            car_info = data_loading(result)
            return x1, y1, x2, y2, result, car_info


if __name__ == "__main__":
    img_path = '00663.jpg'
    x1, y1, x2, y2, result, car_info = recognition(img_path)

    image = cv2.imread(img_path)
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(image, result, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow('Detected', image)
    print(car_info)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
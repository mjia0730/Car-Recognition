# Car Recognition

## How to run?
1. Download the folder from main branch (data and training folder are optional), and open recognition.py
2. Change the img_path to your desired image file path if you want
3. Run recognition.py

## Output
x1, y1, x2, y2, results, car_info
1. x1, y1, x2, y2 = bounding boxes of the detected car
2. results = model name of the detected car
3. car_info = a list of information about the detected model
   - price: manufacturer's suggested retail price (MSRP) in USD
   - engine: type of engine
   - MPG: measure for a car's fuel (Miles Per Gallon)
   - seating: seating capacity
   - transmission: type of transmission
   - power: power of the car

* data folder: contains script on web scrapping the car information
* training folder: training of the YOLO model and image classification model in (.ipynb) format

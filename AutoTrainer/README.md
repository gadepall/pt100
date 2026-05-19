
# Automated OCR Training Pipeline
 
A Python-based pipeline that uses a webcam feed to automatically capture and log voltage and temperature readings from physical displays, building a dataset for OCR model training.
<img width="1252" height="424" alt="image" src="https://github.com/user-attachments/assets/4db5ebca-a4bb-4b6c-b582-2932fa03fd34" />
---
 
## Prerequisites
 
### Hardware & Software Setup
 
1. Install [**DroidCam**](https://droidcam.app) on your Android device (optional — any webcam works).
2. Install [**OBS Studio**](https://obsproject.com) on your Linux laptop.
3. Connect your Android phone to your Linux laptop, open DroidCam, and select the DroidCam device from OBS Studio's menu.
> **Note:** Any webcam that [OpenCV](https://github.com/opencv/opencv) can detect will work, including a built-in laptop camera or USB webcam. DroidCam + OBS is just one example setup.
 
### Python Libraries
 
Install the required packages:
 
```bash
pip install opencv-python easyocr numpy
```
 
> **Note:** [`easyocr`](https://github.com/jaidedai/easyocr) will also install [**PyTorch**](https://pytorch.org), which is a large download and a required dependency.
 
---
 
## Collecting the Dataset
 
1. Navigate to the project directory and run the script:
   ```
   https://github.com/gadepall/pt100/AutoTrainer/
   ```
 
   ```bash
   python a.py
   ```
 
2. Two windows will appear: **`Voltage`** and **`Temperature`**. These show the exact regions being sent to the OCR engine.
3. To stop the script, click on one of the windows to make it active, then **press `q`**.
The script uses OpenCV and EasyOCR to capture video from the webcam, read text from two specific regions (voltage and temperature), and log the data to a file. It is designed for a fixed-camera setup — for example, reading from an LCD screen and a separate thermometer.
 
---
 
## Output
 
The script generates two types of output:
 
### `out.txt`
Logs detected readings. Every 15 frames, if text is found in both regions, a new line is appended in the format:
 
```
[voltage_reading] [temperature_reading]
```
 
### `img/` Directory
Saves cropped images (`voltageXX.png`, `tempXX.png`) of the exact frames sent to EasyOCR. Use these for debugging calibration issues.
 
**Directory structure:**
 
```
codes/
├── out.txt
└── img/
    ├── voltage_1.png
    ├── temperature_1.png
    ├── voltage_2.png
    ├── temperature_2.png
    └── ...
```
 
> `out.txt` may contain some incorrect readings due to OCR errors. In such cases, manually correct the data and save it as `trainingdata.txt`.
 
The final training data is available at:
 
```
https://github.com/gadepall/pt100/blob/main/AutoTrainer/trainingdata.txt
```
 
---
 
## Important! -  Calibration Required
 
**The script will not work correctly without calibration.** The following adjustments must be made in `a.py`:
 
### 1. GPU Usage
 
If you do **not** have a compatible NVIDIA GPU, change:
 
```python
# From:
reader = easyocr.Reader(['en'], gpu=True)
 
# To:
reader = easyocr.Reader(['en'], gpu=False)
```
 
The script will run slower on CPU but will still function.
 
---
 
### 2. Frame Cropping
 
This is the most critical calibration step. The script must be told exactly where to look for each reading. Adjust the crop parameters to match your camera setup:
 
```python
# Change the crop values according to requirement
voltage_frame = frame[0:int(h/2), :]
temp_frame = frame[int(h/2):, 0:int(w/3)]
```
 
- `voltage_frame` — currently set to the **top half** of the entire camera feed.
- `temp_frame` — currently set to the **bottom-left third** of the feed.
Adjust the `h/2`, `w/3` values to precisely isolate the readings. Watch the **`Voltage`** and **`Temperature`** windows to verify, then re-run until the crop regions are correct.
 
---
 
### 3. Image Processing
 
The following code for reading the physical thermometer may need to be modified depending on your camera, lighting, and display:
 
```python
# These values need to be calibrated according to requirement
gray_t = cv2.cvtColor(temp_frame, cv2.COLOR_BGR2GRAY)
t_lower = 50
t_upper = 100
_, thres = cv2.threshold(gray_t, 130, 255, cv2.THRESH_BINARY_INV)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))
closed_img = cv2.morphologyEx(thres, cv2.MORPH_CLOSE, kernel)
pretemp = cv2.bitwise_not(closed_img)
temp = cv2.GaussianBlur(pretemp, (17, 17), 0)
```
 
**Key values to adjust:**
 

ParameterDescription`cv2.threshold(gray_t, 130, 255, cv2.THRESH_BINARY_INV)``130` is the threshold value — highly sensitive to lighting. Adjust up or down until the text is clearly separated from the background in the `Temperature` window.`cv2.getStructuringElement(cv2.MORPH_RECT, (11, 11))`Kernel size for the morphological closing operation, which connects broken parts of a digit. Increase or decrease as needed.`cv2.GaussianBlur(pretemp, (17, 17), 0)`Kernel size for the Gaussian blur.

While calibrating, watch the **`Temperature`** window. The goal is to make the digits clear and solid while removing as much background noise as possible. It is also recommended to hide the decimal point, either physically or through additional image processing. It can also be done by displaying the voltage in millivolts.

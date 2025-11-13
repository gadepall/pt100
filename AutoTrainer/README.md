# PT-100
---
# Auto trainer for PT-100

This script uses OpenCV and EasyOCR to capture video from a webcam, identify and read text from two specific regions (voltage and temperature in this case), and log this data to a file.

It is designed to be calibrated for a specific, fixed-camera setup, such as this case where we are reading data from an LCD screen and a separate standard thermometer.

##  Getting Started

Follow these instructions to get the script up and running on your local machine.

### Prerequisites

Before you run the script, you'll need a few things set up.

**Hardware:**
* A webcam connected to your computer.
* **(Not necessary)** An NVIDIA GPU with CUDA installed. The script is pre-set to use `gpu=True` for much faster processing.

**Software:**
* Python 3.x
* The required Python libraries: [`opencv-python`](https://pypi.org/project/opencv-python/), [`easyocr`](https://github.com/JaidedAI/EasyOCR?tab=readme-ov-file), and [`numpy`](https://numpy.org/).

 #### A Note on the Webcam (Optional)
This script will work with any webcam that OpenCV can detect, including built-in laptop cameras or standard USB webcams. The most important factor is a stable, well-positioned camera.

For reference, the development and testing for this project were done using a virtual camera setup:

[DroidCam](https://droidcam.app/obs/): An application to use a smartphone as a high-quality webcam.

[OBS Studio](https://obsproject.com/): This software was used to capture the DroidCam feed and output it as an "OBS Virtual Camera," which was then selected by the Python script.

Again, this specific setup is not required. It is just one example of how to provide a camera feed to the script. Any simple webcam will work perfectly fine.

### Installation

1.  **Create a Directory for Images:**
    The script is hardcoded to save debug images to an `img/` folder. You must create this folder in the same directory as the script for the program to run.
    ```bash
    mkdir img
    ```

2.  **Install Python Libraries:**
    Install the necessary packages using `pip`:
    ```bash
    pip install opencv-python easyocr numpy
    ```
    > **Note:** [`easyocr`](https://github.com/JaidedAI/EasyOCR?tab=readme-ov-file) will also install [PyTorch](https://pytorch.org/), which is a large download and a required dependency.

##  How to Run

1.  Make sure your webcam is plugged in and positioned correctly to see both your target readings.
2.  Open a terminal and navigate to the folder containing `a.py`.
3.  Run the script:
    ```bash
    python3 a.py
    ```
4.  Two windows will appear: 'Voltage' and 'Temperature'. These show the exact (and processed) regions being sent to the OCR engine.
5.  To stop the script, make sure one of these windows is active (click on it) and **press the 'q' key**.

---

##  Important: Calibration is Required!

This script **will not work correctly** without calibration. You must adjust the code to fit your specific camera, lighting, and display setup.

Here are the key sections you **must** modify in `a.py`:

### 1. GPU Usage

If you **do not** have a compatible NVIDIA GPU, you must change this line:

```python
# From:
reader = easyocr.Reader(['en'], gpu=True)

# To:
reader = easyocr.Reader(['en'], gpu=False)
```

The script will run much slower on the CPU but will still function.

### 2. Frame Cropping
This is the most critical part. You need to tell the script exactly where to look for your data.

```python
#Change the crop values according to requirement
voltage_frame = frame[0:int(h/2), :]
temp_frame = frame[int(h/2):, 0:int(w/3)]
```

Python slices are in [y1:y2, x1:x2] format (rows, then columns).

`voltage_frame` is currently set to the top half of the entire camera feed.

`temp_frame` is set to the bottom-left third of the feed.

You must change these pixel/percentage values to precisely isolate your voltage and temperature readings. The `Voltage` and `Temperature` windows will show you what the script sees in these cropped zones, so you can adjust the values and re-run until they are correct.

### 3. Image Processing

#### a. Temperature
```python
#These values need to be calibrated acccording to requirement
gray_t = cv2.cvtColor(temp_frame, cv2.COLOR_BGR2GRAY)
t_lower = 50
t_upper = 100
_,thres = cv2.threshold(gray_t,130, 255, cv2.THRESH_BINARY_INV)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11,11))
closed_img = cv2.morphologyEx(thres, cv2.MORPH_CLOSE, kernel)
pretemp = cv2.bitwise_not(closed_img)
temp = cv2.GaussianBlur(pretemp, (17,17), 0)
```

* ##### Key Values to Change:

`cv2.threshold(gray_t,130, 255, cv2.THRESH_BINARY_INV)`: The 130 is the threshold value. This is highly sensitive to lighting. Adjust it up or down until the text is clearly separated from the background in the 'Temperature' window.

`cv2.getStructuringElement(cv2.MORPH_RECT, (11,11))`: This is the kernel size for the 'closing' operation, which helps connect broken parts of a number. You may need to make it larger or smaller.

`cv2.GaussianBlur(pretemp, (17,17), 0)`: This is the kernel size for the blur.

Look at the `Temperature` window while calibrating. Your goal is to make the numbers you want to read clear and solid, while removing as much background noise as possible.

It is also preferred to hide the decimal point, either physically or by further image processing.

#### b. Voltage
In this case, the cropped voltage frame, is converted to grayscale before it is used for OCR. Make sure the voltage reading is visible in the voltage frame. It is also preferred to hide the decimal point, either physically or by further image processing.
  
##  Data Collection Methodology

The dataset is collected by simulating a **real-world thermal change (cooling cycle)** to capture paired temperature readings.

1. **Setup:**  
   - Place both the PT100 probe and the reference thermometer inside an electric kettle, submerged in water.

2. **Heating Phase:**  
   - Turn on the kettle and heat the water to its boiling point.

3. **Recording Phase:**  
   - Switch off the kettle at boiling point.
   - Start recording a **video** using the smartphone.
   - Ensure **both the PT100 LCD display** and **reference thermometer** are visible in the frame.

4. **Cooling Phase:**  
   - Continue recording the cooling process as the water temperature drops naturally.

5. **Data Extraction:**  
   - The recorded video acts as the raw dataset.  
   - Extract frames and apply **OCR (Optical Character Recognition)** to detect readings from both displays.  

 ---

## Output

The script generates two types of output:

* `out.txt`: A text file that logs the detected readings. Every 15 frames, if text is found in both regions, a new line is added, formatted as: [voltage_reading] [temperature_reading]

* `img/` Directory: This folder saves voltageXX.png and tempXX.png images. These are the exact frames that were sent to EasyOCR. If you are getting bad readings, check these images to see why. They are perfect for debugging your calibration and fixing the readings.

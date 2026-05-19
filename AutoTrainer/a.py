import cv2
import easyocr
import numpy as np
import time

# Use gpu=True if you have a compatible GPU for faster processing.
reader = easyocr.Reader(['en'], gpu=True)

#Search for cameras. Set i = 0 for default cameras
for i in range(0,5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        break
    else:
        print(f'Camera {i} not available')

print("Starting webcam. Press 'q' to exit.")

counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break
    h = frame.shape[0]
    w = frame.shape[1]

    #Change the crop values according to requirement
    voltage_frame = frame[0:int(h/2), :]
    temp_frame = frame[int(h/2):, 0:int(w/3)]
    counter += 1
    
    #These values need to be calibrated acccording to requirement
    volt = voltage_frame

    gray_t = cv2.cvtColor(temp_frame, cv2.COLOR_BGR2GRAY)
    t_lower = 50
    t_upper = 100
    _,thres = cv2.threshold(gray_t,130, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11,11))
    closed_img = cv2.morphologyEx(thres, cv2.MORPH_CLOSE, kernel)
    pretemp = cv2.bitwise_not(closed_img)
    temp = cv2.GaussianBlur(pretemp, (17,17), 0)

    voltagereadings = reader.readtext(volt, detail=0)
    temperaturereadings = reader.readtext(temp, detail = 0)

    if (counter % 15 == 0):
            if(len(voltagereadings) > 0 and len(temperaturereadings) > 0):
                with open('out.txt', 'a') as output:
                    row = voltagereadings[0]
                    row += ' '
                    row += temperaturereadings[0]
                    row += '\n'
                    output.write(row)
                    print(f'Voltage is : {voltagereadings[0]}') 
                    print(f'Temperature is: {temperaturereadings[0]}')
                    cv2.imwrite(f'img/voltage{int(counter/5)}.png', volt)
                    cv2.imwrite(f'img/temp{int(counter/5)}.png', temp)
    
    cv2.imshow('Voltage', volt)
    cv2.imshow('Temperature', temp)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

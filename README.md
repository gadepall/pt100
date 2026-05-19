# AI-Based High-Precision Industrial Thermometer (PT100)

A cost-effective PT100 sensor calibration system using OCR-based automated data collection and machine learning regression models — no thermal chamber required.

## Overview

PT100 RTDs are standard for industrial precision thermometry but traditionally require expensive calibration hardware. This project replaces that with:

1. An **OCR pipeline** that automatically pairs analog thermometer readings with sensor voltages during a natural cooling cycle (see [`AutoTrainer/README.md`](AutoTrainer/README.md)).
2. **ML regression models** trained on that data to predict temperature from voltage.

## Hardware

Two analog front-ends were evaluated:

| Setup | ADC | Notes |
|---|---|---|
| Wheatstone Bridge + ADS1115 | 16-bit external | High precision, differential measurement |
| Simple Voltage Divider | 10-bit internal (Arduino) | Lower cost, simpler circuit |

**Common components:** Arduino Uno, PT100 RTD, JHD 162A LCD, 22kΩ potentiometer, breadboard and jumper wires.

**Wheatstone bridge additions:** ADS1115 ADC, 100Ω precision resistor, two 4kΩ resistors.

Full pin connection tables and circuit schematics are in the paper (Appendix A). Arduino data collection code is [here](https://github.com/gadepall/pt100/tree/main/codes/arduino/datacollection).

## Models

Three models were evaluated, all fitting a quadratic curve motivated by the Callendar-Van Dusen equation (R(t) = R₀(1 + At + Bt²)):

- **LSQ (Quadratic)** — physically-informed least squares; forward model `T = aV² + bV + c`
- **SGD Regressor** — stochastic gradient descent on a polynomial feature expansion
- **Random Forest Regressor** — ensemble tree-based model

## Results

Tested on the Wheatstone bridge + ADS1115 setup:

| Model | MSE | R² |
|---|---|---|
| LSQ Quadratic | **0.009198** | **0.999956** |
| Inverse LSQ | 0.016221 | 0.999922 |
| SGD Regressor | 0.030477 | 0.999854 |
| Random Forest | 1.161318 | 0.994451 |
| Voltage Divider (no ADC) | 0.6612 | 0.9977 |

The **LSQ Quadratic model on the Wheatstone bridge** is the clear winner. The Random Forest performs worst due to its step-function interpolation being poorly suited to continuous analog data.

Model implementation and evaluation notebook: [`codes/models/PT100_models.ipynb`](https://github.com/gadepall/pt100/blob/main/codes/models/PT100_models.ipynb)  
Temperature inference Arduino code: [`codes/arduino/inference`](https://github.com/gadepall/pt100/tree/main/codes/arduino/inference/code)

## Data Collection

See **[`AutoTrainer/README.md`](AutoTrainer/README.md)** for the full OCR pipeline setup and calibration guide.

The final training dataset: [`AutoTrainer/trainingdata.txt`](https://github.com/gadepall/pt100/blob/main/AutoTrainer/trainingdata.txt)

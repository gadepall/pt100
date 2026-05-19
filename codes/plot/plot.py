import matplotlib.pyplot as plt
import numpy as np

# --- Data from Context Files ---

# Experiment 1: Training Data (Low Voltage)
t_exp1_train = np.array([
    26.7, 36.7, 43.9, 47.8, 56.6, 59.1, 60.0, 72.0, 79.1, 85.3, 87.5, 90.0, 91.4, 94.6
])
v_exp1_train = np.array([
    0.20171, 0.23471, 0.26471, 0.28671, 0.29541, 0.30671, 0.30821, 0.35171, 0.37671, 0.39771, 0.43271, 0.44671, 0.45271, 0.45871
])

# Experiment 1: Validation Data (Low Voltage)
t_exp1_val = np.array([36.8, 93.1, 57.3, 73.4])
v_exp1_val = np.array([0.23571, 0.45391, 0.29921, 0.35621])

# Experiment 2: Training Data (High Voltage)
t_exp2_train = np.array([
    32.1, 36.6, 41.1, 45.5, 50.8, 56.8, 62.1, 67.6, 71.8, 76.6, 81.3, 85.9, 90.9, 95.9, 97.6
])
v_exp2_train = np.array([
    2.66, 2.67, 2.68, 2.69, 2.71, 2.74, 2.75, 2.77, 2.79, 2.81, 2.82, 2.83, 2.85, 2.87, 2.89
])

# Experiment 2: Validation Data (High Voltage)
t_exp2_val = np.array([
    32.0, 36.5, 41.0, 45.5, 50.5, 56.6, 62.0, 67.5, 71.5, 76.5, 81.1, 85.9, 90.7, 95.5, 97.5
])
v_exp2_val = np.array([
    2.66, 2.67, 2.68, 2.69, 2.71, 2.74, 2.75, 2.77, 2.79, 2.81, 2.82, 2.82, 2.85, 2.87, 2.89
])

# Model 2 (SGD) Predicted Points from Validation
v_model2_pts = np.array([
    2.66, 2.67, 2.68, 2.69, 2.71, 2.74, 2.75, 2.77, 2.79, 2.81, 2.82, 2.82, 2.85, 2.87, 2.89
])
t_model2_preds = np.array([
    31.89, 36.46, 41.00, 45.50, 50.41, 56.59, 62.13, 67.56, 71.74, 76.60, 81.33, 81.33, 90.57, 95.04, 97.35
])


# --- Voltage Normalization (New) ---
# We will normalize both voltage datasets to the range [0, 1]
# to plot them on the same x-axis.

# Find min/max for Exp 1
v_exp1_all = np.concatenate((v_exp1_train, v_exp1_val))
v1_min, v1_max = v_exp1_all.min(), v_exp1_all.max()

# Find min/max for Exp 2
v_exp2_all = np.concatenate((v_exp2_train, v_exp2_val))
v2_min, v2_max = v_exp2_all.min(), v_exp2_all.max()

# Normalize all data points
v_exp1_train_norm = (v_exp1_train - v1_min) / (v1_max - v1_min)
v_exp1_val_norm = (v_exp1_val - v1_min) / (v1_max - v1_min)

v_exp2_train_norm = (v_exp2_train - v2_min) / (v2_max - v2_min)
v_exp2_val_norm = (v_exp2_val - v2_min) / (v2_max - v2_min)

# Normalize SGD model points
v_model2_pts_norm = (v_model2_pts - v2_min) / (v2_max - v2_min)


# --- Model Definitions for Normalized Plot ---

# Create a smooth normalized voltage range [0, 1] for plotting the curves
v_norm_curve = np.linspace(0, 1, 200)

# Model 1: LSQ V=f(T) (from Exp 1)
a1 = 1.7826e-5
b1 = 1.4987e-3
c1 = 0.1570
# "Un-normalize" the curve back to Exp 1's raw voltage range
v_raw_exp1 = v_norm_curve * (v1_max - v1_min) + v1_min
# Calculate T from the original formula
discriminant = b1**2 - 4*a1*(c1 - v_raw_exp1)
discriminant[discriminant < 0] = np.nan # Avoid math domain errors
t_model1 = (-b1 + np.sqrt(discriminant)) / (2*a1)

# Model 3: Inverse LSQ T=f(V) (from Exp 2)
a3 = 269.84
b3 = -953.11
c3 = 874.19
# "Un-normalize" the curve back to Exp 2's raw voltage range
v_raw_exp2 = v_norm_curve * (v2_max - v2_min) + v2_min
# Calculate T from the original formula
t_model3 = a3 * v_raw_exp2**2 + b3 * v_raw_exp2 + c3


# --- Plotting ---

plt.figure(figsize=(12, 7))

# Plot data points
plt.scatter(v_exp1_train_norm, t_exp1_train, 
            label='Exp 1 Training Data', marker='x', color='blue', alpha=0.7)
plt.scatter(v_exp1_val_norm, t_exp1_val, 
            label='Exp 1 Validation Data', marker='x', color='cyan', s=100)

plt.scatter(v_exp2_train_norm, t_exp2_train, 
            label='Exp 2 Training Data', marker='o', color='red', alpha=0.7, facecolors='none')
plt.scatter(v_exp2_val_norm, t_exp2_val, 
            label='Exp 2 Validation Data', marker='o', color='orange', s=100)

# Plot model curves
plt.plot(v_norm_curve, t_model1, label='Model 1: LSQ V=f(T) (from Exp 1)', color='blue', linestyle='-')

# Plot Model 2 (SGD) as points, sorting them to create a line
sort_indices = np.argsort(v_model2_pts_norm)
plt.plot(v_model2_pts_norm[sort_indices], t_model2_preds[sort_indices], 
         label='Model 2: SGD T=f(V) (Predictions)', color='green', linestyle='--', marker='^', markersize=4)

# Plot Model 3 (Inverse LSQ)
plt.plot(v_norm_curve, t_model3, label='Model 3: Inverse LSQ T=f(V) (from Exp 2)', color='red', linestyle='-')


# Add plot labels and formatting
plt.title('Comparison of All Models (Normalized Voltage)')
plt.xlabel('Normalized Voltage (Scaled from 0 to 1)')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.grid(True)
plt.ylim(20, 105) # Set Y-axis limits
plt.xlim(-0.05, 1.05) # Set X-axis limits
plt.savefig('../../figs/combined_model_plot.png')

import serial
import os
import serial
import time
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from tensorflow.keras.models import load_model
import pyautogui

serial_port = 'COM4'  # Replace with the appropriate serial port
baud_rate = 115200

# Open the serial port
ser = serial.Serial(serial_port, baud_rate)
print("Serial connection established with Arduino.")
# Wait for the Arduino to initialize
time.sleep(3)

# List of model paths and movements
model_paths = ['E:/DATA_SET/allnew_upperdown.h5', 'E:/DATA_SET/allnew_upperdown.h5', 'E:/DATA_SET/model_right_left.h5', 'E:/DATA_SET/model_right_left.h5']
movements = [(0, -100), (0, 100)]
movements_1 = [(100, 0), (-100, 0)]

# Perform prediction with different models and movements
for i in range(4):
    # Create an empty list to store the received data
    received_data = []

    # Start receiving data for 5ms to 6ms
    start_time = time.time()
    samples_received = 0  # Counter for received samples
    while samples_received < 5:
        line = ser.readline().decode().strip()
        if line:
            values = line.split(',')
            if len(values) != 3:
                continue  # Skip the line if it doesn't have 3 values

            try:
                values = [float(value) for value in values]
                received_data.append(values)
                samples_received += 1  # Increment the counter
            except ValueError:
                continue

    # Convert the list of values to a DataFrame
    df = pd.DataFrame(received_data, columns=['AnalogValue', 'density_value', 'amplitude'])
    print(df.head())
    # Perform Min-Max scaling on the data
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df)

    # Reshape the data into the desired shape
    reshaped_data = np.reshape(scaled_data, (scaled_data.shape[0], scaled_data.shape[1], 1))

    # Load the model
    model = load_model(model_paths[i])

    # Perform the prediction on the model
    prediction = model.predict(reshaped_data)

    # Get the second prediction result for each sample
    print("the prediction:", prediction)
    # Calculate the average of the predictions
    average_result = np.mean(prediction)

    # Determine the final result based on the average
    final_result = 0 if average_result <= 0.5 else 1

    # Check if it's the first two loops
    if i < 2:
        # Check if the final result is 0 and update the movement accordingly
        movement = movements[0] if final_result == 0 else movements[1]
    else:
        # Check if the final result is 0 and update the movement accordingly
        movement = movements_1[0] if final_result == 0 else movements_1[1]

    # Move the cursor based on the movement
    pyautogui.move(movement[0], movement[1], duration=0.5)

    # Print the result and movement
    print("Prediction:", final_result)
    print("Movement:", movement)

    # Wait for 2 seconds before proceeding to the next iteration
    time.sleep(3)

# Close the serial port
ser.close()

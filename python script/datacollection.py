import serial
import csv

serial_port = 'COM4'  # Replace with the appropriate serial port
baud_rate = 115200

# Open the serial port
ser = serial.Serial(serial_port, baud_rate)

# Create a CSV file to store the received values
csv_file_path = 'arduino_data_up.csv'

with open(csv_file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['AnalogValue', 'density_value', 'amplitude'])  # Write the header row

    try:
        # Read values from the serial port and write them to the CSV file
        while True:
            line = ser.readline().decode().strip()
            if line:
                values = line.split(',')
                try:
                    analog_value = float(values[0])
                    density_value = float(values[1])
                    amplitude = float(values[2])
                    writer.writerow([analog_value, density_value, amplitude])
                except (ValueError, IndexError):
                    continue
    except KeyboardInterrupt:
        pass

# Close the serial port
ser.close()

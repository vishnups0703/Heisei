# import necessary modules
import serial
import threading
import eel

# Initialize Eel
eel.init('web')

# Function to read from serial port
def read_from_port(ser):
    while True:
        if ser.isOpen():
            try:
                # Read data from serial port
                data = ser.readline().decode('utf-8').strip()
                # Print received data to console
                print(f"Received: {data}")
                # Pass data to Eel to update HTML
                eel.updateMessage(data)()
            except serial.SerialException as e:
                print(f"Error reading serial port: {e}")
                break

# Define function to start serial reading in a separate thread
def start_serial_reading(port, baudrate):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Serial port {port} opened successfully.")
        # Start a thread to read from serial port
        thread = threading.Thread(target=read_from_port, args=(ser,))
        thread.daemon = True  # Daemonize thread
        thread.start()
    except serial.SerialException as e:
        print(f"Error opening serial port {port}: {e}")

# Expose a function to start reading from serial port
@eel.expose
def start_reading():
    start_serial_reading('COM3', 9600)

# Start Eel
eel.start('main.html', size=(600, 400))


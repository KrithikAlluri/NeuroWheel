import serial
import time

# Setup serial communication
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Adjust port as necessary
time.sleep(2)  # Allow some time for the connection to establish

def send_voltages(v1, v2):
    # Construct the string to send
    message = f"{v1},{v2}\n"
    ser.write(message.encode())  # Send message to Arduino
    print(f"Sent: {message.strip()}")

try:
    while True:
        # Example values to send, could be replaced with actual inputs
        v1 = 2.5  # Neutral
        v2 = 4.5  # Forward
        
        send_voltages(v1, v2)
        
        # Wait 2 seconds before sending the next set of values
        time.sleep(2)

except KeyboardInterrupt:
    # Close serial communication on exit
    ser.close()
    print("Program terminated")
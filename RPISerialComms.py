import socket
import serial
import time

# Setup serial communication with Arduino
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Adjust port if necessary
time.sleep(2)  # Wait for the connection to establish

# Function to send voltages to Arduino
def send_voltages(v1, v2):
    message = f"{v1},{v2}\n"
    ser.write(message.encode())
    print(f"Sent to Arduino: {message.strip()}")

# Setup socket communication to receive from the computer
def receive_from_computer():
    server_ip = '0.0.0.0'  # Listen on all available interfaces
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((server_ip, port))
        s.listen()

        print(f"Listening for connections on {server_ip}:{port}...")

        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                # Extract and send the arcade values to the Arduino
                v1, v2 = map(float, data.decode().strip().split(','))
                send_voltages(v1, v2)

if __name__ == "__main__":
    try:
        while True:
            receive_from_computer()

    except KeyboardInterrupt:
        ser.close()
        print("Program terminated")

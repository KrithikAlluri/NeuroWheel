import socket

# Tank to Arcade conversion function
def tank_to_arcade(left_tank, right_tank):
    NEUTRAL = 2.5  # Neutral point for no movement
    MAX_OUTPUT = 5.0
    MIN_OUTPUT = 0.0

    # Forward/Backward (arcade_y)
    arcade_y = (left_tank + right_tank) / 2

    # Turning (arcade_x)
    arcade_x = (left_tank - right_tank) / 2

    # Convert to range 0 to 5
    arcade_y_mapped = NEUTRAL + arcade_y
    arcade_x_mapped = NEUTRAL + arcade_x

    # Ensure values are within the range 0 to 5
    arcade_y_mapped = max(MIN_OUTPUT, min(MAX_OUTPUT, arcade_y_mapped))
    arcade_x_mapped = max(MIN_OUTPUT, min(MAX_OUTPUT, arcade_x_mapped))

    return arcade_y_mapped, arcade_x_mapped

# Setup socket communication to send to Raspberry Pi
def send_to_rpi(arcade_y, arcade_x):
    server_ip = '192.168.68.101'  # Replace with the Raspberry Pi's IP
    port = 12345  # Port to use for socket communication

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip, port))
        message = f"{arcade_y},{arcade_x}\n"
        s.sendall(message.encode())
        print(f"Sent to Raspberry Pi: {message.strip()}")

if __name__ == "__main__":
    try:
        while True:
            # Example tank drive values (you can replace these with actual inputs)
            left_tank = float(input("Enter left tank value (0 to 5): "))
            right_tank = float(input("Enter right tank value (0 to 5): "))

            # Convert tank drive to arcade drive
            arcade_y, arcade_x = tank_to_arcade(left_tank, right_tank)

            # Send the converted arcade values to the Raspberry Pi
            send_to_rpi(arcade_y, arcade_x)

    except KeyboardInterrupt:
        print("Program terminated")
import serial




serial_port = 0
serial_path = "/dev/ttyUSB0" # default_path
def open_port(path, baud):
    try:
        serial_port = serial.Serial(path, baud)
        print(serial_port.name) # prints out the actual path that was used when opened
    except serial.SerialException:
        print("failed to open port")

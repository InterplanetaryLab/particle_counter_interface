from metone_serial import MetOneSerial
x = MetOneSerial("/dev/ttyUSB0")
x.open_port()
x.write_serial(MetOneSerial.COMMAND_CLEAR_BUFFER)
x.close_port()

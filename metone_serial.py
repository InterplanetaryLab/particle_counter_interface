import serial
import time
import json

class MetOneSerial: 
    COMMAND_AUTO = 'a'
    COMMAND_MANUAL = 'b'
    COMMAND_START_COUNTING_COMP = 'c'
    COMMAND_START_COUNTING_COUNT = 'd'
    COMMAND_STOP_COUNTING = 'e'
    COMMAND_CLEAR_BUFFER = 'C'
    COMMAND_SEND_NUM_RECORDS = 'D'
    COMMAND_SEND_EPROM_REVISION = 'E'
    COMMAND_MODE_REQUEST = 'M'
    COMMAND_IDENTIFY_MODEL = 'T'
    COMMAND_SEND_RECORD = 'A'
    COMMAND_RESEND_RECORD = 'R'
    COMMAND_STANDBY_MODE = 'h'
    COMMAND_ACTIVE_MODE = 'g'
    COMMAND_LOCAL_MODE = 'l'
    COMMAND_UNIVERSAL_SELECT = 'U'

    serial_path = "/dev/ttyUSB0"
    serial_port = 0
    baud = 9600

    def __init__(self,path): 
        self.serial_path = path
    
    def open_port(self):
        if self.serial_port == 0:
            try:
                self.serial_port = serial.Serial(self.serial_path, MetOneSerial.baud)
                print("open port path: %s" %self.serial_port.name)
            except serial.SerialException:
                print("failed to open port")
                self.serial_port = 0
    def close_port(self):
        if self.serial_port != 0:
            try:
                self.serial_port.close()
                self.serial = 0
            except serial.SerialException:
                print("failed to close port")
                self.serial_port = 0

    def write_serial(self,command):
        if self.serial_port != 0:
            try:
                self.serial_port.write(str.encode(command))
            except serial.SerialException:
                print("exception occured while trying to write: %s" %command)
        else:
            print("port not open. open it before attempting to use it")

    # starts the particle counter using the auto settings
    def auto_count(self):
        self.write_serial(COMMAND_AUTO)
        self.write_serial(COMMAND_START_COUNTING_COUNT)

    def auto_count_time_set(self, seconds):
        self.write_serial(COMMAND_AUTO) 
        time.sleep(count_sec_len)
        self.write_serial(COMMAND_STOP_COUNTING)

    def retrieve_record(self):
        message_raw = []
        message_dict = {
                "status":"",
                "date":"",
                "time":"",
                "period":"",
                "size1_count":"",
                "size2_count":"",
                "size3_count":"",
                "size4_count":"",
                "size5_count":"",
                "size6_count":"",
                }
        self.serial_port.reset_input_buffer()
        self.write_serial(COMMAND_SEND_RECORD)
        read_char = serial.read()
        while read_char != "\r\n":
            read_char = serial.read()
            message_raw.append(read_char)
        return [message_raw, message_dict]

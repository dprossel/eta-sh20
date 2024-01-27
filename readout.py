import serial

port = "/dev/ttyS0"
baud = 19200

#startbits = 1; stopbits = 1; databits = 8; parity = none

# msg format:
# |{|fcode1|fcode2|length|check|msg...|}|}|

def construct_message(fcode, message):
    l = len(message)
    c = sum(message, start=0x00)
    msg = bytearray([0x7b, *fcode, l, c, *message, 0x7d])
    return msg

def send_message(ser, message):
    ser.write(message)

def subscribe(ser, values, interval=10):
    send_message(ser, construct_message([0x4d, 0x43], [interval, 0x08, 0x00, v for v in values]))

def unsubscribe(ser):
    send_message(ser, construct_message([0x4d, 0x45], []))

def decode(msg):
    l = msg[3]
    values = []
    for v in range(l/5):
         values.append((msg[5 + v * 5 +1] + msg[5 + v * 5 +2], msg[5 + v * 5 +3] << 8 + msg[5 + v * 5 +4]))

def main():
        ser = serial.Serial(port, baud)

        # Temp top, mid, bot, avg
        subscribe(ser, [0x0c, 0x0b, 0x0a, 0x0d])
        while True:
            msg = ser.read()
            print(msg)
            values = decode(msg)
            print(values)



if __name__ == "__main__":
    main()



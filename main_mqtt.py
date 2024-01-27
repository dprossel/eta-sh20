# Complete project details at https://RandomNerdTutorials.com

from machine import UART

def sub_cb(topic, msg):
  print((topic, msg))
  if topic == b'notification' and msg == b'received':
    print('ESP received hello message')

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  #client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

def construct_message(fcode, message):
    l = len(message)
    c = sum(message, 0)
    msg = bytearray([0x7b] + fcode + [l, c] + message + [0x7d])
    print(msg)
    return msg

def decode(msg):
    l = msg[3]
    values = []
    for v in range(l/5):
         values.append((msg[5 + v * 5 +1] + msg[5 + v * 5 +2], msg[5 + v * 5 +3] << 8 + msg[5 + v * 5 +4]))

def subscribe(ser, values, interval=10):
    send_message(ser, construct_message([0x4d, 0x43], [interval] + sum([[0x08, 0x00, v] for v in values], [])))

def unsubscribe(ser):
    send_message(ser, construct_message([0x4d, 0x45], []))

def send_message(ser, message):
    ser.write(message)

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

baud = 19200
uart = UART(2, baud)
uart.init(baud, bits=8, parity=None, stop=1, timeout=10000)

topic_names = ["Temperatur_oben", "Temperatur_mitte", "Temperatur_unten", "Temperatur"]
print("Subscribing")
subscribe(uart, [0x0c, 0x0b, 0x0a, 0x0d])

while True:
  try:
    #client.check_msg()
    msg = uart.read()
    print(msg)
    if msg == None:
        continue
    values = decode(msg)
    print(values)
    for name, value in zip(topic_names, values):
      mqtt_msg = "%d" % value
      client.publish(topic_pub + "/" + name, mqtt_msg)

  except OSError as e:
    restart_and_reconnect()

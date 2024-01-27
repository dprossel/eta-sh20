from MicroWebSrv2 import *
import json

class SH20Uart:
    def __init__(self, uart_id=2, baudrate=19200, device_file="values.json"):
        self.uart_id = uart_id
        self.baud = baudrate
        self.uart = None
        self.device = None

        if device_file is not None:
           with open(device_file) as f:
            self.device = json.load(f)
           
    def connect(self):
       self.uart = machine.UART(self.uart_id, self.baud)
       self.uart.init(self.baud, bits=8, parity=None, stop=1, timeout=10000)


    def construct_message(self, fcode, message):
        l = len(message)
        c = sum(message, 0)
        msg = bytearray([0x7b] + fcode + [l, c] + message + [0x7d])
        print(msg)
        return msg

    def decode(msg):
        if msg is None:
           return None
        l = msg[3]
        values = []
        for v in range(l/5):
            values.append((msg[5 + v * 5 +1] + msg[5 + v * 5 +2], msg[5 + v * 5 +3] << 8 + msg[5 + v * 5 +4]))

#    def subscribe(self, values, interval=10):
#        self.send_message(self.construct_message([0x4d, 0x43], [interval] + sum([[0x08, 0x00, v] for v in values], [])))

    def subscribe(self, interval=10):
        values = sum([[loc.address, v.to_bytes(2)] for loc in self.device.locations for v in loc.values], [])
        self.send_message(self.construct_message([0x4d, 0x43], [interval] + values))

    def unsubscribe(self):
        self.send_message(self.construct_message([0x4d, 0x45], []))

    def send_message(self, message):
        self.uart.write(message)
    
    def get_next(self):
        msg = self.uart.read()
        print(msg)
        values = self.sh20.decode(msg)
        print(values)
        return values

class Server():
    def __init__(self, sh20):
        self.wsMod = MicroWebSrv2.LoadModule('WebSockets')
        self.wsMod.OnWebSocketAccepted = lambda mws2, ws: self.OnWebSocketAccepted(mws2, ws)

        #self.pyhtmlTemplateMod = MicroWebSrv2.LoadModule('PyhtmlTemplate')
        #self.pyhtmlTemplateMod.ShowDebug = True

        self.mws2=MicroWebSrv2()
        self.mws2.SetEmbeddedConfig()

        self.sh20 = sh20
        self.valueWebSock = None

    def OnWebSocketAccepted(self, microWebSrv2, webSocket) :
        print('New WebSocket accepted from %s:%s.' % webSocket.Request.UserAddress)
        print("Subscribing")
        self.sh20.connect()
        self.sh20.subscribe([0x0c, 0x0b, 0x0a, 0x0d])
        self.valueWebSock = webSocket

    def start(self):
        self.mws2.StartManaged()
        print("Webserver started")

    def read_and_send(self):
        msg = self.sh20.get_next()
        if self.valueWebSock is not None:
            self.valueWebSock.SendTextMessage("Test")

    def stop(self):
       self.mws2.Stop()


#@WebRoute(GET, '/')
#def loadRoot(mws2, req):
#    req.Response.ReturnRedirect("index.pyhtml")


server = Server(SH20Uart())
server.start()

try:
  while True:
    server.read_and_send()
    time.sleep(5)
except OSError as e:
  machine.reset()
except KeyboardInterrupt:
  server.stop()

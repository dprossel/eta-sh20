# Complete project details at https://RandomNerdTutorials.comimport timeimport ubinasciiimport machineimport micropythonimport networkimport syssys.path.append(".")import espesp.osdebug(None)import gcgc.collect()ssid = 'WLAN-Office'password = '20Kartoffelkaefer06'station = network.WLAN(network.STA_IF)station.active(True)station.connect(ssid, password)count = 0while station.isconnected() == False:    time.sleep(1)    count += 1    if count == 5:        print("Could not connect to Wifi")        print("Resetting")        machine.reset()if station.isconnected():    print('Wifi connection successful')    print(station.ifconfig())
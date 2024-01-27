# Reading ETA-SH20
Inspired by: http://ulrich-franzke.de/haustechnik/eta_programm1.html

# Files
- boot.py: Executed at startup of ESP32
- main.py: main file to start WebServer and connect to SH20
- index.html: Website to display values
- main.js: Javascript to update values on website
- values.json: Names and registers of values to be read

# TODO
- Add remaining values
- Send commands to SH20
- Send Email, if heating shuts down 
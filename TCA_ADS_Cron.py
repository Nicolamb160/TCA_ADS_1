import time




import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_tca9548a
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
import json

THINGSBOARD_HOST = 'digitalconstruction.cloud'
ACCESS_TOKEN = 's3zt6DTcU4fHcMG7tT8j'

# Data capture and upload interval in seconds.
#INTERVAL=30


sensor_data = {'strain': 0, 'volt': 0}
next_reading = time.time()

client = mqtt.Client()

# Set access token
client.username_pw_set(ACCESS_TOKEN)

# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1884, 60)

client.loop_start()
# Create I2C bus as normal
i2c = board.I2C()  # uses board.SCL and board.SDA

# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c, address=0X70)

#for channel in range(8):
    #if tca[channel].try_lock():
        #print("Channel {}:".format(channel), end="")
        #addresses = tca[channel].scan()
        #print([hex(address) for address in addresses if address != 0x70])

# Create the ADC object using the I2C bus
# ads = ADS.ADS1115(i2c)
# you can specify an I2C adress instead of the default 0x48
# ads1 = ADS.ADS1115(i2c, address=0x48)
 # si addresse ==0x48 :
                    #ads1 = ADS.ADS1115()
# For each sensor, create it using the TCA9548A channel instead of the I2C object
ads = []
chan = []
u = []
for channel in range(4):
    if tca[channel].try_lock():
        print("Channel {}:".format(channel), end  ='')
        addresses = tca[channel].scan()
        print([hex(address) for address in addresses if address != 0x70])
        tca[channel].unlock()
        myads = ADS.ADS1115(tca[channel])
        ads.append(myads)
        chan.append(AnalogIn(myads, ADS.P2, ADS.P3))
        u.append(AnalogIn(myads, ADS.P0, ADS.P1))




# print("{:>5}\t{:>5}".format("chan raw", "v"))

# while True:
   # print("0","{:>5}\t{:>5.3f}".format(chan0.value, chan0.voltage))
   # print("1","{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage))
   # time.sleep(1)

# The ADS1015 and ADS1115 both have the same gain options.
#
#       GAIN    RANGE (V)
#       ----    ---------
#        2/3    +/- 6.144
#          1    +/- 4.096
#          2    +/- 2.048
#          4    +/- 1.024
#          8    +/- 0.512
#         16    +/- 0.256
#
gains = (2 / 3, 1, 2, 4, 8, 16)

#while True:
strain= []

N=50

for channel in range(4):
    #if tca[channel].try_lock():
    strain = 0
    for i in range(N):
        ads[channel].gain = 16
        dv = chan[channel].voltage
        ads[channel].gain = 1
        v = u[channel].voltage
        strain += dv/v*1e6*4/2.1
    print(u"{:>5}\t{:>5.3f}\t{:>5.3f}".format(dv, v, strain))
    #    tca[channel].unlock()
    sensor_data['strain%d' % channel] = strain



# Sending humidity and temperature data to ThingsBoard
client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)

#next_reading += INTERVAL
sleep_time = next_reading-time.time()
if sleep_time > 0:
    time.sleep(sleep_time)

#except KeyboardInterrupt:
    #pass

client.loop_stop()
client.disconnect()
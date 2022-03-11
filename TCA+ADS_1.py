# This example shows using two TSL2491 light sensors attached to TCA9548A channels 0 and 1.
# Use with other I2C sensors would be similar.
import time
import board
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_tca9548a

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
ads1 = ADS.ADS1115(tca[0])
ads2 = ADS.ADS1115(tca[1])
ads3 = ADS.ADS1115(tca[2])
ads4 = ADS.ADS1115(tca[3])


# Create differential input between channel 2 and 3
chan0 = AnalogIn(ads1, ADS.P2, ADS.P3)
chan1 = AnalogIn(ads2, ADS.P2, ADS.P3)
chan2 = AnalogIn(ads3, ADS.P2, ADS.P3)
chan3 = AnalogIn(ads4, ADS.P2, ADS.P3)

print("{:>5}\t{:>5}".format("chan raw", "v"))


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

while True:
    ads1.gain = gains[5]
    ads2.gain = gains[5]
    ads3.gain = gains[5]
    ads4.gain = gains[5]
    print("0","{:>5}\t{:>5.3f}".format(chan0.value, chan0.voltage))
    print("1","{:>5}\t{:>5.3f}".format(chan1.value, chan1.voltage))
    print("0","{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage))
    print("1","{:>5}\t{:>5.3f}".format(chan3.value, chan3.voltage))
    time.sleep(1)
tca[channel].unlock()

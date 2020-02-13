# Importing all the neccesary modules
from sense_hat import SenseHat
import os
import time
import logging
import ephem

sense = SenseHat()

# Data for the ephem module so we can find the height of the ISS
name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   20041.12826888  .00000636  00000-0  19647-4 0  9996"
line2 =  "2 25544  51.6446 262.0895 0004888 248.3633 259.5861 15.49151660212163"

# Logging module configuration:
logging.basicConfig(filename='data01.csv', level=logging.DEBUG,
                    format='%(asctime)s, %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

#Header: 
logging.info('Temp (from H),Temp(from P),Avrage Temp,Humid,Pres,ISS Heigth(m),Accelelerometer(x),Accelelerometer(y),Accelelerometer(z),Gyroscope(x),Gyroscope(y),Gyroscope(z)') 
# **********************************

# Time setup:
time_at_start = time.time()  # Time at start
max_time = 9500  # Maximum running time
delay_intre_afisari = 5  # Delay between showing data on the matrix

# All the colours:
x = [0, 0, 0]  # Blank - for the flag
y = [255, 255, 0]  # Yellow - for the flag and text
b = [0, 0, 255]  # Blue - for the flag and text
r = [255, 0, 0]  # Red - for the flag
g = [0, 255, 0]  # Green - for some text
opb = [255, 255, 0] # Opposite of blue
bg = [69, 124, 173] # Background
txt = [255, 221, 85] # Text colour


def steag(nr_afisari, delay):
    """
    :param nr_afisari: How many times should the flag wave
    :param delay: Delay between the waves

    This function shows the flag right at the begggining.
    """
    stg_sus = [r, r, r, x, x, b, b, b,
               r, r, r, y, y, b, b, b,
               r, r, r, y, y, b, b, b,
               r, r, r, y, y, b, b, b,
               r, r, r, y, y, b, b, b,
               r, r, r, y, y, b, b, b,
               r, r, r, y, y, b, b, b,
               x, x, x, y, y, x, x, x]

    stg_jos = [x, x, x, y, y, x, x, x,
               r, r, r, y, y, b, b, b,
               r, r, r, y, y, b, b, b,
               r, r, r, y, y, b, b, b,
               r, r, r, y, y, b, b, b,
               r, r, r, y, y, b, b, b,
               r, r, r, y, y, b, b, b,
               r, r, r, x, x, b, b, b]

    # Lowering of the flag
    j = 0  # Lines
    brk = 0  # Counter

    while brk < 8:
        sense.set_pixel(0, j, r)
        sense.set_pixel(1, j, r)
        sense.set_pixel(2, j, r)
        sense.set_pixel(3, j, y)
        sense.set_pixel(4, j, y)
        sense.set_pixel(5, j, b)
        sense.set_pixel(6, j, b)
        sense.set_pixel(7, j, b)

        j += 1
        brk += 1
        time.sleep(delay)

    time.sleep(delay)

    afisari = 0  # Moving flag
    while afisari < nr_afisari:
        afisari += 1
        sense.set_pixels(stg_jos)
        time.sleep(delay)
        sense.set_pixels(stg_sus)
        time.sleep(delay)


def get_show_data(scrl_spd, col_t, col_h, col_p, bk_t, bk_h, bk_p):
    """
    :param scrl_spd: Speed of the scrolling text
    :param col_t: Text colour for the temperature
    :param col_h: Text colour for the humidity
    :param col_p: Text colour for the pressure
    :param bk_t: Background colour for the temperature
    :param bk_h: Background colour for the humidity
    :param bk_p: Background colour for the pressure

       This is our function for collecting the data from the sensors,
    and also showing it on the LED Matrix.
    """
    # Getting the data
    t1 = round(sense.get_temperature_from_humidity())
    t2 = round(sense.get_temperature_from_pressure())
    t3 = int((t1 + t2) / 2)
    h = round(sense.get_humidity())
    p = round(sense.get_pressure())

    # Showing it on the matrix
    sense.show_message("Temp=" + str(t3) + "C", scroll_speed=scrl_spd, text_colour=col_t, back_colour=bk_t)
    sense.show_message("Humi=" + str(h) + "%", scroll_speed=scrl_spd, text_colour=col_h, back_colour=bk_h)
    sense.show_message("Pres=" + str(p) + "hPa", scroll_speed=scrl_spd, text_colour=col_p, back_colour=bk_p)
    
    # And clearing the matrix
    sense.clear()
    

def logger():
    """
        This function is saving the relevant data in the data01.csv file
    and it also gets the height of the ISS. 
    """
    # Sensors:
    t1 = round(sense.get_temperature_from_humidity())
    t2 = round(sense.get_temperature_from_pressure())
    t3 = int((t1 + t2) / 2)
    h = round(sense.get_humidity())
    p = round(sense.get_pressure())
    
    # ISS Height:
    sat = ephem.readtle(name, line1, line2)
    g = ephem.Observer()
    sat.compute(g)
    ISS_Height = sat.elevation
    
    # Accelerometer:
    raw = sense.get_accelerometer_raw()
    
    # Gyroscope:
    gyro = sense.get_gyroscope()
    
    logging.info( str(t1) + ',' + str(t2) + ',' + str(t3) + ',' + str(h) + ',' + str(p) + ','
                 + str(round(ISS_Height))
                 +',' + "{x},{y},{z}".format(**raw)
                 + ',' +"{pitch},{roll},{yaw}".format(**gyro) )


"""*********************
*********TO_RUN*********
*********************"""

steag(3, 0.5)  # Lowering of the flag

while (time.time() - time_at_start - delay_intre_afisari - 10) < max_time:
    # Making sure we stop the code in our 3 hours
    
    get_show_data(0.1, txt, txt, txt, bg, bg, bg)
    
    logger()
    
    time.sleep(delay_intre_afisari)


#end

from sense_hat import SenseHat
import os
import time
import logging
import logzero
from logzero import logger

sense = SenseHat()

"""
TODO:
  Accelerometru?
  Forta gravitationala?
  Inaltimea la care e?
    -> De adaugat astea la log

  -> Documentatie facuta cum trebe
    - Apoi cu Sphynx

  Pt final:
    Nume fisier <- main.py
    Toate log-urile sa fie data01.csv, data02.csv...
    Timpul max in care poate rula!
"""

# --------
sense.set_rotation(270)  # Sa fie verical pe Pi
# --------

# Pentru datalog
file_path = os.path.dirname(os.path.realpath(__file__))
logzero.logfile(file_path + "/data01.csv")

# TODO: Sa vedem daca schimbam ceva! <- Cod ciordit din tutorial!
# Set a custom formatter
formatter = logging.Formatter('%(name)s - %(asctime)-15s - %(levelname)s: %(message)s')
logzero.formatter(formatter)
# **********************************

# Valori pt timp;
time_at_start = time.time()  # Timpul initial la rulare
max_time = 60  # TODO: Cat trebuie sa ruleze?
delay_intre_afisari = 5  # Cate sec asteptam intre afisari?

# Globale
global t
global h
global p

x = [0, 0, 0]  # Blank - for the flag
y = [255, 255, 0]  # Yellow - for the flag and text
b = [0, 0, 255]  # Blue - for the flag and text
r = [255, 0, 0]  # Red - for the flag
g = [0, 255, 0]  # Green - for some text


def steag(nr_afisari, delay):
    """
    :param nr_afisari: de cate ori sa faca steagul sus-jos
    :param delay: cat timp sa stea intre etape

    TODO: Actual documentatie(si mai apoi cu Sphynx)
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

    # Coborare steag
    j = 0  # Linii
    brk = 0  # Cea mai ok varinata care am gasit-o

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

    afisari = 0  # Afisare streag miscator
    while afisari < nr_afisari:
        afisari += 1
        sense.set_pixels(stg_jos)
        time.sleep(delay)
        sense.set_pixels(stg_sus)
        time.sleep(delay)


def get_show_data(scrl_spd, col_t, col_h, col_p):
    """
    :param scrl_spd: Viteza de scroll pt text
    :param col_t: Culoarea textului pt temperatura
    :param col_h: Culoarea textului pt umiditate
    :param col_p: Culoarea textului pt presiune

    TODO: Actual documentatie(si mai apoi cu Sphynx)
    """
    t = round(sense.get_temperature())
    h = round(sense.get_humidity())
    p = round(sense.get_pressure())

    sense.show_message("Temp=" + str(t) + "C", scroll_speed=scrl_spd, text_colour=col_t)
    sense.show_message("Humi=" + str(h) + "%", scroll_speed=scrl_spd, text_colour=col_h)
    sense.show_message("Pres=" + str(p) + "hPa", scroll_speed=scrl_spd, text_colour=col_p)


def logging():
    """
      All this function does is to save the relevant data in the data01.csv file

      TODO: Date de la accelerometru si chestii
    """
    logger.info("%s,%s", str(t), str(h), str(p))


"""*********************
*********Rulare*********
*********************"""

steag(3, 0.5)  # Coborarea steagului

while (time.time() - time_at_start - delay_intre_afisari - 10) < max_time:
    # Ca sa fim 100% siguri ca se opreste singur
    get_show_data(0.1, g, b, y)
    logging()
    time.sleep(delay_intre_afisari)

# end

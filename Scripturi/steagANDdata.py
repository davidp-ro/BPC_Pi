from sense_hat import SenseHat
import time

sense = SenseHat()

# --------
sense.set_rotation(270)  # Sa fie verical pe emulator
# --------

# Globale
global t
global h
global p

x = [0, 0, 0]
y = [255, 255, 0]
b = [0, 0, 255]
r = [255, 0, 0]
g = [0, 255, 0]


def steag(nr_afisari, delay):
    """
    :param nr_afisari: de cate ori sa faca steagul sus-jos
    :param delay: cat timp sa stea intre etape
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
    """
    t = round(sense.get_temperature())
    h = round(sense.get_humidity())
    p = round(sense.get_pressure())

    sense.show_message("Temp=" + str(t) + "C", scroll_speed=scrl_spd, text_colour=col_t)
    sense.show_message("Humi=" + str(h) + "%", scroll_speed=scrl_spd, text_colour=col_h)
    sense.show_message("Pres=" + str(p) + "hPa", scroll_speed=scrl_spd, text_colour=col_p)


"""*********************
*********Rulare*********
*********************"""
steag(3, 0.5)
get_show_data(0.1, g, b, y)

# end

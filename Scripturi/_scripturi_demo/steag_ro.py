from sense_emu import SenseHat
sense = SenseHat()

r=[255, 0, 0]
y=[240, 230, 5]
b=[0, 0, 255]

flag_ro = [
    r, r, r, y, y, b, b, b,
    r, r, r, y, y, b, b, b,
    r, r, r, y, y, b, b, b,
    r, r, r, y, y, b, b, b,
    r, r, r, y, y, b, b, b,
    r, r, r, y, y, b, b, b,
    r, r, r, y, y, b, b, b,
    r, r, r, y, y, b, b, b]

sense.set_pixels(flag_ro)
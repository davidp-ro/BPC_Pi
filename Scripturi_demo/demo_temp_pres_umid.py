import time
from sense_emu import SenseHat
sense = SenseHat()

while True:
    #Temperatura
    t1 = sense.get_temperature_from_humidity()
    t2 = sense.get_temperature_from_pressure()
    t = (t1+t2)/2
    t = round(t)

    #Umiditate
    h = sense.get_humidity()
    h = round(h)

    #Presiune
    p = sense.get_pressure()
    p = round(p)

    print("************")
    print("Temp:")
    print(t)
    print("Umid:")
    print(h)
    print("Pres:")
    print(p)
    print("************")
    time.sleep(3)
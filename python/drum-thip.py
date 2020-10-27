from practicum import find_mcu_boards, McuBoard, PeriBoard
from time import sleep
import pygame

devs = find_mcu_boards()
pygame.mixer.init()

sd = pygame.mixer.Sound("./sound/sd.wav")
chh = pygame.mixer.Sound("./sound/chh.wav")
ohh = pygame.mixer.Sound("./sound/ohh.wav")
c = pygame.mixer.Sound("./sound/c.wav")
t = pygame.mixer.Sound("./sound/mt.wav")
r = pygame.mixer.Sound("./sound/r.wav")
fts = pygame.mixer.Sound("./sound/ft.wav")
bd = pygame.mixer.Sound("./sound/bd.wav")


if len(devs) == 0:
    print("*** No practicum board found.")
    exit(1)

mcu = McuBoard(devs[0])
print("*** Practicum board found")
print("*** Manufacturer: %s" % \
        mcu.handle.getString(mcu.device.iManufacturer, 256))
print("*** Product: %s" % \
        mcu.handle.getString(mcu.device.iProduct, 256))
peri = PeriBoard(mcu)

while True:
    snare = peri.get_snare()
    hihat = peri.get_hihat()
    crash = peri.get_crash()
    tom = peri.get_tom()
    ride = peri.get_ride()
    ft = peri.get_ft()
    lf = peri.get_lf()
    rf = peri.get_rf()

    if snare > 500:
        print("Snare Hit!!!     | value: %d" % (snare))
        sd.set_volume((snare-500)/1023)
        sd.play()
    
    if hihat > 500:
        print("Hihat Hit!!!     | value: %d" % (hihat))
        if lf == True:
            chh.set_volume((hihat-500)/500)
            chh.play()
        else:
            ohh.set_volume((hihat-500)/1023)
            ohh.play()

    if crash > 500:
        print("Crash Hit!!!     | value: %d" % (crash))
        c.set_volume((crash-500)/1023)
        c.play()

    if tom > 300:
        print("Tom Hit!!!       | value: %d" % (tom))
        t.set_volume((tom-500)/1023)
        t.play()

    if ride > 500:
        print("Ride Hit!!!      | value: %d" % (ride))
        r.set_volume((ride)/1023)
        r.play()

    if ft > 200:
        print("Floor Tom Hit!!! | value: %d" % (ft))
        fts.set_volume((ft-500)/1023)
        fts.play()

    if rf == True:
        bd.set_volume(1.0)
        bd.play()

    sleep(0.01)
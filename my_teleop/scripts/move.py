import rospy
from std_msgs.msg import String

from tkinter import *

WIDTH = 150
HEIGHT = 200

root = Tk()
cnv = Label(root, text = 'Saisi commande clavier')
cnv.pack()
cnv.focus_set()

SIDE = 30
UNIT = 2

# rect = cnv.create_rectangle(
#     (WIDTH / 2 - SIDE / 2, HEIGHT / 2 - SIDE / 2),
#     (WIDTH / 2 + SIDE / 2, HEIGHT / 2 + SIDE / 2), fill="black")

def handler():
    unit = UNIT
    global keys
    #print("entrée handler")
    if sum(keys.values()) > 1:
        unit = UNIT/1.5

    test = False
    for key in drn:
        #print("entrée test")
        if keys[key]:
            if keys["Up"] == True:
                test = True
            elif keys["Right"] == True:
                test = True
            elif keys["Left"] == True:
                test = True
            elif keys["Down"] == True:
                test = True
			elif keys["x"] == True
				test = True
			elif keys["y"] == True:
				test = True
			elif keys["z"] == True:
				test = True

    if test == True:
        print("entrée mvt")
        for key in drn:
            if keys[key]:
                if key == "Up":
                #    cnv.move(rect, 0, -unit)
					print('')
                elif key == "Right":
					gt = 1
                #    cnv.move(rect, unit, 0)
                elif key == "Left":
					gt = 1
                #    cnv.move(rect, -unit, 0)
                elif key == "Down":
					gt = 1
                #    cnv.move(rect, 0, unit)
    root.after(5, handler)


def press(event):
    global keys
    print("touche enfoncée", event.keysym)
    keys[event.keysym] = True


def release(event):
    global keys
    print("touche relâchée", event.keysym)
    keys[event.keysym] = False


drn = ["Up", "Right", "Left", "Down", "x", "y", "z"]
keys = dict.fromkeys(drn, False)
#print(keys)

for key in drn:
    cnv.bind("<KeyPress-%s>" % key, press)
    cnv.bind("<KeyRelease-%s>" % key, release)

handler()

root.mainloop()
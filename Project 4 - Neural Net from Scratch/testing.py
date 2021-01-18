import keyboard

def pressed():
    if keyboard.is_pressed("Up"):
        return True

while True:
    print(pressed())

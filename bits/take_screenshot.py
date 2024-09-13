import keyboard
from PIL import ImageGrab

i = 0

def screenshot():
    """ Take a screenshot and save it """
    global i
    img = ImageGrab.grab()
    img.save(f"screenshot_{i}.png")
    i += 1
    print(f"Screenshot {i} taken")

# When the key 'i' is pressed, call the screenshot function
keyboard.on_press_key('i', lambda _: screenshot())

# Keep processing key events until the key 'e' is pressed
keyboard.wait('e')

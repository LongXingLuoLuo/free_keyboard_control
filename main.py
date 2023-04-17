import pyautogui
import pynput.keyboard

src_path = r'./images'

screenShootKey = pynput.keyboard.Key.f8


def on_press(key):
    if key == screenShootKey:
        x1, y1 = pyautogui.position()

        def on_press2(Key2):
            if Key2 == screenShootKey:
                x2, y2 = pyautogui.position()
                startX = x1 if x1 < x2 else x2
                startY = y1 if y1 < y2 else y2
                width = abs(x1 - x2)
                height = abs(y1 - y2)
                pyautogui.screenshot(src_path + r'/' + '1.png', region=(startX, startY, width, height))
                return False

        # noinspection PyTypeChecker
        with pynput.keyboard.Listener(on_press=on_press2) as listener:
            listener.join()


def position():
    pass

def screenShootByKey():
    with pynput.keyboard.Listener(on_press=on_press) as listener:
        listener.join()

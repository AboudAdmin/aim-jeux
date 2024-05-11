import cv2
import numpy as np
import pyautogui
import time
import threading
import keyboard
import tkinter as tk
from tkinter import colorchooser

class MasteryConquerAimBot:
    def __init__(self, scan_speed=0.01, click_delay=0.05):
        self.scan_speed = scan_speed
        self.click_delay = click_delay
        self.running = False
        self.enemy_color = None

    def start(self):
        self.running = True
        threading.Thread(target=self._start_bot).start()

    def stop(self):
        self.running = False

    def set_enemy_color(self, color):
        self.enemy_color = color

    def _start_bot(self):
        while self.running:
            if keyboard.is_pressed('x'):
                self._aim()
            time.sleep(0.1)

    def _aim(self):
        while self.running:
            if pyautogui.mouseDown():
                mouse_position = pyautogui.position()
                if self.enemy_color is None:
                    continue
                closest_enemy_position = None
                closest_enemy_distance = float('inf')
                screenshot = pyautogui.screenshot()
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                for x in range(frame.shape[1]):
                    for y in range(frame.shape[0]):
                        pixel_color = frame[y, x]
                        if np.array_equal(pixel_color, self.enemy_color):
                            distance = ((x - mouse_position[0]) ** 2 + (y - mouse_position[1]) ** 2) ** 0.5
                            if distance < closest_enemy_distance:
                                closest_enemy_position = (x, y)
                                closest_enemy_distance = distance
                if closest_enemy_position:
                    pyautogui.moveTo(closest_enemy_position[0], closest_enemy_position[1])
                    pyautogui.click()
                    time.sleep(self.click_delay)
            time.sleep(self.scan_speed)

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("MasteryConquer Aim Bot")
        master.geometry("300x150")

        self.start_button = tk.Button(master, text="بدء", command=self.start_bot)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="إيقاف", command=self.stop_bot)
        self.stop_button.pack()

        self.choose_color_button = tk.Button(master, text="تحديد لون العدو", command=self.choose_color)
        self.choose_color_button.pack()

        self.quit_button = tk.Button(master, text="خروج", command=master.quit)
        self.quit_button.pack()

        self.enemy_color = None


if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()

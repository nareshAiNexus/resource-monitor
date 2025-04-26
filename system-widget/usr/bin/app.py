#!/usr/bin/env python3
import tkinter as tk
import psutil
import threading
import time
import random

# --- Config ---
WIDTH = 260
HEIGHT = 120
UPDATE_INTERVAL = 1  # seconds

# --- Setup GUI ---
root = tk.Tk()
root.title("System Widget")
root.geometry(f"{WIDTH}x{HEIGHT}")
root.configure(bg="white")
root.attributes("-topmost", True)
root.resizable(False, False)

# Optional: Set a transparent icon to hide Tkinter logo
try:
    icon = tk.PhotoImage(file="transparent.png")
    root.iconphoto(False, icon)
except:
    pass

# --- Canvas ---
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white", highlightthickness=0)
canvas.pack()

# === Bars ===
cpu_bar = canvas.create_rectangle(30, 65, 70, 80, fill="deepskyblue", width=0)
ram_bar = canvas.create_rectangle(110, 65, 150, 80, fill="mediumseagreen", width=0)
battery_bar = None  # will be created if laptop

# === Labels Under Bars ===
cpu_label = canvas.create_text(50, 100, text="CPU", fill="black", font=("Comic Sans MS", 10, "bold"))
ram_label = canvas.create_text(130, 100, text="RAM", fill="black", font=("Comic Sans MS", 10, "bold"))
battery_label = canvas.create_text(210, 100, text="", fill="black", font=("Comic Sans MS", 10, "bold"))

# === Top Texts (LEFT aligned) ===
cpu_usage_text = canvas.create_text(10, 10, anchor="w", text="", font=("Comic Sans MS", 9, "bold"), fill="black")
ram_usage_text = canvas.create_text(90, 10, anchor="w", text="", font=("Comic Sans MS", 9, "bold"), fill="black")
battery_usage_text = canvas.create_text(170, 10, anchor="w", text="", font=("Comic Sans MS", 9, "bold"), fill="black")

# === Battery/Desktop Icon on top ===
battery_icon_text = canvas.create_text(210, 40, text="", font=("Comic Sans MS", 16))

# === Update Function ===
def update_stats():
    global battery_bar
    while True:
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        battery = psutil.sensors_battery()

        # Animate CPU and RAM
        cpu_h = int((cpu / 100) * 40)
        ram_h = int((ram / 100) * 40)
        bounce = random.randint(-1, 1)

        canvas.coords(cpu_bar, 30, 80 - cpu_h + bounce, 70, 80)
        canvas.coords(ram_bar, 110, 80 - ram_h + bounce, 150, 80)

        # Update left aligned usage text
        canvas.itemconfig(cpu_usage_text, text=f"⚡ {cpu:.1f}%")
        canvas.itemconfig(ram_usage_text, text=f"🧠 {ram:.1f}%")

        if battery:
            # If laptop, show battery bar
            if not battery_bar:
                battery_bar = canvas.create_rectangle(190, 65, 230, 80, fill="orange", width=0)

            bat_h = int((battery.percent / 100) * 40)
            canvas.coords(battery_bar, 190, 80 - bat_h + bounce, 230, 80)

            fill = "#00C853" if battery.power_plugged else "#FF9100"
            canvas.itemconfig(battery_bar, fill=fill)

            canvas.itemconfig(battery_label, text="BAT")
            canvas.itemconfig(battery_usage_text, text=f"🔋 {battery.percent:.1f}%")

            if battery.power_plugged:
                canvas.itemconfig(battery_icon_text, text="🔌")
            else:
                canvas.itemconfig(battery_icon_text, text="🔋")
        else:
            # If desktop, remove battery bar and show monitor icon
            if battery_bar:
                canvas.delete(battery_bar)
                battery_bar = None
            canvas.itemconfig(battery_label, text="")
            canvas.itemconfig(battery_usage_text, text="")
            canvas.itemconfig(battery_icon_text, text="🖥️")

        time.sleep(UPDATE_INTERVAL)

# === Start Thread ===
threading.Thread(target=update_stats, daemon=True).start()

# === Run GUI ===
root.mainloop()

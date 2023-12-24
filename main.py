import util
import proxy

import threading

from tkinter import *
from tkinter.ttk import OptionMenu
from PIL import ImageTk, Image

from ctypes import windll

already_connected = []
invalid_proxies = []
selected_country = "USA"
connected = False

version = "v1.1.00"

proxy.toggle_proxy(False)

def add_to_taskbar(window):
    hwnd = windll.user32.GetParent(window.winfo_id())

    style = windll.user32.GetWindowLongW(hwnd, -20)
    style = style & ~0x00000080
    style = style | 0x00040000

    windll.user32.SetWindowLongW(hwnd, -20, style)

    window.wm_withdraw()
    window.after(10, lambda: window.wm_deiconify())

def disconnect():
    global connected

    proxy.toggle_proxy(False)

    connect_text.place_configure(x=253)
    connect_text.configure(text="Tap here to connect!", font=("Arial Bold", 16))

    connected = False

    ip_text.configure(text=f"IP: {util.get_ip(None)}")
    connected_text.configure(text=f"Connected: {connected}")

def find_and_connect_to_proxy():
    global already_connected
    global connected

    connect_text.place_configure(x=290)
    connect_text.configure(text="Connecting...", font=("Arial Bold", 16))

    country = util.country_to_code(selected_country)
    timeout = timeout_var.get().replace("ms", "")
    anonymity = anonymity_var.get().lower()
    ssl = ssl_var.get().lower()

    proxies = proxy.scrape_proxies(country, timeout, anonymity, ssl)
    if proxies == []:
        connect_text.place_configure(x=235)
        connect_text.configure(text="Unknown error! Please try again.", font=("Arial Bold", 12))

    for addr in proxies:
        if proxy.check_proxy(addr, int(timeout)) and addr not in already_connected and addr not in invalid_proxies:
            proxy.toggle_proxy(True)
            proxy.set_proxy(addr)

            connect_text.place_configure(x=240)
            connect_text.configure(text="Tap here to disconnect!", font=("Arial Bold", 16))

            connected = True
            try:
                ip_text.configure(text=f"IP: {util.get_ip(addr)}")
            except:
                connected = False
                connect_text.place_configure(x=235)
                connect_text.configure(text="Unknown error! Please try again.", font=("Arial Bold", 12))
            connected_text.configure(text=f"Connected: {connected}")

            already_connected.append(addr)
            break
        else:
            invalid_proxies.append(addr)

def start(event):
    if connected:
        thread = threading.Thread(target=disconnect)
        thread.start()
    else:
        thread = threading.Thread(target=find_and_connect_to_proxy)
        thread.start()

def set_country(text):
    global selected_country
    for widget in window.winfo_children():
        if isinstance(widget, Label):
            if widget.cget("text") == text:
                selected_country = widget.cget("text")
                widget.configure(text=f"{widget.cget('text')} <-")
            else:
                widget.configure(text=f"{widget.cget('text')}".replace(" <-", ""))

def set_usa(event):
    set_country("USA")

def set_ukraine(event):
    set_country("Ukraine")

def set_russia(event):
    set_country("Russia")

def get_title_click(event):
    global title_click_x, title_click_y
    title_click_x = event.x_root
    title_click_y = event.y_root

def move_window(event):
    global title_click_x, title_click_y

    new_pos_x = window.winfo_x() + (event.x_root - title_click_x)
    new_pos_y = window.winfo_y() + (event.y_root - title_click_y)
    window.geometry(f'+{new_pos_x}+{new_pos_y}')
    title_click_x = event.x_root
    title_click_y = event.y_root

def quit(event):
    window.destroy()
    exit()

window = Tk()
window.wm_title(f"AutoProxy {version}")
window.overrideredirect(True)
window.geometry('512x512+100+100')
window.configure(bg="white")
window.iconbitmap("res/icon2.ico")
windll.shell32.SetCurrentProcessExplicitAppUserModelID("a")

titlebar = Frame(bg="#8277ff")
titlebar.place(x=0, y=0, width=512, height=50)

icon = Image.open("res/icon.png")
icon = icon.resize((32, 32))
icon = ImageTk.PhotoImage(icon)

titlebar_icon = Label(image=icon, bg="#8277ff")
titlebar_icon.place(x=2, y=6)

title = Label(text=f"AutoProxy {version}", bg="#8277ff", fg="white", font=("Arial Bold", 24))
title.place(x=50, y=2)

close = Image.open("res/close.png")
close = close.resize((32, 32))
close = ImageTk.PhotoImage(close)

close_icon = Label(image=close, bg="#8277ff")
close_icon.place(x=470, y=6)

welcome = Label(text="Welcome!", bg="white", font=("Arial Bold", 32))
welcome.place(x=256, y=50)

countries_list = Frame(bg="#9b90ff")
countries_list.place(x=0, y=50, width=200, height=512)

usa = Image.open("res/usa.png")
usa = usa.resize((64, 64))
usa = ImageTk.PhotoImage(usa)

usa_icon = Label(image=usa, bg="#9b90ff")
usa_icon.place(x=10, y=60)

usa_text = Label(text="USA <-", bg="#9b90ff", fg="white", font=("Arial Bold", 12))
usa_text.place(x=80, y=78)

ukraine = Image.open("res/ukraine.png")
ukraine = ukraine.resize((85, 85))
ukraine = ImageTk.PhotoImage(ukraine)

ukraine_icon = Label(image=ukraine, bg="#9b90ff")
ukraine_icon.place(x=0, y=130)

ukraine_text = Label(text="Ukraine", bg="#9b90ff", fg="white", font=("Arial Bold", 12))
ukraine_text.place(x=82, y=162)

russia = Image.open("res/russia.png")
russia = russia.resize((85, 85))
russia = ImageTk.PhotoImage(russia)

russia_icon = Label(image=russia, bg="#9b90ff")
russia_icon.place(x=0, y=210)

russia_text = Label(text="Russia", bg="#9b90ff", fg="white", font=("Arial Bold", 12))
russia_text.place(x=82, y=241)

border = Frame(bg="black")
border.place(x=0, y=300, width=200, height=2)

border = Frame(bg="black")
border.place(x=0, y=50, width=512, height=2)

border = Frame(bg="black")
border.place(x=200, y=50, width=2, height=512)

ssls = ["", "All", "Yes", "No"]
anonymities = ["", "All", "Elite", "Anonymous", "Transparent"]
timeouts = ["", "1000ms", "2000ms", "3000ms", "4000ms",
            "5000ms", "6000ms", "7000ms", "8000ms", 
            "9000ms", "10000ms"]

ssl_text = Label(text="SSL: ", bg="#9b90ff", fg="white", font=("Arial Bold", 12))
ssl_text.place(x=10, y=310)

anonymity_text = Label(text="Anonymity: ", bg="#9b90ff", fg="white", font=("Arial Bold", 12))
anonymity_text.place(x=10, y=340)

timeout_text = Label(text="Timeout: ", bg="#9b90ff", fg="white", font=("Arial Bold", 12))
timeout_text.place(x=10, y=370)

ssl_var = StringVar(window)
anonymity_var = StringVar(window)
timeout_var = StringVar(window)

ssl_var.set("All")
anonymity_var.set("All")
timeout_var.set("1000ms")

ssl_menu = OptionMenu(window, ssl_var, *ssls)
ssl_menu.place(x=60, y=310)

anonymity_menu = OptionMenu(window, anonymity_var, *anonymities)
anonymity_menu.place(x=110, y=340)

timeout_menu = OptionMenu(window, timeout_var, *timeouts)
timeout_menu.place(x=90, y=370)

connect_text = Label(text="Tap here to connect!", bg="white", font=("Arial Bold", 16))
connect_text.place(x=253, y=200)

power = Image.open("res/power.png")
power = power.resize((128, 128))
power = ImageTk.PhotoImage(power)

power_icon = Label(image=power, bg="#ffffff")
power_icon.place(x=295, y=250)

connected_text = Label(text=f"Connected: {connected}", bg="white", font=("Arial Bold", 16))
connected_text.place(x=220, y=450)

ip_text = Label(text=f"IP: {util.get_ip(None)}", bg="white", font=("Arial Bold", 16))
ip_text.place(x=220, y=475)

window.bind('<Button-1>', get_title_click)
window.bind('<B1-Motion>', move_window)

close_icon.bind("<Button-1>", quit)

usa_icon.bind("<Button-1>", set_usa)
usa_text.bind("<Button-1>", set_usa)

ukraine_icon.bind("<Button-1>", set_ukraine)
ukraine_text.bind("<Button-1>", set_ukraine)

russia_icon.bind("<Button-1>", set_russia)
russia_text.bind("<Button-1>", set_russia)

power_icon.bind("<Button-1>", start)

window.after(10, lambda: add_to_taskbar(window))
window.mainloop()
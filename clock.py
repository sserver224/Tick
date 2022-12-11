from tkinter import *
from datetime import datetime
from tkinter.ttk import Progressbar
from tk_tools import *
from tkinter import Menu
import pygame
import os
from tkinter import messagebox
from win10toast import ToastNotifier
from winreg import *
pygame.mixer.init()
channel=pygame.mixer.find_channel()
alarmchannel=pygame.mixer.find_channel()
from tkinter.ttk import *
from tkinter import filedialog
from time import sleep
from threading import Thread
import time
import ctypes
def get_resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
def vibrate_on():
    set_vibration(0, clock.vibLevel0, clock.vibLevel1)
def vibrate_off():
    set_vibration(0, 0, 0)
def vibrate():
    n=0
    while n<int(mins)/15:
        vibrate_on()
        sleep(0.25)
        vibrate_off()
        sleep(0.25)
        n+=1
def vibrate_basic_long():
    vibrate_on()
    sleep(2)
    vibrate_off()
    sleep(1)
    if clock.strike:
        n=0
        while n<hour:
            vibrate_on()
            sleep(0.25)
            vibrate_off()
            sleep(0.25)
            n+=1
def vibrate_basic():
    vibrate_on()
    sleep(1)
    vibrate_off()
class XINPUT_VIBRATION(ctypes.Structure):
    _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort),
                ("wRightMotorSpeed", ctypes.c_ushort)]

xinput = ctypes.windll.xinput1_1  # Load Xinput.dll
ConnectRegistry(None, HKEY_CURRENT_USER)
CreateKeyEx(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver\Tick', reserved=0)
# Set up function argument types and return type
XInputSetState = xinput.XInputSetState
XInputSetState.argtypes = [ctypes.c_uint, ctypes.POINTER(XINPUT_VIBRATION)]
XInputSetState.restype = ctypes.c_uint
toaster = ToastNotifier()
# You can also create a helper function like this:
def set_vibration(controller, left_motor, right_motor):
    vibration = XINPUT_VIBRATION(int(left_motor * 65535), int(right_motor * 65535))
    XInputSetState(controller, ctypes.byref(vibration))
clock=Tk()
hour=0
secs=0
readFailed=False
try:
    if QueryValueEx(OpenKey(OpenKey(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver', reserved=0, access=KEY_ALL_ACCESS), 'Tick', reserved=0, access=KEY_ALL_ACCESS), 'BarMode')[0]==1:
        clock.barmode=True
    else:
        clock.barmode=False
except:
    clock.barmode=False
    readFailed=True
mins=0
try:
    if QueryValueEx(OpenKey(OpenKey(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver', reserved=0, access=KEY_ALL_ACCESS), 'Tick', reserved=0, access=KEY_ALL_ACCESS), 'Notify')[0]==1:
        clock.notify=True
    else:
        clock.notify=False
except:
    clock.notify=False
    readFailed=True
try:
    clock.vibLevel0=int(QueryValueEx(OpenKey(OpenKey(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver', reserved=0, access=KEY_ALL_ACCESS), 'Tick', reserved=0, access=KEY_ALL_ACCESS), 'VibLevel0')[0])/100
except:
    clock.vibLevel0=0
    readFailed=True
try:
    clock.vibLevel1=int(QueryValueEx(OpenKey(OpenKey(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver', reserved=0, access=KEY_ALL_ACCESS), 'Tick', reserved=0, access=KEY_ALL_ACCESS), 'VibLevel1')[0])/100
except:
    clock.vibLevel1=0.67
    readFailed=True
try:
    if QueryValueEx(OpenKey(OpenKey(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver', reserved=0, access=KEY_ALL_ACCESS), 'Tick', reserved=0, access=KEY_ALL_ACCESS), 'StrikeHours')[0]==1:
        clock.strike=True
    else:
        clock.strike=False
except:
    clock.strike=True
    readFailed=True
if readFailed:
    error=Thread(target=lambda x: showerror('Options Read Error','One or more registry reads have failed. Setting errors to default...'))
    error.daemon=True
    error.start()
clock.settingalarm=False
def play_chime(n):
    if channel.get_busy()==False and clock.chime.get()>0:
        try:
            channel.play(pygame.mixer.Sound(get_resource_path(str(n)+'.wav')))
        except FileNotFoundError:
            messagebox.showerror('Error', 'File '+str(clock.chime.get())+'.wav cannot be found.')
def set_alarm():
    errorLabel.config(text='')
    if not clock.settingalarm:
        clock.settingalarm=True
        clock.alarm.set(0)
        hourEntry.config(state='readonly')
        minuteEntry.config(state='readonly')
        offButton.config(state=DISABLED)
        onButton.config(state=DISABLED)
    else:
        if hourEntry.get()=='' or minuteEntry.get()=='':
            errorLabel.config(text='Error: Blank values!')
        else:
            clock.settingalarm=False
            clock.alarmhour=int(hourEntry.get())
            clock.alarmmins=int(minuteEntry.get())
            hourEntry.config(state=DISABLED)
            minuteEntry.config(state=DISABLED)
            offButton.config(state=NORMAL)
            onButton.config(state=NORMAL)
def stop_alarm():
    vibrate_off()
    alarmchannel.stop()
    setButton.config(text='Set Alarm', command=set_alarm)
clock.config(bg='black')
clock.resizable(False, False)
clock.title('Tick v2.1 ©sserver')
day_percent=DoubleVar()
hourLabel=SevenSegmentDigits(clock, background='black', digit_color='#00ff00', height=100, digits=2)
hourLabel.grid(column=1, row=1)
colon1=Label(clock, text=':', foreground='white', background='black', font=('Century Gothic', 75))
colon1.grid(column=2, row=1)
minuteLabel=SevenSegmentDigits(clock, background='black', digit_color='#00ff00', height=100, digits=2)
minuteLabel.grid(column=3, row=1)
colon2=Label(clock, text=':', foreground='white', background='black', font=('Century Gothic', 75))
colon2.grid(column=4, row=1)
secondLabel=SevenSegmentDigits(clock, background='black', digit_color='#00ff00', height=100, digits=2)
secondLabel.grid(column=5, row=1)
Progressbar(clock, mode='determinate', variable=day_percent, length=350).place(x=10, y=130)
clock.chime=IntVar()
clock.alarm=IntVar()
clock.lift()
clock.alarmhour=0
clock.alarmmins=0
Radiobutton(clock, 
               text="Off",
               variable=clock.chime, 
               value=0, command=channel.stop).place(x=20, y=160)
Radiobutton(clock, 
               text="On",
               variable=clock.chime, 
               value=1).place(x=60, y=160)
Radiobutton(clock, 
               text="4x4",
               variable=clock.chime, 
               value=2).place(x=98, y=160)
Label(clock, text='↑Chime Options                                               Alarm Options↓', background='black', foreground='white').place(x=20, y=190)
errorLabel=Label(clock, background='black', foreground='red', text='')
errorLabel.place(x=120,y=190)
clock.mode=False
clock.keepontop=False
clock.geometry('370x250')
playButton=Button(clock, text='Play Chime', command=lambda: play_chime('00'))
offButton=Radiobutton(clock, 
               text="Off",
               variable=clock.alarm, 
               value=0, command=stop_alarm, state=DISABLED)
offButton.place(x=20, y=220)
onButton=Radiobutton(clock, 
               text="On",
               variable=clock.alarm, 
               value=1, state=DISABLED)
onButton.place(x=60, y=220)
setButton=Button(clock, text='Set Alarm', command=set_alarm)
setButton.place(x=260, y=220)
hourEntry=Spinbox(clock, from_=0, to=23, width=10, state=DISABLED)
hourEntry.place(x=100, y=220)
minuteEntry=Spinbox(clock, from_=0, to=59, width=10, state=DISABLED)
minuteEntry.place(x=180, y=220)
playButton.place(x=290, y=160)
clock.options_open=False
def close():
    try:
        if clock.barmode:
            SetValueEx(OpenKey(OpenKey(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver', reserved=0, access=KEY_ALL_ACCESS), 'Tick', reserved=0, access=KEY_ALL_ACCESS), 'BarMode', 0, REG_DWORD, 1)
        else:
            SetValueEx(OpenKey(OpenKey(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver', reserved=0, access=KEY_ALL_ACCESS), 'Tick', reserved=0, access=KEY_ALL_ACCESS), 'BarMode', 0, REG_DWORD, 0)
        if clock.notify:
            SetValueEx(OpenKey(OpenKey(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver', reserved=0, access=KEY_ALL_ACCESS), 'Tick', reserved=0, access=KEY_ALL_ACCESS), 'Notify', 0, REG_DWORD, 1)
        else:
            SetValueEx(OpenKey(OpenKey(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver', reserved=0, access=KEY_ALL_ACCESS), 'Tick', reserved=0, access=KEY_ALL_ACCESS), 'Notify', 0, REG_DWORD, 0)
        if clock.strike:
            SetValueEx(OpenKey(OpenKey(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver', reserved=0, access=KEY_ALL_ACCESS), 'Tick', reserved=0, access=KEY_ALL_ACCESS), 'StrikeHours', 0, REG_DWORD, 1)
        else:
            SetValueEx(OpenKey(OpenKey(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver', reserved=0, access=KEY_ALL_ACCESS), 'Tick', reserved=0, access=KEY_ALL_ACCESS), 'StrikeHours', 0, REG_DWORD, 0)
        SetValueEx(OpenKey(OpenKey(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver', reserved=0, access=KEY_ALL_ACCESS), 'Tick', reserved=0, access=KEY_ALL_ACCESS), 'VibLevel0', 0, REG_DWORD, int(clock.vibLevel0*100))
        SetValueEx(OpenKey(OpenKey(OpenKey(HKEY_CURRENT_USER, 'Software', reserved=0, access=KEY_ALL_ACCESS), 'sserver', reserved=0, access=KEY_ALL_ACCESS), 'Tick', reserved=0, access=KEY_ALL_ACCESS), 'VibLevel1', 0, REG_DWORD, int(clock.vibLevel1*100))
    except Exception as e:
        messagebox.showerror("Save Error", "Your settings won't be saved due to the following error:\n"+str(e)) 
    vibrate_off()
    clock.destroy()
    if clock.options_open:
        clock.options.destroy()
    vibrate_off()
clock.protocol('WM_DELETE_WINDOW', close)
def reset():
    clock.options_open=False
    clock.options.destroy()
def options():
    def update_values():
        if chk.instate(['selected']):
            clock.mode=True
        else:
            clock.mode=False
        if chk1.instate(['selected']):
            clock.keepontop=True
        else:
            clock.keepontop=False
        if chk2.instate(['selected']):
            clock.strike=True
        else:
            clock.strike=False
        if chk3.instate(['selected']):
            clock.notify=True
        else:
            clock.notify=False
    def update_motors(n):
        if str(vibLevel0.get())=='High':
            clock.vibLevel0=1
        elif str(vibLevel0.get())=='Medium':
            clock.vibLevel0=0.67
        elif str(vibLevel0.get())=='Low':
            clock.vibLevel0=0.33
        else:
            clock.vibLevel0=0
        if str(vibLevel1.get())=='High':
            clock.vibLevel1=1
        elif str(vibLevel1.get())=='Medium':
            clock.vibLevel1=0.67
        elif str(vibLevel1.get())=='Low':
            clock.vibLevel1=0.33
        else:
            clock.vibLevel1=0
    def barmode(n):
        if str(rb.get())=='Part of hour':
            clock.barmode=True
        else:
            clock.barmode=False
    if not clock.options_open:
        clock.options=Tk()
        clock.options.title('Options')
        clock.options.attributes('-toolwindow', True)
        chk=Checkbutton(clock.options, command=update_values, text='Show part of day/hour remaining in bar')
        chk.pack()
        chk1=Checkbutton(clock.options, command=update_values, text='Keep on top')
        chk1.pack()
        chk2=Checkbutton(clock.options, command=update_values, text='Strike hours')
        chk2.pack()
        chk3=Checkbutton(clock.options, command=update_values, text='Send a notification when chime or alarm sounds')
        chk3.pack()
        Label(clock.options, text='Controller Vibration Intensity').pack()
        Label(clock.options, text='L Motor').pack()
        vibLevel0=Combobox(clock.options, values=['Off', 'Low', 'Medium', 'High'], state='readonly')
        vibLevel0.pack()
        Label(clock.options, text='R Motor').pack()
        vibLevel1=Combobox(clock.options, values=['Off', 'Low', 'Medium', 'High'], state='readonly')
        vibLevel1.pack()
        Label(clock.options, text='What do you want to show on the progress bar?').pack()
        rb=Combobox(clock.options, values=['Part of day', 'Part of hour'], state='readonly')
        rb.bind("<<ComboboxSelected>>", barmode)
        vibLevel0.bind("<<ComboboxSelected>>", update_motors)
        vibLevel1.bind("<<ComboboxSelected>>", update_motors)
        rb.pack()
        chk.state(['!alternate'])
        if clock.vibLevel0==1:
            vibLevel0.set('High')
        elif clock.vibLevel0==0.67:
            vibLevel0.set('Medium')
        elif clock.vibLevel0==0.33:
            vibLevel0.set('Low')
        elif clock.vibLevel0==0:
            vibLevel0.set('Off')
        else:
            vibLevel0.set('(Custom value)')
        if clock.vibLevel1==1:
            vibLevel1.set('High')
        elif clock.vibLevel1==0.67:
            vibLevel1.set('Medium')
        elif clock.vibLevel1==0.33:
            vibLevel1.set('Low')
        elif clock.vibLevel1==0:
            vibLevel1.set('Off')
        else:
            vibLevel1.set('(Custom value)')
        chk1.state(['!alternate'])
        chk2.state(['!alternate'])
        chk3.state(['!alternate'])
        if clock.mode:
            chk.state(['selected'])
        if clock.keepontop:
            chk1.state(['selected'])
        if clock.iconpresent:
            clock.options.iconbitmap('clock.ico')
        if clock.barmode:
            rb.set('Part of hour')
        else:
            rb.set('Part of day')
        if clock.strike:
            chk2.state(['selected'])
        if clock.notify:
            chk3.state(['selected'])
        clock.options.protocol('WM_DELETE_WINDOW', reset)
        clock.options.resizable(False, False)
        clock.options_open=True
    else:
        clock.options.lift()
Button(clock, text='Options', command=options).place(x=200, y=160)
clock.iconpresent=True
vibrate_off()
try:
    clock.iconbitmap(get_resource_path('clock.ico'))
except:
    messagebox.showerror('Icon Error', 'App icon is missing or corrupt')
    clock.iconpresent=False
while True:
    try:
        d = datetime.now()
        hour = d.strftime("%I")
        hour2=d.strftime('%H')
        mins = d.strftime("%M")
        secs = d.strftime("%S")
        day =  d.strftime("%A")
        part_of_day=d.strftime("%p")
        hourLabel.set_value(hour)
        minuteLabel.set_value(mins)
        secondLabel.set_value(secs)
        clock.update()
        if clock.keepontop:
            clock.call('wm', 'attributes', '.', '-topmost', True)
        else:
            clock.call('wm', 'attributes', '.', '-topmost', False)
        if not clock.barmode:
            if clock.mode:
                day_percent.set(((86400-((int(hour2)*3600+int(mins)*60+int(secs))))/86400)*100)
            else:
                day_percent.set(((int(hour2)*3600+int(mins)*60+int(secs))/86400)*100)
        else:
            if clock.mode:
                day_percent.set(((3600-(int(mins)*60+int(secs)))/3600)*100)
            else:
                day_percent.set(((int(mins)*60+int(secs)))/3600*100)
        if clock.alarm.get()==1 and (int(mins)==clock.alarmmins and int(hour2)==clock.alarmhour and secs=='00') and (not alarmchannel.get_busy()):
            try:
                alarmchannel.play(pygame.mixer.Sound(get_resource_path('alarm.wav')), -1)
                if clock.notify:
                    toaster.show_toast("Clock Alarm", "Alarm at "+hour2+':'+mins, icon_path=None, duration=5, threaded=True)
                setButton.config(text='Stop Alarm', command=stop_alarm)
                vibrate_on()
            except:
                messagebox.showerror('Error', 'File alarm.wav cannot be found.')
        if mins=='00' and secs=='00' and clock.chime.get()>0:
            if clock.strike:
                play_chime(hour)
            else:
                play_chime('00')
            if clock.notify:
                toaster.show_toast("Clock Chime", "It's "+hour+':'+mins, icon_path=None, duration=5, threaded=True)
            w=Thread(target=vibrate_basic_long)
            w.daemon=True
            w.start()
        elif (int(mins))%15==0 and secs=='00' and clock.chime.get()>0:
            if clock.chime.get()==2:
                play_chime(mins)
                if clock.notify:
                    toaster.show_toast("Clock Chime", "It's "+hour+':'+mins, icon_path=None, duration=5, threaded=True)
                w=Thread(target=vibrate)
                w.daemon=True
                w.start()
        time.sleep(0.01)
    except:
        break

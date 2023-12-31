import ctypes
from genericpath import getsize
import pprint
import shutil
from sys import getsizeof
import time
from urllib import request
from numpy import equal
import pyttsx3
import requests #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib
import platform
import psutil
import GPUtil
import pyjokes

import requests

import flappy as f
import snake as s
  
# initializing URL

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)

assname = ('Lucy')

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
        speak("i wish you a very good day ahead")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")  
        speak("hope you are having a great day") 

    else:
        speak("Good Evening!")  
        speak("hope you had a great day")

    assname = ('Lucy')
    speak("Lucy your personal assistance")   
    url = "https://www.google.com"
    timeout = 10
    try:
        # requesting URL
        request = requests.get(url, timeout=timeout)
        #print("Internet is on")
  
    # catching exception
    except (requests.ConnectionError, requests.Timeout) as exception:
        speak("No network Connected")    
        #speak(assname)

def username():
    speak("What should i call you sir")
    query = takeCommand().lower()
    query1 = query.replace("Call me","")
    #uname = takeCommand()
    speak("Welcome Mister")
    speak(query1)
    columns = shutil.get_terminal_size().columns
    print("#####################".center(columns))
    print("Welcome Mr.", query1.center(columns))
    print("#####################".center(columns))
    speak("How can i Help you, Sir")

def takeCommand():
    
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language ='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
        return "None"
    
    return query

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()

def system():
    speak("="*40, "System Information", "="*40)
    uname = platform.uname()
    speak(f"System: {uname.system}")
    speak(f"Node Name: {uname.node}")
    speak(f"Release: {uname.release}")
    speak(f"Version: {uname.version}")
    speak(f"Machine: {uname.machine}")
    speak(f"Processor: {uname.processor}")

def boot():
    speak("="*40, "Boot Time", "="*40)
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    speak(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

def news():
    import requests
    newsapi_key = "e411342a09aa45b79cf8e314b96a68cd"
    url=f"https://newsapi.org/v2/everything?q=Apple&from=2022-04-14&sortBy=popularity&apiKey={newsapi_key}"
    main_page = requests.get(url).json()
    article = main_page["articles"]
    head = []
    speak("Top two Head lines are")
    for ar in article:
        head.append(ar["description"])
    for i in range (2):
        speak(f"{i+1}{head[i]}\n")

def CPU():
    speak("="*40, "CPU Info", "="*40)
# number of cores
    speak("Physical cores:", psutil.cpu_count(logical=False))
    speak("Total cores:", psutil.cpu_count(logical=True))
# CPU frequencies
    cpufreq = psutil.cpu_freq()
    speak(f"Max Frequency: {cpufreq.max:.2f}Mhz")
    speak(f"Min Frequency: {cpufreq.min:.2f}Mhz")
    speak(f"Current Frequency: {cpufreq.current:.2f}Mhz")
# CPU usage
    speak("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        speak(f"Core {i}: {percentage}%")
        speak(f"Total CPU Usage: {psutil.cpu_percent()}%")

def memory():
    # Memory Information
    speak("="*40, "Memory Information", "="*40)
    # get the memory details
    svmem = psutil.virtual_memory()
    speak(f"Total: {get_size(svmem.total)}")
    speak(f"Available: {get_size(svmem.available)}")
    speak(f"Used: {get_size(svmem.used)}")
    speak(f"Percentage: {svmem.percent}%")
    speak("="*20, "SWAP", "="*20)
    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    speak(f"Total: {get_size(swap.total)}")
    speak(f"Free: {get_size(swap.free)}")
    speak(f"Used: {get_size(swap.used)}")
    speak(f"Percentage: {swap.percent}%")

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def disk():
    # Disk Information
    speak("="*40, "Disk Information", "="*40)
    speak("Partitions and Usage:")
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        speak(f"=== Device: {partition.device} ===")
        speak(f"  Mountpoint: {partition.mountpoint}")
        speak(f"  File system type: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
            continue
        speak(f"  Total Size: {getsize(partition_usage.total)}")
        speak(f"  Used: {getsizeof(partition_usage.used)}")
        speak(f"  Free: {get_size(partition_usage.free)}")
        speak(f"  Percentage: {partition_usage.percent}%")
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    speak(f"Total read: {get_size(disk_io.read_bytes)}")
    speak(f"Total write: {get_size(disk_io.write_bytes)}")

def network():
    # Network information
    speak("="*40, "Network Information", "="*40)
    # get all network interfaces (virtual and physical)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            speak(f"=== Interface: {interface_name} ===")
            if str(address.family) == 'AddressFamily.AF_INET':
                speak(f"  IP Address: {address.address}")
                speak(f"  Netmask: {address.netmask}")
                speak(f"  Broadcast IP: {address.broadcast}")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                speak(f"  MAC Address: {address.address}")
                speak(f"  Netmask: {address.netmask}")
                speak(f"  Broadcast MAC: {address.broadcast}")
    # get IO statistics since boot
    net_io = psutil.net_io_counters()
    speak(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
    speak(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")

def gpu():
    import GPUtil
    from tabulate import tabulate
    speak("="*40, "GPU Details", "="*40)
    gpus = GPUtil.getGPUs()
    list_gpus = []
    for gpu in gpus:
    # get the GPU id
        gpu_id = gpu.id
    # name of GPU
        gpu_name = gpu.name
    # get % percentage of GPU usage of that GPU
        gpu_load = f"{gpu.load*100}%"
    # get free memory in MB format
        gpu_free_memory = f"{gpu.memoryFree}MB"
    # get used memory
        gpu_used_memory = f"{gpu.memoryUsed}MB"
    # get total memory
        gpu_total_memory = f"{gpu.memoryTotal}MB"
    # get GPU temperature in Celsius
        gpu_temperature = f"{gpu.temperature} °C"
        gpu_uuid = gpu.uuid
        list_gpus.append((
            gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
            gpu_total_memory, gpu_temperature, gpu_uuid
        ))

    speak(tabulate(list_gpus, headers=("id", "name", "load", "free memory", "used memory", "total memory",
                                   "temperature", "uuid")))

def joke1():
    
    j = pyjokes.get_joke('en', category='neutral')
    print(j)
    speak(j)

def camera():
    import pyautogui
    import cv2
    import numpy as np
  
    # Specify resolution
    resolution = (1920, 1080)
  
    # Specify video codec
    codec = cv2.VideoWriter_fourcc(*"XVID")
  
    # Specify name of Output file
    filename = "Recording.avi"
    
    # Specify frames rate. We can choose any 
    # value and experiment with it
    fps = 60.0
  
  
# Creating a VideoWriter object
    out = cv2.VideoWriter(filename, codec, fps, resolution)
  
# Create an Empty window
    cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
  
# Resize this window
    cv2.resizeWindow("Live", 480, 270)
  
    while True:
    # Take screenshot using PyAutoGUI
        img = pyautogui.screenshot()
  
    # Convert the screenshot to a numpy array
        frame = np.array(img)
  
    # Convert it from BGR(Blue, Green, Red) to
    # RGB(Red, Green, Blue)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  
    # Write it to the output file
        out.write(frame)
      
    # Optional: Display the recording screen
        cv2.imshow('Live', frame)
      
    # Stop recording when we press 'q'
        if cv2.waitKey(1) == ord('q'):
            break
  
# Release the Video writer
    out.release()
  
# Destroy all windows
    cv2.destroyAllWindows()

def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    print(ip_address["ip"])
    speak(ip_address["ip"])
    
def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    ad = res['slip']['advice']
    print(ad)
    speak(ad)

def bluetooth():
    import pyautogui
    pyautogui.click(x=1884, y=1059)
    time.sleep(2)
    pyautogui.click(x=1709, y=612)
    time.sleep(2)
    pyautogui.click(x=1884, y=1059)

def network():
    import pyautogui
    pyautogui.click(x=1669, y=1054)
    time.sleep(2)
    pyautogui.click(x=1533, y=980)
    time.sleep(2)
    pyautogui.click(x=1669, y=1054)

def speed():
    import speedtest
    st = speedtest.Speedtest()
    dw = st.download()
    up = st.upload()
    print(f"download : {dw} Mb")
    print(f"upload : {up} Mb")
    speak(f"download{dw}upload{up}")

def google():
    
    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")
 
    # to search
    query = "Geeksforgeeks"
 
    for j in search(query, tld="co.in", num=10, stop=10, pause=2):
        print(j)

def search1():
    speak("What do you want to search")
    webName = takeCommand()
    speak("Here are the results")
    webbrowser.open(webName)

def send_mail_function():
    from http import server
    speak("ok, what's the message")
    msg = takeCommand()
    ajay = 'ajay3932kamble@gmail.com'
    Ajay = 'ajay3932kamble@gmail.com'
    yash = 'yashpardeshi04.yp@gmail.com'
    Yash = 'yashpardeshi04.yp@gmail.com'
    speak("enter reciever's name")
    nam = takeCommand()
    if nam == ajay or Ajay:
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login('firedetectionproject1@gmail.com', 'Firedetection')
        server.sendmail('firedetectionproject1@gmail.com',ajay, msg)
        speak('Mail sent')
    
    elif nam == yash or Yash:
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login('firedetectionproject1@gmail.com', 'Firedetection')
        server.sendmail('firedetectionproject1@gmail.com',yash, msg)
        speak('Mail sent')

    else:
        speak('please enter valid name, sir')

    

if __name__ == "__main__":
    wishMe()
    username()
    while True:
    # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if 'wikipedia' in query:
            query = query.replace("on wikipedia", "")
           # query = query.replace("wikipedia", "")
            # query = query.replace("search", "")
            speak(f"{query} on wikipedia")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif assname+'open youtube' in query:
            webbrowser.open("https://www.youtube.com/")

        elif 'jarvis open google' in query:
            webbrowser.open("https://www.google.com/")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")   

        elif 'open anime' in query:
            webbrowser.open("https://9anime.vc/watch/kimetsu-no-yaiba-movie-mugen-ressha-hen-15763?ep=67753")

        elif 'play music' in query:
            music_dir = 'E:\Music'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))

        elif "what's the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")  
            print(f"Sir, the time is {strTime}")  
            speak(f"Sir, the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\AJAY\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'how are you' in query:
            print('i am fine sir')
            speak('i am fine sir')
            print('how are you sir')
            speak('how are you sir')
        
        elif 'fine' in query or "good" in query:
            print("It's good to know that your fine")
            speak("It's good to know that your fine")
        
        elif "change my name to" in query:
            query = query.replace("change my name to", "")
            assname = query
        
        elif "change name" in query:
            speak("What would you like to call me, Sir ")
            assname = takeCommand()
            speak("Thanks for naming me")

        elif "what's your name" in query or "What is your name" in query:
            speak("My friends call me")
            speak(assname)
            print("My friends call me", assname)

        elif 'exit' in query:
            speak("Thanks for giving me your time")
            exit()
        
        elif "who made you" in query or "who created you" in query:
            print("I have been created by team 7.")
            speak("I have been created by team 7.")

        elif "wake up lucy" in query:
            speak("i am  "+assname+"  sir, please tell me how may i help you")

        elif "you can sleep now" in query:
            print("okay sir, i am going to sleep you can call me anytime")
            speak("okay sir, i am going to sleep you can call me anytime")

        elif 'lock window' in query:
            speak("locking the device")
            ctypes.windll.user32.LockWorkStation()

        elif "don't listen" in query or "stop listening" in query:
            speak("for how much time you want to stop jarvis from listening commands")
            a = int(takeCommand())
            time.sleep(a)
            print(a)

        elif "system" in query :
            sys = system()
            speak(sys)

        elif "boot" in query :
            bt = boot()
            speak(bt)
        
        elif "cpu" in query:
            cpu = CPU()
            speak(cpu)
        
        elif "disk" in query:
            dk = disk()
            speak(dk)
        
        elif "memory" in query:
            mm = memory()
            speak(mm)
        
        elif "network" in query:
            nt = network()
            speak(nt)

        elif "gpu" in query:
            gp = gpu()
            speak(gp)
        
        elif "open camera" in query:
            cm = camera()
            speak(cm)

        elif "tell me news" in query:
            nw = news()
            speak(nw)

        elif "tell me a joke" in query:
            joke1()

        elif "what is my ip" in query:
            find_my_ip()

        elif "give me a motivation" in query:
            get_random_advice()
        
        elif "check internet speed" in query:
            speed()

        elif "turn on bluetooth" in query:
            bluetooth()
        
        elif "turn on wifi" in query:
            network()
        
        elif "play flappy game" in query:
            f.flappy()

        elif "play snake game" in query:
            s.snake1()

        elif "i want to search" in query:
            search1()

        elif "send mail" in query:
            send_mail_function()
        


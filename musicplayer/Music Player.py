import tkinter
from tkinter import Button
from tkinter import Listbox
from tkinter import Entry
from tkinter import Scale
from tkinter import Label
from tkinter import Toplevel
from pymediainfo import MediaInfo
import re
from mutagen.mp3 import MP3
import json
from tkinter import Message
import threading
import pygame
import requests
import time
import os
import random
import shutil
from tkinter.filedialog import *
from tkinter import StringVar
from fake_useragent import UserAgent
from PIL import Image, ImageTk


top = tkinter.Tk()
top.geometry("1100x400")
top.title("音乐播放器")
ua = UserAgent()
screenwidth = top.winfo_screenwidth()
screenheight = top.winfo_screenheight() - 100

pygame.init()
path='C:/music'
paths = StringVar()
pathn = StringVar()
patht = StringVar()
v = StringVar()
v1 = StringVar()
v2 = StringVar()


def callback():  # 搜索本地文件
    path_ = askopenfilenames(filetypes=[("mp3 file", "*.mp3"),("all","*.*")])
    return path_

def find():
    folder_path = "C:/music"
    folder_list = os.listdir(folder_path)  # 遍历文件夹里面每个文件
    list = []
    count = 0
    for i in folder_list:  # 将文件夹里的文件按顺序传提给变量i  此处区别os.walk()
        if os.path.splitext(i)[1] == '.mp3':  # 提取特定后缀文件'.***'
            list.append(i)
            o1.insert("end",i)

def selectPath():  # 随机播放
    folder_path = "C:/music"
    folder_list = os.listdir(folder_path)  # 遍历文件夹里面每个文件
    list = []
    count = 0
    for i in folder_list:  # 将文件夹里的文件按顺序传提给变量i  此处区别os.walk()
        if os.path.splitext(i)[1] == '.mp3':  # 提取特定后缀文件'.***'
            list.append(i)
            # print(type(list))
            count = count + 1
    # print(count)

    s = random.randint(0, (count - 1))  # 获取随机数
    file = list[s]
    fil = folder_path + "\\" + file

    pygame.mixer.music.load(fil)
    global path
    path= fil
    pygame.mixer.music.play(1, 0)
    media_info = MediaInfo.parse(fil)
    data = media_info.to_json()  # media到json()这两行是获取文件的所有属性
    rst = re.search('other_duration.*?(.*?)min(.*?)s.*?', data)
    t = int(rst.group(0)[19:20])
    r = int(rst.group(0)[-4:-2])
    m = (t * 60 + r) * 1000

    musictime = str(t) + ':' + str(r)
    l2.config(text=file)
    l3.config(text=musictime)
    lbTime = tkinter.Label(top, anchor='w')
    lbTime.place(x=25, y=150)

def get_song():
    global songname
    song_name=songname
    search_url = "https://songsearch.kugou.com/song_search_v2?callback=jQuery112405132987859127838_1550204317910&page" \
                 "=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_fil" \
                 "ter=0&_=1550204317912&keyword={}".format(song_name)
    headers1 = {
        "UserAgent": ua.random
    }
    global  headers2
    headers2 = {
        "Cookie": "kg_mid=3786e26250f01bf2c64bc515820d9752; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1559960644; Hm_lpvt_aedee6983d4cfc62f509129360d6bb3d=1559960644; ACK_SERVER_10015=%7B%22list%22%3A%5B%5B%22bjlogin-user.kugou.com%22%5D%5D%7D; ACK_SERVER_10016=%7B%22list%22%3A%5B%5B%22bjreg-user.kugou.com%22%5D%5D%7D; ACK_SERVER_10017=%7B%22list%22%3A%5B%5B%22bjverifycode.service.kugou.com%22%5D%5D%7D; kg_dfid=0iEqIA1uep0h0AogH30Jq1Od; kg_dfid_collect=d41d8cd98f00b204e9800998ecf8427e",
        "Host": "www.kugou.com",
        "Referer": "http://www.kugou.com/",
        "UserAgent": ua.random
    }
    global name
    name=song_name
    res = requests.get(search_url, headers=headers1)
    # print(res.text)
    start = re.search("jQuery\d+_\d+\(?", res.text)
    js = json.loads(res.text.strip().lstrip(start.group()).rstrip(")"))  # 注意：末尾有一个换行需要去掉
    global song_list
    song_list = js['data']['lists']

    for i in range(10):
        r1.insert(i,str(i + 1) + ">>>" + str(song_list[i]['FileName']).replace('<em>', '').replace('</em>', ''))

    #num = int(input("\n请输入您想要下载的歌曲序号："))

def download():
    global num
    num=num[0]
    num=int(num)
    x1 = Label(top, text='', width=25, font=("Helvetica", 16))
    x1.place(x=430, y=320)
    v2="请稍等，下载歌曲中..."
    x1.config(text=v2)
    time.sleep(1)

    file_hash = song_list[num - 1]['FileHash']

    hash_url = "http://www.kugou.com/yy/index.php?r=play/getdata&hash={}".format(file_hash)
    # print(hash_url)
    hash_res = requests.get(hash_url, headers=headers2)
    hash_js = hash_res.json()  # json格式
    # print(hash_js)
    play_url = hash_js['data']['play_url']

    # 下载歌曲
    try:
        with open("C:/music/" + name + ".mp3", "wb")as fp:
            fp.write(requests.get(play_url).content)
        v2="歌曲已下载完成！"
        x1.config(text=v2)
    except Exception as e:
        print(e)

def printScale(text):
    t = int(text)
    pygame.mixer.music.set_volume(t / 100)

def jdScale(texts):
    global path
    pat=path
    audio=MP3(pat)
    m=audio.info.length
    t1 =int(texts)
    t=m/100
    pygame.mixer.init()
    pygame.mixer.music.load(pat)
    pygame.mixer.music.play(1,t*t1)

def gdScale():
  while True:
    tex = c1.get()
    print(tex)
    global path
    pat = path
    audio = MP3(pat)
    m = audio.info.length
    t1 = tex
    t = 100/m
    c1.set(t1 + t)
    time.sleep(1)

def update_timeText():
    # Get the current time, note you can change the format as you wish
    current = time.strftime("%H:%M:%S")  # 获取当前时间

    # Update the timeText Label box with the current time
    timeText.configure(text=current)

    # Call the update_timeText() function after 1 second
    top.after(1000, update_timeText)

def musicadd():
    dir='C:/music'
    if not os.path.exists(dir):
        os.mkdir(dir)
    fi = callback()
    fi = fi[0]
    shutil.copy(fi,dir)
    name=str(os.path.basename(fi))
    #for itm in name:
    o1.insert("end",name)


def play():  # 播放音乐
    f = callback()  # 选择制定文件
    f=f[0]
    pygame.mixer.music.load(f)
    pygame.mixer.music.play()
    global path
    path=f
    pathn.set(f)
    media_info = MediaInfo.parse(f)
    data = media_info.to_json()  # medio到json()这两行是获取文件的所有属性
    rst = re.search('other_duration.*?(.*?)min(.*?)s.*?', data)
    t = int(rst.group(0)[19:20])
    r = int(rst.group(0)[-4:-2])
    m = (t * 60 + r) * 1000
    musictime = str(t) + ':' + str(r)
    l2.config(text=f)
    l3.config(text=musictime)
    lbTime = tkinter.Label(top, anchor='w')
    lbTime.place(x=25, y=150)


def stop():
    pygame.mixer.music.stop()  # 停止播放


def pause():
    pygame.mixer.music.pause()  # 暂停


def unpause():
    pygame.mixer.music.unpause()  # 继续播放


def choosepic():  # 保存的路径不能有中文，若需要中文则吧/换成\
    path_s = askopenfilename()
    paths.set(path_s)
    img_open = Image.open(e1.get())
    img = ImageTk.PhotoImage(img_open)
    l1.config(image=img)
    l1.image = img

def getmu(self):
    dir = 'C:/music'
    music_name=o1.get(o1.curselection())
    print(music_name)
    global path
    file=os.path.join(dir,music_name)
    path=file
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()


def create():
    top = Toplevel()
    top.title('使用提示')
    top.geometry("400x400")
    t = "关于照片，新建一个存放图片的文件，用英文命名，然后存里面的图片也用英文命名。关于音乐: 新建一个名字叫音乐的文件，把歌曲添加到该文件夹。"
    msg = Message(top, text=t)
    msg.config(font=('times', 24, 'italic'))
    msg.place(x=0, y=0)


def loops():
    selectPath()

def getentry(self):
    global songname
    songname=s1.get()

def getnum(self):
    global num
    num=r1.get(r1.curselection())
    #print(r1.curselection())

def gettime():
    t = time.strftime('%H%M%S')
    s = int(t[0:2])
    d = int(t[2:4])
    f = int(t[4:6])
    g = s * 60 * 60 + d * 60 + f


if __name__=='__main__':
    l1 = Label(top)  # 图片放置位置
    l1.place(x=0, y=0)

    global songname
    # 时间
    timeText = Label(top, text="", font=("Helvetica", 15))
    timeText.place(x=180, y=370)
    update_timeText()

    # 选择文件
    Button(top, text="选择文件/播放", command=play, width=10, bg="sky blue").place(x=20, y=20)
    Entry(top, text=pathn, width=25, state='readonly').place(x=120, y=20)

    # 选择图片
    Button(top, text='选择图片', command=choosepic, width=10, bg="sky blue").place(x=20, y=55)
    e1 = Entry(top, text=paths, state='readonly', width=25)
    e1.place(x=120, y=55)

    #输入歌曲
    #qq=StringVar()
    s1 = Entry(top, width=25)
    s1.place(x=510, y=20)
    #Button(top, text='确认', command=getentry, width=5, bg="sky blue").place(x=690, y=15)
    s1.bind('<Return>',getentry)
    #songname=qq

    #print(songname)
    Button(top, text='搜索歌曲', command=get_song, width=10, bg="sky blue").place(x=420, y=15)

    # x1 = Label(top, text='', width=25, font=("Helvetica", 16))
    # x1.place(x=430,y=270)
    #slb = Scrollbar(top)
    r1= Listbox(top,width=40,selectmode="browse")
    r1.place(x=420,y=120)
    r1.bind("<Double-Button-1>",getnum)
    # nnum = r1.get()
    # print('第'+nnum)
    Button(top, text='下载', command=download, width=10, bg="sky blue").place(x=420, y=55)

    #歌单
    o1=Listbox(top,width=40,selectmode="brose")
    o1.place(x=730,y=120)
    find()
    Button(top,text='添加歌曲',command=musicadd,bg="sky blue").place(x=740,y=330)
    o1.bind("<Double-Button-1>",getmu)
    m1 = Label(top, text='播放歌单', width=25, font=("Helvetica", 15))
    m1.place(x=750,y=70)

    # 随机播放
    Button(top, text="随机播放", command=selectPath, width=7, bg="sky blue").place(x=20, y=225)
    l2 = Label(top, text='', width=25, font=("Helvetica", 16))  # 音乐名
    l2.place(x=0, y=100)
    Button(top, text="下一首", command=loops, width=5, bg="sky blue").place(x=100, y=225)
    l3 = Label(top, text='', width=15)  # 音乐时长
    l3.place(x=24, y=150)

    # 暂停，继续播放，结束播放
    Button(top, text="暂停", command=pause, width=7, bg="sky blue").place(x=170, y=245)
    Button(top, text="继续播放", command=unpause, width=7, bg="sky blue").place(x=170, y=205)
    Button(top, text="结束播放", command=stop, width=7, bg="sky blue").place(x=240, y=225)

    # 使用说明
    Button(top, text="使用说明", command=create, width=10, bg="sky blue").place(x=20, y=360)

    # 音量
    w1 = Scale(top, from_=0, to=100, orient="horizontal", length=75, variable=v, command=printScale, label="音量")
    w1.place(x=240, y=145)

    #进度条
    c1 = Scale(top, from_=0, to=100, orient="horizontal", length=200,repeatinterval=1000,variable=v1, command=jdScale, label="进度")
    c1.place(x=110, y=275)
    # tt = threading.Thread(target=gdScale())
    # tt.start()
    # while True:
    #   n=c1.get()
    #   if n > 0:
    #       c1.set(n+1)
    #   time.sleep(1000)
    # tt.join(1)
    top.mainloop()

import os
import pickle
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
from tkinter import font
from pygame import mixer

class Player(tk.Frame): #clase
    def __init__(self,master): #metodo
        super().__init__(master)
        self.master= master
        self.pack()

        mixer.init()

        if os.path.exists('songs.pickle'):
            with open('songs.pickle', 'rb') as f:
                self.playlist = pickle.load(f)
        else:
            self.playlist = []


        self.current = 0
        self.paused = True
        self.played= False

        self.create_frames()
        self.track_widgets()
        self.control_widgets()
        self.trackList_widgets()
        

    def create_frames(self):#metodo/funcion
        #SongTrack
        self.track = tk.LabelFrame(self, text='Cancionero', 
                    font=("times new roman", 15, "bold"),
                    bg="pink", fg="white",bd=6,relief=tk.GROOVE)
        self.track.configure(width=410, height=300)
        self.track.grid(row=0, column=0)
        #Song list
        self.trackList = tk.LabelFrame(self, text=f'Playlist - {str(len(self.playlist))}', 
                    font=("times new roman", 15, "bold"),
                    bg='#B9B3E7', fg="white",bd=6,relief=tk.GROOVE)
        self.trackList.configure(width=190, height=600)
        self.trackList.grid(row=0, column=1, rowspan=3, pady=5)
        #controls
        self.controls = tk.LabelFrame(self,  
                    font=("times new roman", 15, "bold"),
   bg="pink", fg="white",bd=6,relief=tk.GROOVE)
        self.controls.configure(width=600, height=450)
        self.controls.grid(row=2, column=0, pady=15, padx=10)

    def track_widgets(self):
        self.canvas = tk.Label(self.track, image=img)
        self.canvas.configure(width=400, height=400)
        self.canvas.grid(row=0, column=0)

        self.songtrack = tk.Label(self.track, font=("times new roman", 15, "bold"),
            bg="white", fg="black")
        self.songtrack['text'] = 'MusicWorld MP3 Player'
        self.songtrack.configure(width=40, height=1)
        self.songtrack.grid(row=1, column=0)

    def control_widgets(self):
        self.loadSongs = tk.Button(self.controls, bg='#B9B3E7', fg="black", font=10)
        self.loadSongs['text'] = 'Abrir directorio'
        self.loadSongs['command'] =  self.retrieve_songs
        self.loadSongs.grid(row=0,column=0, padx=10)
        self.configure(background="pink")

        self.prev = tk.Button(self.controls,image=prev)
        self.prev['command'] =  self.prev_song
        self.prev.grid(row=0, column=1)
        
        self.pause = tk.Button(self.controls, image=pause)
        self.pause['command'] =  self.pause_song
        self.pause.grid(row=0, column=2)

        self.next= tk.Button(self.controls, image=next_)
        self.next['command'] =  self.next_song
        self.next.grid(row=0, column=3)

        self.volume = tk.DoubleVar()
        self.slider = tk.Scale(self.controls, from_=0, to=10, orient=tk.HORIZONTAL)
        self.slider['variable'] = self.volume
        self.slider.set(8)
        mixer.music.set_volume(0.8)
        self.slider['command'] =  self.change_volume
        self.slider.grid(row=0, column=4, padx=5)


    def trackList_widgets(self):
        self.scrollbar = tk.Scrollbar(self.trackList, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0, column=1, rowspan=5, sticky='ns')

        self.list= tk.Listbox(self.trackList, selectmode=tk.SINGLE, 
                    yscrollcommand=self.scrollbar.set, selectbackground='pink')
        self.enumerate_songs()
        self.list.config(height=22)
        self.list.bind('<Double-1>', self.play_song)
        self.scrollbar.config(command=self.list.yview)
        self.list.grid(row=0,column=0, rowspan=5)
        

    def enumerate_songs(self):
        for index, song in enumerate(self.playlist):
            self.list.insert(index,os.path.basename(song))

    def retrieve_songs(self):
        self.songlist = []
        directory = filedialog.askdirectory()
        for root_, dirs, files in os.walk(directory):
           for file in files:
               if os.path.splitext(file)[1] == '.mp3':
                   path = (root_+ '/' + file).replace('\\', '/')
                   self.songlist.append(path)

        with open('songs.pickle', 'wb') as f:
            pickle.dump(self.songlist,f)
        
        self.playlist = self.songlist
        self.trackList['text'] = f'Playlist - {str(len(self.playlist))}'
        self.list.delete(0,tk.END)
        self.enumerate_songs()

    def play_song(self, event=None):
        if event is not None:
            self.current = self.list.curselection()[0]
            for i in range(len(self.playlist)):
                self.list.itemconfigure(i, bg='pink')

        mixer.music.load(self.playlist[self.current])
        self.pause['image'] = play
        self.paused = False
        self.played = True
        self.songtrack['anchor'] = 'w'
        self.songtrack['text'] = os.path.basename(self.playlist[self.current])
        self.list.activate(self.current)
        self.list.itemconfigure(self.current, bg="pink", fg="dark gray")
        mixer.music.play()


    def pause_song(self):
        if not self.paused:
            self.paused = True
            mixer.music.pause()
            self.pause['image'] = pause
        else:
            if self.played == False:
                self.play_song()
            self.paused = False
            mixer.music.unpause()
            self.pause['image'] = play

    def prev_song(self):
        if self.current > 0:
            self.current -= 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current, bg="white")
        self.play_song()

    def next_song(self):
        if self.current < len(self.playlist) -1 :
            self.current += 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current, bg="white")
        self.play_song()

    def change_volume(self, event=None):
        self.v = self.volume.get() #get volumen del 1 al 10
        mixer.music.set_volume(self.v / 10)


root = tk.Tk()
root.geometry('670x580')
root.wm_title('MusicWorld MP3 Player')

img = PhotoImage(file='images/music.gif')
next_ = PhotoImage(file='images/next.png')
prev = PhotoImage(file='images/previous.png')
play = PhotoImage(file='images/play.png')
pause = PhotoImage(file='images/pause.png')

root.resizable(0,0)
root.configure(background="pink")
root.iconbitmap('favicon.ico')

app = Player(master=root)
app.mainloop()
import os
import pygame
import tkinter as tk
from tkinter import filedialog, Listbox, messagebox, Menu

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Music Player")
        self.root.geometry("600x400")

        pygame.mixer.init()

        self.track = tk.StringVar()
        self.status = tk.StringVar()

        # Track Frame for Song label & status label
        trackframe = tk.LabelFrame(self.root, text="Song Track", font=("times new roman", 15, "bold"), bg="grey", fg="white", bd=5, relief=tk.GROOVE)
        trackframe.place(x=0, y=0, width=600, height=100)
        
        songtrack = tk.Label(trackframe, textvariable=self.track, width=20, font=("times new roman", 24, "bold"), bg="grey", fg="gold").grid(row=0, column=0, padx=10, pady=5)
        trackstatus = tk.Label(trackframe, textvariable=self.status, font=("times new roman", 24, "bold"), bg="grey", fg="gold").grid(row=0, column=1, padx=10, pady=5)

        # Button Frame for Play, Stop, Pause, Load buttons
        buttonframe = tk.LabelFrame(self.root, text="Control Panel", font=("times new roman", 15, "bold"), bg="grey", fg="white", bd=5, relief=tk.GROOVE)
        buttonframe.place(x=0, y=100, width=600, height=100)
        
        playbtn = tk.Button(buttonframe, text="PLAY", command=self.play_song, width=10, height=1, font=("times new roman", 16, "bold"), fg="navyblue", bg="gold").grid(row=0, column=0, padx=10, pady=5)
        stopbtn = tk.Button(buttonframe, text="STOP", command=self.stop_song, width=10, height=1, font=("times new roman", 16, "bold"), fg="navyblue", bg="gold").grid(row=0, column=1, padx=10, pady=5)
        pausebtn = tk.Button(buttonframe, text="PAUSE", command=self.pause_song, width=10, height=1, font=("times new roman", 16, "bold"), fg="navyblue", bg="gold").grid(row=0, column=2, padx=10, pady=5)
        loadbtn = tk.Button(buttonframe, text="LOAD", command=self.load_songs, width=10, height=1, font=("times new roman", 16, "bold"), fg="navyblue", bg="gold").grid(row=0, column=3, padx=10, pady=5)

        # Songs Listbox
        songsframe = tk.LabelFrame(self.root, text="Song Playlist", font=("times new roman", 15, "bold"), bg="grey", fg="white", bd=5, relief=tk.GROOVE)
        songsframe.place(x=0, y=200, width=600, height=200)

        scrollbar = tk.Scrollbar(songsframe, orient=tk.VERTICAL)
        self.playlistbox = Listbox(songsframe, yscrollcommand=scrollbar.set, selectbackground="gold", selectmode=tk.SINGLE, font=("times new roman", 12, "bold"), bg="silver", fg="navyblue", bd=5, relief=tk.GROOVE)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar.config(command=self.playlistbox.yview)
        self.playlistbox.pack(fill=tk.BOTH)

        self.load_songs()


    def load_songs(self):
        self.playlistbox.delete(0, tk.END)
        self.songs = []
        for root, dirs, files in os.walk("music/"):
            for file in files:
                if file.endswith(".mp3"):
                    self.songs.append(os.path.join(root, file))
        
        for song in self.songs:
            self.playlistbox.insert(tk.END, os.path.basename(song))
    

    def play_song(self):
        try:
            song = self.songs[self.playlistbox.curselection()[0]]
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()
            self.track.set(os.path.basename(song))
            self.status.set("Playing")
        except Exception as e:
            messagebox.showerror("Error", "No song selected or failed to play. Error: " + str(e))


    def stop_song(self):
        pygame.mixer.music.stop()
        self.status.set("Stopped")
    

    def pause_song(self):
        pygame.mixer.music.pause()
        self.status.set("Paused")


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()

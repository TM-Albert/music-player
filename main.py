import os
import pygame
import tkinter as tk
from tkinter import filedialog, Listbox, messagebox, Menu
from PIL import Image, ImageTk

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Music Player")
        self.root.geometry("720x550")

        pygame.mixer.init()

        self.track = tk.StringVar()
        self.status = tk.StringVar()

        # Frame for the title
        titleframe = tk.Frame(self.root, bg="#002C54", bd=5)
        titleframe.place(x=0, y=0, width=720, height=50)
        
        title = tk.Label(titleframe, text="Songs list", font=("times new roman", 24, "bold"), bg="#002C54", fg="#C5001A")
        title.pack(pady=1)

        # Frame for the songs listbox
        self.songsframe = tk.Frame(self.root, bg="#FDF6F6", bd=5)
        self.songsframe.place(x=0, y=50, width=720, height=400)
        
        scrollbar = tk.Scrollbar(self.songsframe, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas = tk.Canvas(self.songsframe, bg="#FDF6F6", yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.canvas.yview)

        self.inner_frame = tk.Frame(self.canvas, bg="#FDF6F6")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.load_songs()

        settingsframe = tk.Frame(self.root, bg="#002C54", bd=5)
        settingsframe.place(x=0, y=445, width=720, height=110)

        self.play_img = Image.open("./media/play_button.png")
        self.play_img = self.play_img.resize((50, 50), Image.Resampling.LANCZOS)
        self.play_icon = ImageTk.PhotoImage(self.play_img)

        self.stop_img = Image.open("./media/stop_button.png")
        self.stop_img = self.stop_img.resize((50, 50), Image.Resampling.LANCZOS)
        self.stop_icon = ImageTk.PhotoImage(self.stop_img)

        self.play_button = tk.Button(settingsframe, image=self.play_icon, bg="#002C54", bd=0, command=self.toggle_play_stop)
        self.play_button.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        skip_forward_img = Image.open("./media/skip_forward.png")  
        skip_forward_img = skip_forward_img.resize((50, 50), Image.Resampling.LANCZOS)
        skip_forward_icon = ImageTk.PhotoImage(skip_forward_img)
        skip_forward_button = tk.Button(settingsframe, image=skip_forward_icon, bg="#002C54", bd=0, command=self.skip_forward)
        skip_forward_button.image = skip_forward_icon
        skip_forward_button.place(relx=0.60, rely=0.45, anchor=tk.CENTER)

        skip_backward_img = Image.open("./media/skip_backward.png") 
        skip_backward_img = skip_backward_img.resize((50, 50), Image.Resampling.LANCZOS)
        skip_backward_icon = ImageTk.PhotoImage(skip_backward_img)
        skip_backward_button = tk.Button(settingsframe, image=skip_backward_icon, bg="#002C54", bd=0, command=self.skip_backward)
        skip_backward_button.image = skip_backward_icon
        skip_backward_button.place(relx=0.4, rely=0.45, anchor=tk.CENTER)

        self.mute_img = Image.open("./media/volume.png")  
        self.mute_img = self.mute_img.resize((50, 50), Image.Resampling.LANCZOS)
        self.mute_icon = ImageTk.PhotoImage(self.mute_img)

        self.unmute_img = Image.open("./media/muted_volume.png")
        self.unmute_img = self.unmute_img.resize((50, 50), Image.Resampling.LANCZOS)
        self.unmute_icon = ImageTk.PhotoImage(self.unmute_img)

        self.mute_button  = tk.Button(settingsframe, image=self.mute_icon, bg="#002C54", bd=0, command=self.mute_audio)
        self.mute_button.place(relx=0.73, rely=0.45, anchor=tk.CENTER)

        self.volume = tk.DoubleVar()
        self.volume.set(0.5)
        volue_slider = tk.Scale(settingsframe, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, length=140, variable=self.volume, command=self.set_volume, bg="#002C54", fg="white", font=("times new roman", 7, "bold"))
        volue_slider.place(relx=0.88, rely=0.45, anchor=tk.CENTER)

        self.inner_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def play_song(self):
        try:
            selected_song = self.songs[self.playlistbox.curselection()[0]]
            pygame.mixer.music.load(selected_song)
            pygame.mixer.music.play()
            self.play_button.config(image=self.stop_icon)
        except IndexError:
            messagebox.showerror("Error", "No song selected")


    def toggle_play_stop(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            self.play_button.config(image=self.play_icon)  # Change to play icon
        else:
            self.play_song()


    def load_songs(self):
        self.songs = []
        for root, _, files in os.walk("music/"):
            for file in files:
                if file.endswith(".mp3"):
                    self.songs.append(os.path.join(root, file))
        
        for song in self.songs:
                song_name = os.path.basename(song).replace('.mp3', '')
                self.add_song_item(song_name)
    

    def add_song_item(self, song_name):
        song_frame = tk.Frame(self.inner_frame, bg="white", bd=2, relief=tk.GROOVE)
        song_frame.pack(fill=tk.X, padx=5, pady=5)

        rectangle = tk.Label(song_frame, bg="#C5001A", width=4, height=2)
        rectangle.pack(side=tk.LEFT, padx=5, pady=5)

        song_label = tk.Label(song_frame, text=song_name, font=("times new roman", 11, "bold"), bg="white", fg="navyblue")
        song_label.pack(side=tk.LEFT, padx=5)


    def skip_forward(self):
        current_index = self.playlistbox.curselection()[0]
        next_index = (current_index + 1) % len(self.songs)
        self.playlistbox.selection_clear(0, tk.END)
        self.playlistbox.selection_set(next_index)
        self.playlistbox.activate(next_index)
        self.play_song()

    def skip_backward(self):
        current_index = self.playlistbox.curselection()[0]
        previous_index = (current_index - 1) % len(self.songs)
        self.playlistbox.selection_clear(0, tk.END)
        self.playlistbox.selection_set(previous_index)
        self.playlistbox.activate(previous_index)
        self.play_song()


    def mute_audio(self):
        if pygame.mixer.music.get_volume() > 0:
            self.last_volume = pygame.mixer.music.get_volume()
            pygame.mixer.music.set_volume(0)
            self.mute_button.config(image=self.mute_icon)
        else:
            pygame.mixer.music.set_volume(self.last_volume)
            self.mute_button.config(image=self.unmute_icon) 


    def set_volume(self, val):
        volume = float(val)
        pygame.mixer.music.set_volume(volume)


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()

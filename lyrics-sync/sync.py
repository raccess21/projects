import tkinter as tk
from tkinter import filedialog, simpledialog
import pygame
import os
import re

class LyricLine(tk.Frame):
    def __init__(self, master, syncer, line_text, line_index):
        super().__init__(master)
        self.syncer = syncer
        self.line_text = line_text
        self.line_index = line_index
        self.timestamp_str = ""
        self.lyric_text = ""

        self.parse_line()
        self.create_widgets()

    def parse_line(self):
        match = re.match(r"\[(\d{2}:\d{2}\.\d{2})\](.*)", self.line_text)
        if match:
            self.timestamp_str = match.group(1)
            self.lyric_text = match.group(2).strip()
        else:
            self.lyric_text = self.line_text.strip()

    def create_widgets(self):
        self.play_button = tk.Button(self, text="▶", command=self.play_from_here)
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.add_button = tk.Button(self, text="+", command=lambda: self.add_time_to_timestamp(sign=1))
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.sub_button = tk.Button(self, text="-", command=lambda: self.add_time_to_timestamp(sign=-1))
        self.sub_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self, text="💨", command=self.delete_timestamp)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.timestamp_label = tk.Label(self, text=f"{self.timestamp_str}", width=12)
        self.timestamp_label.pack(side=tk.LEFT)
        self.timestamp_label.bind("<Button-1>", self.update_timestamp)
        self.timestamp_label.pack(side=tk.LEFT, padx=5)

        self.lyric_label = tk.Label(
            self,
            text=self.lyric_text,
            anchor="w",
            wraplength=400,   # wrap after 400px (tweak as needed)
            justify="left"    # align wrapped lines to the left
        )
        self.lyric_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.lyric_label.bind("<Button-1>", self.edit_lyric)

    def play_from_here(self):
        if self.timestamp_str:
            minutes, seconds = map(float, self.timestamp_str.split(':'))
            time_in_seconds = minutes * 60 + seconds
            self.syncer.play_audio(start_time=time_in_seconds)

    def delete_timestamp(self):
        if 0 <= self.line_index < len(self.syncer.lyrics):
            del self.syncer.lyrics[self.line_index]
            self.syncer.save_lrc_file()

        self.destroy()
    
    def add_time_to_timestamp(self, sign):
        if self.timestamp_str:
            minutes, seconds = map(float, self.timestamp_str.split(':'))
            time_in_seconds = minutes * 60 + seconds + (sign * 0.2)
            minutes = int(time_in_seconds // 60)
            seconds = time_in_seconds % 60
            self.timestamp_str = f"{minutes:02d}:{seconds:05.2f}"
            self.timestamp_label.config(text=f"[{self.timestamp_str}]")
            self.update_lrc_line()
            self.play_from_here()

    def update_timestamp(self, event):
        if not pygame.mixer.music.get_busy():
            return

        pos_ms = pygame.mixer.music.get_pos()
        if pos_ms < 0 and self.syncer.play_t0 is not None:
            # fallback if get_pos misbehaves
            elapsed = (pygame.time.get_ticks() - self.syncer.play_t0) / 1000.0
        else:
            elapsed = max(0.0, pos_ms / 1000.0)

        # absolute position = offset we started + elapsed since then
        current_time = self.syncer.start_offset + elapsed

        minutes = int(current_time // 60)
        seconds = current_time % 60
        self.timestamp_str = f"{minutes:02d}:{seconds:05.2f}"
        self.timestamp_label.config(text=f"[{self.timestamp_str}]")
        self.update_lrc_line()

    def edit_lyric(self, event):
        new_lyric = simpledialog.askstring("Edit Lyric", "Enter new lyric:", initialvalue=self.lyric_text)
        if new_lyric is not None:
            self.lyric_text = new_lyric
            self.lyric_label.config(text=self.lyric_text)
            self.update_lrc_line()
            
    def update_lrc_line(self):
        new_line = f"[{self.timestamp_str}] {self.lyric_text}\n"
        self.syncer.lyrics[self.line_index] = new_line
        self.syncer.save_lrc_file()
    
    def set_highlight(self, active: bool):
        if active:
            self.lyric_label.config(bg="yellow")
        else:
            self.lyric_label.config(bg="SystemButtonFace")


class LyricSyncer:
    def __init__(self, master):
        self.master = master
        master.title("Lyric Syncer")
        self.audio_file = "Sanson Ki Mala Peh Simroon Main Nusrat Fateh Ali Khan.mp3"

        self.lrc_file = ""
        self.lyrics = []
        self.lyric_lines = []
        self.current_highlight = -1
        # track playback offset & play start
        self.start_offset = 0.0
        self.play_t0 = None

        self.create_widgets()

    def create_widgets(self):
        self.top_frame = tk.Frame(self.master)
        self.top_frame.pack(fill=tk.X)
        
        self.load_button = tk.Button(self.top_frame, text="Load Audio", command=self.load_audio)
        self.load_button.pack(side=tk.LEFT)

        self.play_button = tk.Button(self.top_frame, text="Play", command=self.play_audio, state=tk.DISABLED)
        self.play_button.pack(side=tk.LEFT)

        self.load_button = tk.Button(self.top_frame, text="ReLoad Lrc", command=self.load_lyrics)
        self.load_button.pack(side=tk.LEFT)


        self.canvas = tk.Canvas(self.master)
        self.scrollbar = tk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")


    def load_audio(self):
        self.audio_file = self.audio_file or filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if self.audio_file:
            self.lrc_file = os.path.splitext(self.audio_file)[0] + ".lrc"
            self.load_lyrics()
            self.play_button.config(state=tk.NORMAL)

    def load_lyrics(self):
        if os.path.exists(self.lrc_file):
            with open(self.lrc_file, "r", encoding="utf-8") as f:
                self.lyrics = f.readlines()
        else:
            self.lyrics = [
                f"[00:00.00] Lyrics Not Found\n",
                f"[00:01.00] For File \n",
                f"[00:02.00] {self.lrc_file}\n",
            ]
        self.display_lyrics()

    def display_lyrics(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.lyric_lines = []
        for i, line in enumerate(self.lyrics):
            lyric_line_widget = LyricLine(self.scrollable_frame, self, line, i)
            lyric_line_widget.pack(fill=tk.X, pady=2)
            self.lyric_lines.append(lyric_line_widget)

    def play_audio(self, start_time=0):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self.start_offset = float(start_time)
        self.play_t0 = pygame.time.get_ticks()
        pygame.mixer.music.load(self.audio_file)
        pygame.mixer.music.play(start=start_time)

        self.update_highlight()

    def save_lrc_file(self):
        with open(self.lrc_file, "w", encoding="utf-8") as f:
            f.writelines(self.lyrics)

    def update_highlight(self):
        if not pygame.mixer.music.get_busy():
            return

        pos_ms = pygame.mixer.music.get_pos()
        if pos_ms < 0 and self.play_t0 is not None:
            elapsed = (pygame.time.get_ticks() - self.play_t0) / 1000.0
        else:
            elapsed = max(0.0, pos_ms / 1000.0)
        current_time = self.start_offset + elapsed

        # find current line
        idx = -1
        for i, line in enumerate(self.lyrics):
            match = re.match(r"\[(\d{2}):(\d{2}\.\d{2})\]", line)
            if match:
                minutes, seconds = int(match.group(1)), float(match.group(2))
                ts = minutes * 60 + seconds
                if current_time >= ts:
                    idx = i
                else:
                    break

        # update highlight only if changed
        if idx != self.current_highlight:
            if self.current_highlight >= 0:
                self.lyric_lines[self.current_highlight].set_highlight(False)
            if idx >= 0:
                self.lyric_lines[idx].set_highlight(True)
            self.current_highlight = idx

        self.master.after(300, self.update_highlight)

if __name__ == "__main__":
    pygame.init()
    root = tk.Tk()
    app = LyricSyncer(root)
    root.mainloop()
    pygame.quit()

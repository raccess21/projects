# 🎶 Lyrics Sync Tool

A simple Python desktop tool to **play audio files with synchronized lyrics** (`.lrc` format).  
It also lets you **edit, timestamp, or delete lyric lines** with an easy-to-use GUI.

---

## ✨ Features
- Play `.mp3` or `.wav` audio files.
- Load matching `.lrc` lyrics (if present).
- **Click a lyric line** → add a timestamp for the current music position.
- **Delete a lyric line** → permanently removes it from the `.lrc` file.
- **Edit lyrics directly** by clicking them.
- **Highlight current line** while the song is playing.
- Auto-wrapping for long lyric lines.
- `.lrc` file updates instantly (no need to manually save).

---

![Sample Screenshot](./ss1.png)

## 🛠 Requirements
- Python 3.8+
- Dependencies:
  - `pygame` (for audio playback)
  - `tkinter` (for GUI, comes pre-installed with Python on most systems)

Install pygame via pip:

~~~bash
pip install pygame
~~~

---

## 🚀 Usage

1. Clone or download this repo.
2. Run the app:

~~~bash
python sync.py
~~~

3. Open an `.mp3` or `.wav` file:
   - If a matching `.lrc` exists (`filename.lrc`), it will load automatically.
   - If no `.lrc` exists, you can add lines manually.

---

## 🎛 Controls
- **▶ Play/Pause:** Control playback of the audio file.
- **🖱 Click lyric line:** Add or edit a timestamp.
- **🗑 Delete line:** Remove the entire lyric line (both from UI and `.lrc` file).
- **Current line highlight:** See which lyric is currently playing in real time.

---

## 📂 Example `.lrc` formats

With timestamps:
~~~lrc
[00:50.71] जुदा होके भी
[00:55.57] तू मुझमें कहीं बाकी है
[01:01.64] पलकों में बनके आँसू, तू चली आती है
~~~

Without timestamps (will be synced manually):
~~~lrc
जुदा होके भी
तू मुझमें कहीं बाकी है
पलकों में बनके आँसू, तू चली आती है
~~~

---

## 💡 Workflow Tip
Instead of re-running `sync.py` every time you make small code changes, you can use:

- **[watchdog](https://pypi.org/project/watchdog/)** or **`python -m watchdog`** to auto-restart when files change.
- Or run in **VS Code with auto-reload** (`F5` debugging, restart on save).
- Or use **`watchmedo auto-restart`**:
  ~~~bash
  watchmedo auto-restart --pattern="*.py" --recursive -- python sync.py
  ~~~

---

## 📜 License
MIT License – free to use, modify, and distribute.

---

## 👨‍💻 Author
Built with ❤️ using Python, Tkinter, and Pygame.

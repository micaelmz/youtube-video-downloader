import threading
from os import system
from io import BytesIO
from tkinter import *
from tkinter import filedialog, ttk, messagebox
import customtkinter
from urllib.request import urlopen

import pyperclip
from PIL import ImageTk, Image
from PIL.Image import Resampling
from pytube import YouTube


customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green


download_path = None
download_name = None

# --------------------  COMMANDS  -------------------- #
def get_thumnail(url):
    image_url = urlopen(url)
    image_raw = image_url.read()
    image_url.close()
    image = Image.open(BytesIO(image_raw))
    thumbnail = image.resize((300, 200), resample=Resampling.LANCZOS)
    image_tk = ImageTk.PhotoImage(thumbnail)
    return image_tk


def paste_url():
    clipboard = pyperclip.paste()
    video_url_entry.delete(0, END)
    video_url_entry.insert(0, clipboard)


def select_path():
    global download_path
    download_path = filedialog.askdirectory()
    destination_path_label_entry.config(text=download_path)


def show_progress_bar(s, chunk, bytes_remaining):
    download_percent_progressbar = float((s.filesize - bytes_remaining) / s.filesize)
    download_percent_title = int(download_percent_progressbar * 100)
    root.after(0, update_gui(download_percent_progressbar, download_percent_title))
    print(f'\rProgress: {download_percent_title} %')


def update_gui(dp_progessbar, dp_title):
    progressbar.set(value=dp_progessbar)
    root.title(f'\rProgress: {dp_title} %')


def complete(s, file_path):
    want_to_open = messagebox.askyesno(title='Download Complete!',
                                       message='Do you want to open the downloaded file?')
    if want_to_open:
        system(f'start {download_path}')

def download_video():
    global download_path
    link = video_url_entry.get()

    # dividir essa funcão em outras
    try:
        yt = YouTube(link)
    except:
        messagebox.showerror(title="Error -  Invalid URL",
                             message='Is not possible to find this video, check the video URL and try again')

    # Don't put callback into Thread
    yt.register_on_progress_callback(show_progress_bar)
    yt.register_on_complete_callback(complete)

    new_icon = get_thumnail(yt.thumbnail_url)
    main_image.configure(image=new_icon)
    main_image.image = new_icon

    is_ok = messagebox.askokcancel(title=yt.title,
                                   message=f'Title: {yt.title}\n'
                                           f'Length: {yt.length // 60}m{yt.length & 60}s\n'
                                           f'Views: {yt.views}\n'
                                           f'Author: {yt.author}')

    if is_ok:
        resolution = current_var.get()

        if resolution == 'mp3':
            video_stream = yt.streams.get_audio_only()
        elif resolution == 'Highest':
            video_stream = yt.streams.get_highest_resolution()
        else:
            video_stream = yt.streams.get_by_resolution(resolution)

        # You cant just call video_stream.download() with params, because it will execute and block outside Thread
        threading.Thread(target=video_stream.download,
                         kwargs={"output_path": download_path, "filename_prefix": f'({resolution}) '}).start()

    else:
        main_image.configure(image=icon)
        main_image.image = icon


# Screen settings
root = customtkinter.CTk()
root.geometry(f"{500}x{400}")
icon = PhotoImage(file='./../logo.png')
root.iconphoto(False, icon)
root.title('Youtube Video Downloader')
root.config(padx=50, pady=50)

# Main Canvas
main_image = Label(root, image=icon, width=350, height=200, bg='black')
main_image.grid(row=1, column=1, columnspan=3)

# Labels
video_url_label = Label(text='Video URL:')
video_url_label.grid(row=2, column=1)
destination_path_label_entry = Label(width=40, bg='white')
destination_path_label_entry.grid(row=3, column=1, columnspan=2)

# Entry's
video_url_entry = Entry(width=35)
video_url_entry.focus()
video_url_entry.grid(row=2, column=2)

# Buttons
search_button = Button(text='Paste', width=15, command=paste_url)
search_button.grid(row=2, column=3)
destination_path_button = Button(text='Select Path', width=15, command=select_path)
destination_path_button.grid(row=3, column=3)
current_var = StringVar(value='Resolution')
combobox = customtkinter.CTkComboBox(variable=current_var,
                                     state='readonly',
                                     values=['mp3', '144p', '240p', '360p', '480p', '720p', '1080p', 'Highest'],
                                     width=100,
                                     text_color_disabled='red',
                                     hover=True)
combobox.grid(row=4, column=1)
download_button = customtkinter.CTkButton(text='Download as MP4', width=300, command=download_video)
download_button.grid(row=4, column=2, columnspan=2)

# Progress bar
progressbar = customtkinter.CTkProgressBar(root, orient=HORIZONTAL, width=410, progress_color='red', bg='black')
progressbar.set(value=0.0)
progressbar.grid(row=5, column=1, columnspan=3)

root.mainloop()

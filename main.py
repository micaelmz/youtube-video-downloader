import tkinter
import customtkinter
from tkinter import *
from tkinter import filedialog, messagebox

import threading
from io import BytesIO
from os import system
from pathlib import Path

from urllib.request import urlopen
from PIL import ImageTk, Image, ImageStat

from pytube import YouTube, Playlist

VIDEO_SCREEN = 'video_screen'
PLAYLIST_SCREEN = 'playlist_screen'
MP3_SCREEN = 'mp3_screen'


class App(customtkinter.CTk):
    WIDTH = 780
    HEIGHT = 520
    COLOR = '#fa0001'
    HOVER_COLOR = '#f74f20'
    TEXT_FONT = ('Arial', 10, 'bold')

    def __init__(self):
        super().__init__()

        # Set up
        self.app_icon = PhotoImage(file='logo.png')
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.title('Youtube Video Downloader')
        self.iconphoto(False, self.app_icon)
        self.download_path = str(Path(__file__).parent.resolve())
        self.current_screen = PLAYLIST_SCREEN
        self.frame_right = {'video_screen': None, 'playlist_screen': None, 'mp3_screen': None}
        self.frame_info = {'video_screen': None, 'playlist_screen': None, 'mp3_screen': None}
        self.search_button_icon = ImageTk.PhotoImage(Image.open("search.png").resize((20, 20), resample=1))

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ============ FRAME LEFT / MENU BAR ============

        self.frame_left = customtkinter.CTkFrame(master=self, width=180, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nwsw")
        # Fill the rows with 'blank space' ready to be use, up 1 to 17
        self.frame_left.rowconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17), weight=1)

        # -------------- HEAD --------------
        self.icon_image_resize = ImageTk.PhotoImage(Image.open("logo.png").resize((100, 70), resample=1))
        self.icon_image = customtkinter.CTkLabel(master=self.frame_left, image=self.icon_image_resize)
        self.icon_image.photo = self.icon_image_resize
        self.icon_image.grid(row=0, column=0, pady=10)

        self.title_label = customtkinter.CTkLabel(master=self.frame_left,
                                                  text="YouTube \nVideo Downloader",
                                                  text_font=('Franklin Gothic Medium Cond', 16),
                                                  text_color=App.COLOR)
        self.title_label.grid(row=1, column=0, pady=20, padx=10)

        # -------------- BODY --------------
        self.video_dowload_button = customtkinter.CTkButton(master=self.frame_left,
                                                            text="Download Video",
                                                            border_width=0,
                                                            height=35,
                                                            fg_color=App.COLOR,
                                                            hover_color=App.HOVER_COLOR,
                                                            text_font=App.TEXT_FONT,
                                                            command=self.change_screen_to_video)
        self.video_dowload_button.grid(row=3, column=0, padx=10)

        self.playlist_download_button = customtkinter.CTkButton(master=self.frame_left,
                                                                text="Download Playlist",
                                                                border_width=0,
                                                                height=35,
                                                                fg_color=App.COLOR,
                                                                hover_color=App.HOVER_COLOR,
                                                                text_font=App.TEXT_FONT,
                                                                command=self.change_screen_to_playlist)
        self.playlist_download_button.grid(row=4, column=0, padx=10)

        self.mp3_dowload_button = customtkinter.CTkButton(master=self.frame_left,
                                                          text="Download MP3",
                                                          border_width=0,
                                                          height=35,
                                                          fg_color=App.COLOR,
                                                          hover_color=App.HOVER_COLOR,
                                                          text_font=App.TEXT_FONT,
                                                          command=self.change_screen_to_mp3)
        self.mp3_dowload_button.grid(row=5, column=0, padx=10)

        # -------------- bOTTOM --------------
        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode", text_font=App.TEXT_FONT)
        self.label_mode.grid(row=15, column=0, padx=10)

        self.mode_menu = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                     values=["Dark", "Light", "System"],
                                                     fg_color='#6e0203',
                                                     button_color='#6e0203',
                                                     button_hover_color='#4a0102',
                                                     text_font=App.TEXT_FONT,
                                                     command=self.change_appearance_mode)
        self.mode_menu.grid(row=16, column=0, padx=10)

        # ============ FRAME RIGHT / MAIN SCREEN ============

        for screen in self.frame_right.keys():
            self.frame_right[screen] = customtkinter.CTkFrame(master=self, corner_radius=0)
            self.frame_right[screen].rowconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), weight=1)

        # -------------- FRAME INFO --------------
        for screen in self.frame_info.keys():
            self.frame_info[screen] = customtkinter.CTkFrame(master=self.frame_right[screen],
                                                             width=300, height=160,
                                                             corner_radius=20, fg_color='#343638')
            self.frame_info[screen].rowconfigure((0, 1, 2, 3, 4), weight=1)
            self.frame_info[screen].columnconfigure((0, 1, 2, 3, 4), weight=1)

        # -------------- VIDEO DOWNLOAD SCREEN --------------
        self.frame_right[VIDEO_SCREEN].rowconfigure((4, 5, 6, 7, 8, 9, 10, 11, 12, 13), weight=1)

        self.video_title_label = customtkinter.CTkLabel(master=self.frame_right[VIDEO_SCREEN],
                                                        text_font=App.TEXT_FONT,
                                                        text='')
        self.video_title_label.grid(row=0, column=0, columnspan=3, padx=(20, 0))

        self.thumbnail_image = customtkinter.CTkLabel(master=self.frame_info[VIDEO_SCREEN],
                                                      image=self.app_icon,
                                                      width=300, height=160,
                                                      corner_radius=6,
                                                      justify=tkinter.LEFT)
        self.thumbnail_image.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)
        
        self.resolution_combobox = customtkinter.CTkOptionMenu(master=self.frame_right[VIDEO_SCREEN],
                                                               values=['Highest', '144p', '240p', '360p', '480p',
                                                                       '720p', '1080p'],
                                                               fg_color=App.COLOR,
                                                               button_color=App.COLOR,
                                                               button_hover_color=App.HOVER_COLOR,
                                                               text_font=App.TEXT_FONT)
        self.resolution_combobox.grid(row=1, column=1)

        # Select Path
        self.path_label = customtkinter.CTkLabel(master=self.frame_right[VIDEO_SCREEN], width=330,
                                                 text=Path(__file__).parent.resolve(), bg_color='#343638', anchor='w')
        self.path_label.grid(row=10, column=0)

        self.path_button = customtkinter.CTkButton(master=self.frame_right[VIDEO_SCREEN],
                                                   text="Select Path",
                                                   border_width=0,
                                                   fg_color=App.COLOR, hover_color=App.HOVER_COLOR,
                                                   text_font=App.TEXT_FONT,
                                                   command=self.select_path)
        self.path_button.grid(row=10, column=1, padx=10, columnspan=2)

        # Put URL
        self.url_entry = customtkinter.CTkEntry(master=self.frame_right[VIDEO_SCREEN],
                                                width=330,
                                                placeholder_text="Video URL")
        self.url_entry.grid(row=11, column=0, padx=20, sticky="w")

        self.download_button = customtkinter.CTkButton(master=self.frame_right[VIDEO_SCREEN],
                                                       text="Download",
                                                       border_width=0,
                                                       fg_color=App.COLOR, hover_color=App.HOVER_COLOR,
                                                       text_font=App.TEXT_FONT,
                                                       command=self.download_video)
        self.download_button.grid(row=11, column=1, padx=10, columnspan=2)

        # Progress bar
        self.download_progress_bar = customtkinter.CTkProgressBar(master=self.frame_right[VIDEO_SCREEN],
                                                                  width=535,
                                                                  progress_color=App.COLOR,
                                                                  highlightthickness=0,
                                                                  height=7)
        self.download_progress_bar.grid(row=13, column=0, columnspan=2)
        self.download_progress_bar.set(value=0)
        # The progressbar just shows up when download starts
        self.download_progress_bar.grid_forget()

        # -------------- PLAYLIST DOWNLOAD SCREEN --------------

        self.current_video_thumbnail = customtkinter.CTkLabel(master=self.frame_info[PLAYLIST_SCREEN],
                                                              image=self.app_icon,
                                                              width=300, height=160,
                                                              corner_radius=6,
                                                              justify=tkinter.LEFT)
        self.current_video_thumbnail.grid(column=0, row=1, sticky="nwe", padx=(20, 0), pady=15)

        self.current_video_title_label = customtkinter.CTkLabel(master=self.frame_right[PLAYLIST_SCREEN],
                                                        text_font=App.TEXT_FONT,
                                                        text='')
        self.current_video_title_label.grid(row=0, column=0, padx=(20, 0))

        self.playlist_canvas = customtkinter.CTkCanvas(master=self.frame_right[PLAYLIST_SCREEN], width=170, height=550)
        self.playlist_frame = customtkinter.CTkFrame(master=self.playlist_canvas, width=150, corner_radius=0, height=450, fg_color='#000')
        self.playlist_scrollbar = customtkinter.CTkScrollbar(master=self.frame_right[PLAYLIST_SCREEN],
                                                             orientation='vertical',
                                                             command=self.playlist_canvas.yview, height=450)

        self.playlist_frame.bind(
            "<Configure>",
            lambda e: self.playlist_canvas.configure(
                scrollregion=self.playlist_canvas.bbox("all")
            )
        )

        self.playlist_canvas.create_window((0, 0), window=self.playlist_frame, anchor='nw', width=450)
        self.playlist_canvas.configure(yscrollcommand=self.playlist_scrollbar.set)

        # for i in range(50):
        #     customtkinter.CTkLabel(self.playlist_frame, text="Sample scrolling label").grid()

        self.playlist_canvas.grid(row=0, column=2, sticky="ne", padx=(25, 0), rowspan=10)
        self.playlist_scrollbar.grid(row=0, column=3, rowspan=10)

        self.playlist_url_entry = customtkinter.CTkEntry(master=self.frame_right[PLAYLIST_SCREEN],
                                                width=275,
                                                placeholder_text="Playlist URL")
        self.playlist_url_entry.grid(row=8, column=0, padx=(20, 0), sticky="w")
        self.playlist_url_entry.insert(0, 'https://www.youtube.com/watch?v=x3vUDtofPtQ&list=PLTKSoAGcIUokqHfZgwMZ77hGTKSFK9Nos')

        self.search_playlist_button = customtkinter.CTkButton(master=self.frame_right[PLAYLIST_SCREEN],
                                                              text="",
                                                              image=self.search_button_icon,
                                                              border_width=0, bg_color=None,
                                                              fg_color=App.COLOR, hover_color=App.HOVER_COLOR,
                                                              width=27, height=27,
                                                              command=self.search_playlist)
        self.search_playlist_button.grid(row=8, column=1, padx=(0, 10), sticky='w')


        self.confirm_download_button = customtkinter.CTkButton(master=self.frame_right[PLAYLIST_SCREEN],
                                                               text="Confirm Download",
                                                               border_width=0,
                                                               fg_color=App.COLOR, hover_color=App.HOVER_COLOR,
                                                               text_font=App.TEXT_FONT,
                                                               width=315, height=30,
                                                               command=None,
                                                               state='disabled')
        self.confirm_download_button.grid(row=9, column=0, padx=(20, 0), pady=(0, 20), columnspan=2, sticky='w')


        # -------------- MP3 DOWNLOAD SCREEN --------------

        self.update_frames()
    # ============ METHODS ============

    def change_screen_to_mp3(self):
        self.current_screen = MP3_SCREEN
        self.update_frames()

    def change_screen_to_video(self):
        self.current_screen = VIDEO_SCREEN
        self.update_frames()

    def change_screen_to_playlist(self):
        self.current_screen = PLAYLIST_SCREEN
        self.update_frames()

    def update_frames(self):
        for screen in self.frame_right.keys():
            if screen == self.current_screen:
                self.frame_right[screen].grid(row=0, column=1, sticky="nwse", padx=40, pady=40)
                self.frame_info[screen].grid(row=1, column=0, columnspan=2, rowspan=4, pady=(0, 20), padx=20, sticky="nw")
            else:
                self.frame_right[screen].grid_forget()
                self.frame_info[screen].grid_forget()


    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def get_thumnail(self, url):
        image_url = urlopen(url)
        image_raw = image_url.read()
        image_url.close()
        image = Image.open(BytesIO(image_raw))
        image_with_no_borders = image.crop((0, 60, 640, 420))
        thumbnail = image_with_no_borders.resize((350, 200), resample=1)
        image_tk = ImageTk.PhotoImage(thumbnail)

        # Gets the median collor in the thumbnail
        pallete_rgb = ImageStat.Stat(image).median
        # Converts RGB list in a HEX string value of the collor
        pallete = f'#{pallete_rgb[0]:02x}{pallete_rgb[1]:02x}{pallete_rgb[2]:02x}'
        self.frame_info[self.current_screen].configure(fg_color=pallete)

        return image_tk

    def select_path(self):
        self.download_path = filedialog.askdirectory()
        self.path_label.configure(text=self.download_path)

    def show_progress_bar(self, s, chunk, bytes_remaining):
        self.download_progress_bar.grid(row=13, column=0, columnspan=2, rowspan=2)
        download_percent_progressbar = float((s.filesize - bytes_remaining) / s.filesize)
        download_percent_title = int(download_percent_progressbar * 100)
        self.after(0, self.update_gui(download_percent_progressbar, download_percent_title))

    def update_gui(self, download_percent_progessbar, download_percent_title):
        self.download_progress_bar.set(value=download_percent_progessbar)
        self.title(f'\rDownload in progress: {download_percent_title} %')

    def complete(self, s, file_path):
        self.download_progress_bar.grid_forget()
        self.title('YouTube Video Downloader')

        want_to_open = messagebox.askyesno(title='Download Complete!',
                                           message='Do you want to open the downloaded file folder?')
        if want_to_open:
            system(f'start {self.download_path}')

    def search_playlist(self):
        url = self.playlist_url_entry.get()
        playlist = Playlist(url)
        videos = playlist.videos
        self.current_video_title_label.configure(text=playlist.title)

        # por tudo numa lista pra ser possivel limpar
        # por todos numa lista pra o usuario escolher qual baixar ou não
        # a thumbnail fica no msm for so que no grid é coluna 1 texto e 0 thumb
        for indice, video in enumerate(playlist.videos):
            customtkinter.CTkLabel(self.playlist_frame,
                                   text=f'{video.title[:20]}\n'
                                        f'{video.title[20:34]}\n'
                                        f'{video.title[34:50]}\n',
                                   text_font=App.TEXT_FONT,
                                   justify=tkinter.LEFT,
                                   anchor='w', width=15).grid(column=1, row=indice)

            customtkinter.CTkLabel(self.playlist_frame,
                                   image=self.get_thumnail(video.thumbnail_url),
                                   justify=tkinter.LEFT,
                                   anchor='w', width=15).grid(column=0, row=indice)
            #print(video.title)
            #print(f'Baixando vídeo {indice + 1}/{len(playlist)}')
            #video.streams.first().download(self.download_path)

    def download_video(self):
        video_url = self.url_entry.get()

        # dividir essa funcão em outras
        try:
            yt = YouTube(video_url)
        except:
            messagebox.showerror(title="Error -  Invalid URL",
                                 message='Is not possible to find this video, check the video URL and try again')
        else:
            yt.register_on_progress_callback(self.show_progress_bar)
            yt.register_on_complete_callback(self.complete)

            new_icon = self.get_thumnail(yt.thumbnail_url)
            self.thumbnail_image.configure(image=new_icon)
            self.thumbnail_image.image = new_icon

            self.video_title_label.configure(text=f'{yt.title[:80]}', width=500)

            is_ok = messagebox.askokcancel(title=yt.title,
                                           message=f'Title: {yt.title}\n'
                                                   f'Length: {yt.length // 60}m{yt.length & 60}s\n'
                                                   f'Views: {yt.views}\n'
                                                   f'Author: {yt.author}')

            if is_ok:
                resolution = self.resolution_combobox.get()

                if resolution == 'mp3':
                    video_stream = yt.streams.get_audio_only()
                elif resolution == 'Highest':
                    video_stream = yt.streams.get_highest_resolution()
                else:
                    video_stream = yt.streams.get_by_resolution(resolution)

                threading.Thread(target=video_stream.download, kwargs={"output_path": self.download_path,
                                                                       "filename_prefix": f'({resolution}) '}).start()
            else:
                self.thumbnail_image.configure(image=self.app_icon)
                self.thumbnail_image.image = self.app_icon
                self.frame_info[self.current_screen].configure(fg_color='#343638')
                self.video_title_label.configure(text='')


app = App()
app.mainloop()

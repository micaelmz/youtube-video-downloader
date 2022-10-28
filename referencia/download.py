import sys

from pytube import YouTube

# Digite o link do vídeo e o local que deseja salvar o video #
link = input("Digite o link do vídeo que deseja baixar:  ")
path = input("Digite o diretório que deseja salvar o vídeo:  ")

def progress(s, chunk, bytes_remaining):
    download_percent = int((s.filesize-bytes_remaining)/s.filesize*100)
    print(f'aaa {download_percent}')
    sys.stdout.write(f'\rProgress: {download_percent} %')
    sys.stdout.flush()

yt = YouTube(link, on_progress_callback=progress)

# Mostra os detalhes do video #
print("Título: ", yt.title)
print("Número de views: ", yt.views)
print("Tamanho do vídeo: ", yt.length, "segundos")
print("Avaliação do vídeo: ", yt.rating)
thumb = yt.thumbnail_url

# Usa a maior resolucao #
ys = yt.streams.get_highest_resolution()


# Começa o Download do vídeo #
print("Baixando...")
ys.download(path)
print("Download completo!")
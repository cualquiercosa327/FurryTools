import requests
import threading
import os

import tkinter as tk
from tkinter import filedialog

from lib import f_funcs as funcs


def start(app):
    Window = tk.Toplevel(app)
    Window.geometry("400x200")
    Window.title('Favorite Downloader')
    L1 = tk.Label(Window, text="Input the Username")
    L1.pack()
    nameInput = tk.Entry(master=Window)
    nameInput.pack()
    # input('Enter the Username of whom you will download theyere favs: ')
    L2 = tk.Label(Window, text="Input how much favorites you want. (320 Max)")
    L2.pack()
    limitInput = tk.Entry(master=Window)
    limitInput.pack()
    # input('Enter how much favorites you want to download (MAX is 320): ')

    runBtn = tk.Button(master=Window, command= lambda: run(nameInput.get(), limitInput.get()), text="Download!")
    runBtn.pack()
    
    def run(name, limit):
        d = filedialog.askdirectory(initialdir=os.getcwd())

        if (int(limit) > 320):
            print('I am sorry but the hard limit is 320.')
            print('Running again...')
            start()

        url = f'https://e621.net/posts.json?tags=fav:{name}&limit={limit}'

        head = {'User-Agent': 'favDownloader/0.1'}

        body = requests.get(url, headers=head)
        p = body.json()

        if (body.status_code == 403):
            print(f'The user {name} has blocked access to theyre favorites.')
            print('Running again...')
            start()

        i = 0

        favsCount = len(p['posts'])

        print(f'Downloading {favsCount} favs!')

        while i < len(p['posts']):
            fileUrl = p['posts'][i]['file']['url']
            artistArray = p['posts'][i]['tags']['artist']
            postID = p['posts'][i]['id']
            artistName = ''

            if (len(artistArray) > 1):
                for a in artistArray:
                    artistName = artistName + f'{a}, '
                    artistName = artistName[:-1]
            else:
                artistName = artistArray = p['posts'][i]['tags']['artist'][0]

            threading.Thread(target=funcs.download, args=(
                fileUrl, artistName, postID, head, d)).start()

            i = i + 1
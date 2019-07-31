#指定したURLの画像を取得する
import os
from tkinter import *
from tkinter import filedialog,messagebox
import requests
from bs4 import BeautifulSoup
from requests.compat import urljoin
import traceback
import threading

#参照ボタン押下時処理
def pathButton_click():
    #フォルダ選択のダイアログを開き、選択したパスを画面に設定する
    iDir = os.path.abspath(os.path.dirname(__file__))
    dir = filedialog.askdirectory(initialdir=iDir)
    pathText.delete(0, END)
    pathText.insert(0, dir)

#ダウンロード開始ボタン押下時処理
def downloadButton_click():

    if not urlText.get():
        messagebox.showwarning('URL未設定', '画像を取得するサイトのURLを設定してください。')
        return

    if not pathText.get():
        messagebox.showwarning('保存先未設定', '画像の保存先を設定してください。')
        return

    #画像ダウンロード処理を別スレッドで実行する
    th = threading.Thread(target=downloadImage)
    th.start()

#終了ボタン押下時処理
def exitButton_click():
    quit()

#画像のダウンロード処理
def downloadImage():
    try:
        url = urlText.get()
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        paths = []

        #for image in soup.find('div', class_='ently_text').find_all('img'):#特定の場所の画像のみ取得する場合
        for image in soup.find_all('img'):#ページ内の全ての画像を取得する場合
            src = image.get('src')
            if src.endswith('.jpg') or src.endswith('.png'):
                #画像の相対パスを絶対パスに変換して配列に格納する
                paths.append(urljoin(url, src))

        #画像を指定した場所に保存する
        for path in paths:
            req = requests.get(path)
            with open(pathText.get() + '/' + path.split('/')[-1], 'wb') as f:
                f.write(req.content)

        messagebox.showinfo('画像のダウンロード完了', '画像のダウンロードが完了しました。')

    except:
        errMsg = '例外が発生しました。' \
                 '\nURL:' + urlText.get() + '' \
                 '\nPath:' + pathText.get() + '' \
                 '\n(' + traceback.format_exc() + ')'
        messagebox.showerror('異常終了', errMsg)

root = Tk()
root.title('image-downloader')
root.geometry('550x140')

#画像を取得するサイトのURL入力欄
urlLabel = Label(root, text='画像を取得するサイトのURLを入力してください。(必須)')
urlLabel.place(x=10, y=0)
urlText = Entry(width=80)
urlText.place(x=10, y=20)

#保存先パス
pathLabel = Label(root, text="取得した画像の保存先を選択してください。(必須)")
pathLabel.place(x=10, y=50)
pathText = Entry(width=80)
pathText.place(x=10, y=70)
pathButton = Button(root, text='参照', command=pathButton_click)
pathButton.place(x=500, y=65)

#ダウンロード実行ボタン
downloadButton = Button(root, text='ダウンロード開始', command=downloadButton_click)
downloadButton.place(x=200, y=100)

#終了ボタン
exitButton = Button(root, text='終了', command=exitButton_click)
exitButton.place(x=300, y=100)

root.mainloop()

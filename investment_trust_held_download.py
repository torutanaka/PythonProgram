#某証券会社のサイトから投資信託の保有残高情報を取得する

from tkinter import *
from tkinter import messagebox, filedialog
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import traceback
import csv
import datetime
from selenium.webdriver.common.keys import Keys
import threading

#投資信託保有残高照会処理
def inquiryInvestmentTrustHeld(csvPath):
    try:
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe',chrome_options=options)

        #ログイン画面にアクセスする
        driver.get('https://???')

        #「ログインID」「パスワード」入力してログインする
        driver.find_element_by_id('loginid').send_keys('???')
        driver.find_element_by_id('passwd').send_keys('???')
        driver.find_element_by_id('passwd').send_keys(Keys.ENTER)

        #「保有残高・口座管理」ボタンをクリックする
        driver.find_element_by_class_name('nav02').click()

        #投資信託の総額を取得する
        contents = driver.find_element_by_name('contents').find_elements_by_class_name('mod-num-block')
        total = []
        #時価総額
        total.append(contents[2].text)
        #評価損益
        total.append(contents[3].text)
        rows = []
        rows.append(total)

        #画面に表示されている内容から、投資信託保留残高の情報を作成する
        detailRows = driver.find_elements_by_class_name('table-block')[1].find_elements_by_tag_name('tr')
        i = 0
        for detailRow in detailRows:
            if i == 0:
                #ヘッダー
                tds = detailRow.find_elements_by_tag_name('th')
                i += 1
            else:
                #明細
                tds = detailRow.find_elements_by_tag_name('td')

            outputRow = []
            #銘柄名
            outputRow.append(tds[0].text)
            #口座区分
            outputRow.append(tds[1].text.split('\n')[0])
            #預り区分
            outputRow.append(tds[1].text.split('\n')[1])
            #基準価額
            outputRow.append(tds[2].text)
            #一般累投区分
            outputRow.append(tds[3].text.replace('\n',''))
            #保有数
            outputRow.append(tds[4].text.split('\n')[0])
            #発注数
            outputRow.append(tds[4].text.split('\n')[1])
            #移動数
            outputRow.append(tds[4].text.split('\n')[2])
            #平均取得単価
            outputRow.append(tds[5].text.replace('\n',''))
            #概算評価額
            outputRow.append(tds[6].text.replace('\n',''))
            #概算評価損益
            outputRow.append(tds[7].text)
            rows.append(outputRow)

        #投資信託保有残高をCSVファイルに出力する
        with open(csvPath, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(rows)

        messagebox.showinfo('ダウンロード完了', '投資信託保有残高のダウンロードが完了しました。')

    except:
        messagebox.showerror('異常終了', '例外が発生しました。\n(' + traceback.format_exc() + ')')

    finally:
        if driver is not None:
            driver.quit()

#「投資信託保有残高をダウンロード」ボタン押下時処理
def investmentTrustHeld_click():
    if not pathText.get():
        messagebox.showwarning('保存先未設定', '投資信託保有残高の保存先を設定してください。')
        return

    #投資信託保有残高照会処理を別スレッドで実行
    ymdHMS = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    csvPath = pathText.get() + '\\InvestmentTrustHeld' + ymdHMS + '.csv'
    th = threading.Thread(target=inquiryInvestmentTrustHeld, args=([csvPath]))
    th.start()

#「参照」ボタン押下時処理
def pathButton_click():
    #フォルダ選択のダイアログを開き、選択したパスを画面に設定する
    iDir = os.path.abspath(os.path.dirname(__file__))
    dir = filedialog.askdirectory(initialdir=iDir)
    pathText.delete(0, END)
    pathText.insert(0, dir)

#「終了」ボタン押下時処理
def exitButton_click():
    quit()

root = Tk()
root.title('investment_trust_held_download')
root.geometry('550x100')

#保存先パス
pathLabel = Label(root, text="投資信託保有残高の保存先を選択してください。(必須)")
pathLabel.place(x=10, y=10)
pathText = Entry(width=80)
pathText.place(x=10, y=30)
pathButton = Button(root, text='参照', command=pathButton_click)
pathButton.place(x=500, y=25)

#「投資信託保有残高をダウンロード」ボタン
investmentTrustHeldButton = Button(root, text='投資信託保有残高をダウンロード', command=investmentTrustHeld_click)
investmentTrustHeldButton.place(x=200, y=60)

#「終了」ボタン
exitButton = Button(root, text='終了', command=exitButton_click)
exitButton.place(x=370, y=60)

root.mainloop()
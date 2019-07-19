#某銀行のインターネットバンキングにログインし、入出金明細の情報を取得してCSVファイルに保存する

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import csv
import os
from tkinter import *
from tkinter import filedialog,messagebox,Radiobutton
import datetime
import traceback
from dateutil.relativedelta import relativedelta

#入出金明細のダウンロード処理
def downloadPaymentDetails(isThisMonth, csvPath):
    try:
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe',chrome_options=options)
        #ログイン画面にアクセスする
        driver.get('https://????.co.jp/ibg/')

        #ログイン情報を入力し、エンターキー押下でログインする
        driver.find_element_by_id('account_id').send_keys('xxxx')
        driver.find_element_by_id('ib_password').send_keys('XXXX')
        driver.find_element_by_id('ib_password').send_keys(Keys.ENTER)

        #「入出金明細を見る」ボタンを押下して画面遷移する
        driver.find_elements_by_tag_name('li')[1].click()

        #今月または前月を選択する
        if isThisMonth:
            driver.find_element_by_id('this_month').click()
        else:
            driver.find_element_by_id('last_month').click()

        #「照会」ボタン押下で画面を再表示させる
        driver.find_elements_by_class_name('button')[0].click()

        #入出金明細を作成する
        with open(csvPath, 'w', newline='') as csv_file:
            #入出金明細全体の情報を取得する
            table = driver.find_element_by_id('no_memo').find_elements_by_tag_name('table')[2]

            #入出金明細のヘッダーの情報を取得する
            ths = table.find_element_by_tag_name('thead').find_elements_by_tag_name('th')
            rows = []
            rows.append([ths[0].text, ths[1].text, ths[2].text, ths[3].text, ths[4].text])

            #入出金明細の明細の情報を取得する
            trs = table.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
            for tr in trs:
                tds = tr.find_elements_by_tag_name('td')
                rows.append([tds[0].text.replace('\n',''), tds[1].text, tds[2].text, tds[3].text, tds[4].text])

            #取得したヘッダーと明細の情報をCSVファイルに書き込む
            writer = csv.writer(csv_file)
            writer.writerows(rows)
    except:
        return traceback.format_exc()

    finally:
        if driver is not None:
            driver.quit()

#参照ボタン押下時処理
def pathButton_click():
    #フォルダ選択のダイアログを開き、選択したパスを画面に設定する
    iDir = os.path.abspath(os.path.dirname(__file__))
    dir = filedialog.askdirectory(initialdir=iDir)
    pathText.insert(0, dir)

#「入出金明細をダウンロード」ボタン押下時処理
def downloadPaymentDetailsButton_click():
    if not pathText.get():
        messagebox.showwarning('保存先未設定', '入出金明細の保存先を設定してください。')
        return

    now = datetime.datetime.now()
    if var.get() == 0:
        #今月の入出金明細をダウンロードする
        isThisMonth = True
        yearMonth = now.strftime('%Y%m')
    else:
        #前月の入出金明細をダウンロードする
        isThisMonth = False
        yearMonth = (now - relativedelta(months=1)).strftime('%Y%m')

    csvPath = pathText.get() + '\\入出金明細' + yearMonth + '.csv'
    result = downloadPaymentDetails(isThisMonth, csvPath)

    if result:
        messagebox.showerror('異常終了', '例外が発生しました。\n(' + result + ')')
    else:
        messagebox.showinfo('ダウンロード完了', '入出金明細のダウンロードが完了しました。')

#終了ボタン押下時処理
def exitButton_click():
    if messagebox.askokcancel('終了','終了します。よろしいですか？')==True:
        quit()

root = Tk()
root.title('payment_details_download')
root.geometry('550x150')

#「出力期間」ダイアログ
var = IntVar()
var.set(0)
monthLabel = Label(root, text="入出金明細の出力期間を選択してください。")
monthLabel.place(x=10, y=10)
thisMonthRadiobutton = Radiobutton(root, value=0, variable=var, text='今月')
thisMonthRadiobutton.place(x=10, y=30)
lastMonthRadiobutton = Radiobutton(root, value=1, variable=var, text='前月')
lastMonthRadiobutton.place(x=60, y=30)

#保存先パス
pathLabel = Label(root, text="入出金明細の保存先を選択してください。(必須)")
pathLabel.place(x=10, y=60)
pathText = Entry(width=80)
pathText.place(x=10, y=80)
pathButton = Button(root, text='参照', command=pathButton_click)
pathButton.place(x=500, y=75)

#「入出金明細をダウンロード」ボタン
downloadPaymentDetailsButton = Button(root, text='入出金明細をダウンロード', command=downloadPaymentDetailsButton_click)
downloadPaymentDetailsButton.place(x=200, y=110)

#「終了」ボタン
exitButton = Button(root, text='終了', command=exitButton_click)
exitButton.place(x=350, y=110)

root.mainloop()
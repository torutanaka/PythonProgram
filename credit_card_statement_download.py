#某カード会社のサイトにアクセスし、クレジットカードの利用明細を取得する
import datetime
import os
from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tkinter import *
from tkinter import messagebox, filedialog
import traceback
import csv
from selenium.webdriver.common.keys import Keys
import threading

#「カード利用明細をダウンロード」ボタン押下時処理
def downloadCreditCardStatement(downloadMonth, csvPath):
    try:
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe',chrome_options=options)

        #ログイン画面にアクセスする
        driver.get('https://www.???.co.jp/')

        #「ユーザID」と「パスワード」を入力してログインする
        driver.find_element_by_id('u').send_keys('???')
        driver.find_element_by_name('p').send_keys('???')
        driver.find_element_by_name('p').send_keys(Keys.ENTER)

        #トップページの「明細を見る」ボタンを押下(ボタン押下できなくなったので、URLを指定して画面遷移)
        url = driver.find_element_by_id('js-bill-mask').find_element_by_class_name('rf-button-alt').get_attribute('href')
        driver.get(url)

        if downloadMonth == 1:
            #前月の明細を取得する場合は「前月」ボタンを押下する
            driver.find_element_by_class_name('stmt-calendar__cmd__prev').click()
        elif downloadMonth == 2:
            #翌月の明細を取得する場合は「次月」ボタンを押下する
            driver.find_element_by_class_name('stmt-calendar__cmd__next').click()

        #「詳細を全て見る」ボタンをクリックする
        driver.find_element_by_class_name('stmt-current-payment-list').find_element_by_tag_name('span').click()

        #画面に表示している内容から、利用明細の部分を取得する
        detailRows = driver.find_elements_by_class_name('stmt-payment-lists__i')

        rows = []
        #ヘッダー行を作成する
        rows.append(['利用日','利用店名・商品名','利用者','支払方法','利用金額','支払手数料','支払総額','当月支払金額','翌月繰越残高'])

        for detailRow in detailRows:
            #明細行の上段の上昇を取得する
            upperRow = detailRow.find_elements_by_class_name('stmt-payment-lists__data')
            #明細行の下段の上昇を取得する
            lowerRow = detailRow.find_elements_by_class_name('stmt-payment-lists__details__col')

            #明細行を作成する
            rows.append([upperRow[0].text, upperRow[1].text, upperRow[2].text, upperRow[3].text, upperRow[4].text,
                         lowerRow[0].text, lowerRow[1].text, lowerRow[2].text])

        #利用明細をCSVファイルに出力する
        with open(csvPath, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(rows)

        messagebox.showinfo('ダウンロード完了', '入出金明細のダウンロードが完了しました。')

    except:
        messagebox.showerror('異常終了', '例外が発生しました。\n(' + traceback.format_exc() + ')')

    finally:
        if driver is not None:
            driver.quit()

#「カード利用明細をダウンロード」ボタン押下時処理
def downloadCreditCardStatement_click():
    if not pathText.get():
        messagebox.showwarning('保存先未設定', 'カード利用明細の保存先を設定してください。')
        return

    now = datetime.datetime.now()
    downloadMonth = var.get()
    if downloadMonth == 0:
        #当月の利用明細をダウンロードする場合
        yearMonth = now.strftime('%Y%m')
    elif downloadMonth == 1:
        #前月の利用明細をダウンロードする場合
        yearMonth = (now - relativedelta(months=1)).strftime('%Y%m')
    else:
        #翌月の利用明細をダウンロードする場合
        yearMonth = (now - relativedelta(months=1)).strftime('%Y%m')

    #カード利用明細のダウンロードを別スレッドで実行
    csvPath = pathText.get() + '\\enavi' + yearMonth + '(9893).csv'
    th = threading.Thread(target=downloadCreditCardStatement, args=([downloadMonth, csvPath]))
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
root.title('credit_card_statement_download')
root.geometry('550x150')

#「出力期間」ダイアログ
var = IntVar()
var.set(0)
monthLabel = Label(root, text="利用明細の出力期間を選択してください。")
monthLabel.place(x=10, y=10)
thisMonthRadiobutton = Radiobutton(root, value=0, variable=var, text='当月')
thisMonthRadiobutton.place(x=10, y=30)
lastMonthRadiobutton = Radiobutton(root, value=1, variable=var, text='前月')
lastMonthRadiobutton.place(x=60, y=30)
nextMonthRadiobutton = Radiobutton(root, value=2, variable=var, text='翌月')
nextMonthRadiobutton.place(x=110, y=30)

#保存先パス
pathLabel = Label(root, text="利用明細の保存先を選択してください。(必須)")
pathLabel.place(x=10, y=60)
pathText = Entry(width=80)
pathText.place(x=10, y=80)
pathButton = Button(root, text='参照', command=pathButton_click)
pathButton.place(x=500, y=75)

#「カード利用明細をダウンロード」ボタン
downloadPaymentDetailsButton = Button(root, text='カード利用明細をダウンロード', command=downloadCreditCardStatement_click)
downloadPaymentDetailsButton.place(x=200, y=110)

#「終了」ボタン
exitButton = Button(root, text='終了', command=exitButton_click)
exitButton.place(x=350, y=110)

root.mainloop()
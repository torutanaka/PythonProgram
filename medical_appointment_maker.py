#某クリニックの診察予約を、予約が可能になり次第取る

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tkinter import *
from tkinter import messagebox
import traceback
from selenium.webdriver.support.ui import Select
import time
import threading

#診察予約取得処理
def makeMedicalAppointment(waitingTime):
    try:
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome('C:\chromedriver_win32\chromedriver.exe', chrome_options=options)
        #クリニックのトップページにアクセスする
        driver.get('https://???')

        #トップページに「いますぐ受付」ボタンが現れるまで、トップページを再表示させつつ指定秒数監視する(todo)
        _time = 1
        while True:
            driver.refresh()
            if len(driver.find_elements_by_id('aTRN')) > 0:
                break
            _time +=1
            if _time > int(waitingTime):
                messagebox.showerror('予約失敗', '待機時間内に予約可能になりませんでした。')
                return
            time.sleep(1)

        #「いますぐ受付」ボタン押下で画面遷移させる
        driver.find_element_by_id('aTRN').click()

        #「1人」を選択して、「次へ」ボタン押下で画面遷移させる
        rsvcnt = Select(driver.find_element_by_name('rsvcnt'))
        rsvcnt.select_by_value('1')
        driver.find_element_by_xpath("//input[@type='submit']").click()

        #「診察券番号」と「誕生日」を入力して、「次へ」ボタン押下で画面遷移させる
        driver.find_element_by_name('HOSID').send_keys('???')
        driver.find_element_by_name('b_date').send_keys('???')
        driver.find_element_by_xpath("//input[@type='submit']").click()

        #「はい」ボタン押下で画面遷移させる
        driver.find_element_by_partial_link_text('はい').click()

        #「次へ」ボタン押下で予約を完了させる
        driver.find_element_by_xpath("//input[@type='submit']").click()

        #何番目に予約が取れたか返却する
        messagebox.showinfo('予約完了', '予約が完了しました。' + driver.find_elements_by_tag_name('font')[2].text + 'です。')

    except:
        messagebox.showerror('予約失敗', '例外が発生しました。\n(' + traceback.format_exc() + ')')

    finally:
        if driver is not None:
            driver.quit()

#「診察予約」ボタン押下時処理
def medicalAppointmentButton_click():
    waitingTime = waitingTimeText.get()
    if not waitingTime:
        messagebox.showwarning('待機時間未設定', '待機時間を入力してください。')
        return

    if waitingTime.isdecimal():
        #待機時間が正しく入力されていれば、予約処理を開始する
        th = threading.Thread(target=makeMedicalAppointment, args=([waitingTime]))
        th.start()
    else:
        messagebox.showwarning('待機時間入力エラー', '待機時間は数値を入力してください。')
        return

#終了ボタン押下時処理
def exitButton_click():
    quit()

root = Tk()
root.title('medical_appointment_maker')
root.geometry('350x120')

#待機時間
waitingTimeLabel = Label(root, text="予約ができない場合の待機時間を入力してください。(単位は秒)")
waitingTimeLabel.place(x=10, y=10)
waitingTimeText = Entry(width=5)
waitingTimeText.place(x=120, y=40)

#「診察予約」ボタン
medicalAppointmentButton = Button(root, text='診察予約', command=medicalAppointmentButton_click)
medicalAppointmentButton.place(x=160, y=40)

#「終了」ボタン
exitButton = Button(root, text='終了', command=exitButton_click)
exitButton.place(x=280, y=80)

root.mainloop()


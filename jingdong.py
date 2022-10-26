import csv
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

import requests
from bs4 import BeautifulSoup


class GetJingDong():
    '''获取京东数据'''
    def __init__(self, name, pages):
        '''初始化'''
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
        self.name = name
        self.pages = pages

    def get_info(self):
        '''获取数据并写入csv文件'''
        date_time = datetime.now().strftime("%Y%m%d%H%M%S")  # 获取当前时间并格式化
        url_list = []  # 把爬取页的地址传入列表
        num = 1  # 初始化第一页
        count = 1  # 序号
        head = ['序号', '商品信息', '价格', '促销信息', '链接地址', '店铺名称', '店铺类型及优惠']
        with open(f"./{self.name}_{date_time}.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(head)
            for i in range(int(self.pages)):  # 循环爬取页数并添加到列表
                url = f'https://search.jd.com/Search?keyword={self.name}&psort=3&wq={self.name}&psort=3&pvid=ee543333173345a3972a25a46de9a736&page={i + 1}&s={num}&click=0'
                url_list.append(url)
                num += 30  # 次页增量
            for url in url_list:
                res = requests.get(url, headers=self.headers)
                res.content.decode("utf8")  # 页面编码
                res_text = BeautifulSoup(res.text, 'html.parser')
                commodityinfo = res_text.find_all('div', class_='gl-i-wrap')
                for info in commodityinfo:
                    try:
                        title = info.find('div', class_="p-name p-name-type-2").find('em').text.replace(' ', '').replace(
                            '\n', '').replace("¥", '')  # 商品信息
                        Promotional = info.find('div', class_="p-name p-name-type-2").find('a')['title'].replace(' ',
                                                                                                                 '').replace(
                            '\n', '').replace("¥", '')  # 促销信息
                        Price = info.find('strong').text.replace(' ', '').replace('\n', '').replace("¥", '')  # 价格
                        link = "https:" + info.find('div', class_="p-name p-name-type-2").find('a')['href'].replace(' ',
                                                                                                                    '').replace(
                            '\n', '')  # 连接
                        shop = info.find('span', class_='J_im_icon').find('a')['title'].replace(' ', '').replace('\n',
                                                                                                                 '')  # 店铺
                        shoptype = info.find('div', class_='p-icons').text.replace(' ', '').replace('\n', '')  # 店铺类型
                    except Exception as e:
                        print(e)
                        pass
                    print(count, title, Price, Promotional, link, shop, shoptype)
                    try:
                        writer.writerow([count, title, Price, Promotional, link, shop, shoptype])  #写入csv
                    except:
                        print("-----写入出错-----")
                        pass
                    count += 1#序号增量
                    time.sleep(0.5)


class Tk_JingDong():

    def start(self, *args):
        try:
            jingdong=GetJingDong(enfocus.get(),enpages.get())
            jingdong.get_info()
            tk.messagebox.showinfo("消息提示", "抓取完成!")
        except Exception as e:
            print(e)
            tk.messagebox.showerror("消息提示", "抓取失败!")

    def key(self):
        bt1 = tk.Button(text="抓  取", width=12, height=1)
        bt1.grid(row=2, column=1, padx=(10, 0), pady=10)

        # 当按下鼠标左键的时候，按钮触发方法
        bt1.bind("<Button-1>", self.start)

    def jd_win(self):
        global enfocus, enpages
        win = tk.Tk()  # 创一个窗口的对象
        win.title("京东数据抓取工具")  # 设置窗体的标题

        scrw = win.winfo_screenwidth()  # 获取屏幕宽度
        scrh = win.winfo_screenheight()  # 获取屏幕高度
        x = (scrw - 480) // 2
        y = (scrh - 200) // 2
        win.geometry(f"400x200+{x}+{y}")  # 设置窗口大小,并设置离屏边缘距离
        win.resizable(False, False)  # 禁止设置窗口大小

        date = tk.Label(win, text='关键字：')
        date.grid(row=0, column=0, pady=10, )
        enfocus = tk.Entry(win)
        enfocus.grid(row=0, column=1, ipadx=60, pady=10)

        pages = tk.Label(win, text="页数（每页30条）")
        pages.grid(row=1, column=0, pady=10)
        enpages = tk.Entry(win)
        enpages.grid(row=1, column=1, ipadx=60, pady=10)

        self.key()

        win.mainloop()  # 主程序
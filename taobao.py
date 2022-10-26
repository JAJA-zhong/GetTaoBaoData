import csv
import json
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

import requests


class GetTaoBao:
    '''抓取淘宝数据'''

    def __init__(self, name, date_time):
        '''初始化'''
        self.name = name
        self.date_time = date_time

    def get_info(self, data_value):
        '''淘宝有反爬，获取网页数据需要传入params、cookie和referer
        data_value是动态，44和88，步长设置为44'''
        params = {
            "data-key": "s",
            "data-value": data_value,
            "ajax": "true",
            "q": self.name,
            "js": 1,
            "stats_click": "search_radio_all%3A1",
            "initiative_id": f"staobaoz_{self.date_time[:8]}",  # 日期
            "ie": "utf8",
            "sort": "sale-desc"  # 以销量倒序
        }
        start_url = "https://s.taobao.com/search?"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "cookie": r"",
            "referer": "https://s.taobao.com/search?q=&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20210303&ie=utf8&sort=sale-desc"
        }
        r = requests.get(start_url, headers=headers, params=params)
        if r.status_code == 200:
            content_dict = json.loads(r.text)  # json字典格式化
            content = content_dict["mods"]["itemlist"]["data"]["auctions"]  # 获取数据
            for data in content:
                name = data["raw_title"]  # 宝贝名称
                price = data["view_price"]  # 价格
                number = data["view_sales"]  # 收货人数
                nick = data['nick']  # 店铺名称
                icon = data['icon']  # 卖家类型
                inner = ""
                for innerText in icon:
                    inner += innerText['innerText'] + '--'
                item_loc = data['item_loc']  # 发货地址
                detail_url = "https:" + data['detail_url']  # 宝贝地址
                pic_url = "https:" + data['pic_url']  # 图片地址
                time.sleep(0.5)
                print(name, price, number, nick, inner, item_loc, detail_url, pic_url)
            return content
        else:
            return ""

    def GoodList(self, data):
        count = 0  # 序号
        head = ['序号', '宝贝名称', '价格', '收货人数', '店铺名称', '卖家类型', '发货地址', '宝贝地址', '图片地址']
        with open(f"./{self.name}_{self.date_time}.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(head)
            for content in data:
                count += 1
                name = content["raw_title"].replace(' ', '').replace('丨', '')
                price = content["view_price"]  # 价格
                number = content["view_sales"]  # 收货人数
                nick = content['nick']  # 店铺名称

                icon = content['icon']  # 卖家类型
                inner = ""
                for innerText in icon:
                    inner += innerText['innerText'] + '--'

                item_loc = content['item_loc']  # 发货地址
                detail_url = "https:" + content['detail_url']  # 宝贝地址
                pic_url = "https:" + content['pic_url']  # 图片地址
                try:
                    writer.writerow([count, name, price, number, nick, inner, item_loc, detail_url, pic_url])
                except:
                    print("-----写入出错-----")
                    pass
                time.sleep(0.02)


class Tk_TaoBao:

    def main(self, *args):
        date_time = datetime.now().strftime("%Y%m%d%H%M%S")
        try:
            datavalue = []  # 创建获取数据列表
            taobao = GetTaoBao(enfocus.get(), date_time)  # 实例化爬取类
            for data_value in range(0, ((int(enpages.get()) - 1) * 44 + 1), 44):  # 循环页
                datavalue = datavalue + taobao.get_info(data_value)  # 运行获取方法返回数据
            taobao.GoodList(datavalue)  # 写入数据CSV
            tk.messagebox.showinfo("消息提示", "抓取完成!")
        except:
            tk.messagebox.showerror("消息提示", "抓取失败!")

    def key(self):
        bt1 = tk.Button(text="抓  取", width=12, height=1)
        bt1.grid(row=2, column=1, padx=(10, 0), pady=10)

        # 当按下鼠标左键的时候，按钮触发方法
        bt1.bind("<Button-1>", self.main)

    def win(self):
        global enfocus, enpages
        win = tk.Tk()  # 创一个窗口的对象
        win.title("淘宝数据抓取工具")  # 设置窗体的标题

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

        pages = tk.Label(win, text="页数（每页44条）")
        pages.grid(row=1, column=0, pady=10)
        enpages = tk.Entry(win)
        enpages.grid(row=1, column=1, ipadx=60, pady=10)

        self.key()

        win.mainloop()  # 主程序
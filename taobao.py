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
        self.count = 1  # 序号
        TBhead = ['序号', '宝贝名称', '价格', '收货人数', '店铺名称', '卖家类型', '发货地址', '宝贝地址', '图片地址']
        with open(f"./淘宝_{self.name}_{self.date_time}.csv", "w", newline="",encoding='utf8') as f:
            writer = csv.writer(f)
            writer.writerow(TBhead)

    def get_info(self, page44):
        '''淘宝有反爬，获取网页数据需要传入params、cookie和referer
        data_value是动态，44和88，步长设置为44'''
        params = {
            "data-key": "s",
            "data-value": page44,  # 循环页步长
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
            "cookie": r"输入你的cookie",  # 必须输入cookie才能获取数据
            "referer": "https://s.taobao.com/search?q=&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20210303&ie=utf8&sort=sale-desc"
        }
        try:
            r_tb = requests.get(start_url, headers=headers, params=params)
            if r_tb.status_code == 200:
                content_dict = json.loads(r_tb.text)  # json字典格式化
                TBdata = content_dict["mods"]["itemlist"]["data"]["auctions"]  # 获取数据
                del r_tb,content_dict
                return TBdata
            else:
                return ""

        except Exception as e:
            print(f"爬取错误{e}")

    def tocsv(self,TBdata):
        with open(f"./淘宝_{self.name}_{self.date_time}.csv", "a", newline="",encoding='utf8') as f:
            writer = csv.writer(f)
            for iteam in TBdata:
                name = iteam["raw_title"].replace(' ', '').replace('丨', '')
                price = iteam["view_price"]  # 价格
                number = iteam["view_sales"]  # 收货人数
                nick = iteam['nick']  # 店铺名称
                icon = iteam['icon']  # 卖家类型
                inner = ""
                for innerText in icon:
                    inner += innerText['innerText'] + '--'
                item_loc = iteam['item_loc']  # 发货地址
                detail_url = "https:" + iteam['detail_url']  # 宝贝地址
                pic_url = "https:" + iteam['pic_url']  # 图片地址
                try:
                    print(self.count, name, price, number, nick, inner, item_loc)
                    writer.writerow([self.count, name, price, number, nick, inner, item_loc, detail_url, pic_url])
                except:
                    print("-----写入出错-----")
                    pass
                self.count += 1
                time.sleep(0.1)
        del TBdata


class Tk_TaoBao:
    '''GUI窗口'''

    def TBrun(self, *args):
        date_time = datetime.now().strftime("%Y%m%d%H%M%S")
        try:
            taobao = GetTaoBao(enfocus.get(), date_time)  # 实例化爬取类
            for page44 in range(0, ((int(enpage.get()) - 1) * 44 + 1), 44):  # 循环页
                TBdata = taobao.get_info(page44)  # 运行获取方法返回数据
                taobao.tocsv(TBdata)  # 写入数据CSV
            tk.messagebox.showinfo("消息提示", "抓取完成!")
            del taobao
        except Exception as e:
            print(e)
            tk.messagebox.showerror("消息提示", "抓取失败!")

    def TBkey(self):
        bt1 = tk.Button(text="抓  取", width=12, height=1)  # 定制按钮文字，大小
        bt1.grid(row=2, column=1, padx=(10, 0), pady=10)  # 放置按钮位置

        # 当按下鼠标左键的时候，按钮触发方法
        bt1.bind("<Button-1>", self.TBrun)

    def TBwin(self):
        global enfocus, enpage
        try:
            TBwin = tk.Tk()  # 创一个窗口的对象
            TBwin.title("淘宝数据抓取工具")  # 设置窗体的标题

            scrw = TBwin.winfo_screenwidth()  # 获取屏幕宽度
            scrh = TBwin.winfo_screenheight()  # 获取屏幕高度
            x = (scrw - 480) // 2
            y = (scrh - 200) // 2
            TBwin.geometry(f"400x200+{x}+{y}")  # 设置窗口大小,并设置离屏边缘距离
            TBwin.resizable(False, False)  # 禁止设置窗口大小

            key_str1 = tk.Label(TBwin, text='关键字：')  # 显示文字
            key_str1.grid(row=0, column=0, pady=10, )  # 放置关键字位置
            enfocus = tk.Entry(TBwin)  # 输入框
            enfocus.grid(row=0, column=1, ipadx=60, pady=10)  # 放置输入框位置

            key_str2 = tk.Label(TBwin, text="页数（每页44条）")
            key_str2.grid(row=1, column=0, pady=10)
            enpage = tk.Entry(TBwin)
            enpage.grid(row=1, column=1, ipadx=60, pady=10)

            self.TBkey()  # 按钮

            TBwin.mainloop()  # 主程序
        except Exception as e:
            print(f"运行错误{e}")

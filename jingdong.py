import csv
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

import requests
from bs4 import BeautifulSoup


class GetJingDong():
    '''获取京东数据'''

    def __init__(self, name, page):
        '''初始化'''
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
        self.name = name
        self.page = page
        self.date_time = datetime.now().strftime("%Y%m%d%H%M%S")  # 获取当前时间并格式化
        self.num = 1  # 初始化第一页
        self.count = 1  # 序号
        JDhead = ['序号', '商品信息', '价格', '促销信息', '链接地址', '店铺名称', '店铺类型及优惠']
        with open(f"./京东_{self.name}_{self.date_time}.csv", "w", newline="", encoding='utf8') as f:
            writer = csv.writer(f)
            writer.writerow(JDhead)

    def tocsv(self, JDdata, wri):
        '''获取数据并写入csv文件'''
        for iteam in JDdata:
            try:
                title = iteam.find('div', class_="p-name p-name-type-2").find('em').text.replace(' ', '').replace('\n',
                                                                                                                  '').replace(
                    "¥", '')  # 商品信息
                Promotional = iteam.find('div', class_="p-name p-name-type-2").find('a')['title'].replace(' ',
                                                                                                          '').replace(
                    '\n', '').replace("¥", '')  # 促销信息
                Price = iteam.find('strong').text.replace(' ', '').replace('\n', '').replace("¥", '')  # 价格
                link = "https:" + iteam.find('div', class_="p-name p-name-type-2").find('a')['href'].replace(' ',
                                                                                                             '').replace(
                    '\n', '')  # 连接
                shop = iteam.find('span', class_='J_im_icon').find('a')['title'].replace(' ', '').replace('\n',
                                                                                                          '')  # 店铺
                shoptype = iteam.find('div', class_='p-icons').text.replace(' ', '').replace('\n', '')  # 店铺类型
            except Exception as e:
                print(f"数据格式出错{e}")
                pass
            try:
                print(self.count, title, Price, Promotional, link, shop, shoptype)
                wri.writerow([self.count, title, Price, Promotional, link, shop, shoptype])  # 写入csv
            except Exception as e:
                print(f"-----写入出错-----{e}")
                pass
            self.count += 1  # 序号增量
            time.sleep(0.1)
        del JDdata

    def get_info(self):
        with open(f"./京东_{self.name}_{self.date_time}.csv", "a", newline="", encoding='utf8') as f:
            writer = csv.writer(f)
            try:
                for i in range(int(self.page)*2):  # 循环爬取页数并添加到列表
                    #销量倒序
                    url = f'https://search.jd.com/Search?keyword={self.name}&wq={self.name}&psort=3&pvid=ed58af233188428f9b2383aef9747036&page={i + 1}&s={self.num}&click=0'
                    r_jd = requests.get(url, headers=self.headers)
                    r_jd.content.decode("utf8")  # 页面编码
                    res_text = BeautifulSoup(r_jd.text, 'html.parser')
                    JDdata = res_text.find_all('div', class_='gl-i-wrap')
                    self.tocsv(JDdata, writer)
                    self.num += 30
                    del r_jd, res_text
            except Exception as e:
                print(f"爬取错误{e}")
                pass


class Tk_JingDong():

    def JDrun(self, *args):
        try:
            jingdong = GetJingDong(enfocus.get(), enpage.get())
            jingdong.get_info()
            tk.messagebox.showinfo("消息提示", "抓取完成!")
            del jingdong
        except Exception as e:
            print(e)
            tk.messagebox.showerror("消息提示", "抓取失败!")

    def key(self):
        bt1 = tk.Button(text="抓  取", width=12, height=1)
        bt1.grid(row=2, column=1, padx=(10, 0), pady=10)

        # 当按下鼠标左键的时候，按钮触发方法
        bt1.bind("<Button-1>", self.JDrun)

    def jd_win(self):
        global enfocus, enpage
        JDwin = tk.Tk()  # 创一个窗口的对象
        JDwin.title("京东数据抓取工具")  # 设置窗体的标题

        scrw = JDwin.winfo_screenwidth()  # 获取屏幕宽度
        scrh = JDwin.winfo_screenheight()  # 获取屏幕高度
        x = (scrw - 480) // 2
        y = (scrh - 200) // 2
        JDwin.geometry(f"400x200+{x}+{y}")  # 设置窗口大小,并设置离屏边缘距离
        JDwin.resizable(False, False)  # 禁止设置窗口大小

        key_str1 = tk.Label(JDwin, text='关键字：')
        key_str1.grid(row=0, column=0, pady=10, )
        enfocus = tk.Entry(JDwin)
        enfocus.grid(row=0, column=1, ipadx=60, pady=10)

        key_str2 = tk.Label(JDwin, text="页数（每页60条）")
        key_str2.grid(row=1, column=0, pady=10)
        enpage = tk.Entry(JDwin)
        enpage.grid(row=1, column=1, ipadx=60, pady=10)

        self.key()

        JDwin.mainloop()  # 主程序

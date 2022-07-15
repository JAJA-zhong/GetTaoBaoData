import csv
import json
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
import requests


class GetTaoBao:

    def __init__(self, name, date_time):
        self.name = name
        self.date_time = date_time

    def get_info(self, data_value):
        params = {
            "data-key": "s",
            "data-value": data_value,
            "ajax": "true",
            "q": self.name,
            "js": 1,
            "stats_click": "search_radio_all%3A1",
            "initiative_id": f"staobaoz_{self.date_time[:8]}",
            "ie": "utf8",
            "sort": "sale-desc"
        }
        start_url = "https://s.taobao.com/search?"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "cookie": r"cna=PM4PGe5IlzECAXQVD8EbXemH; tracknick=\u5BB6\u5BB6\u5546\u4E1A; "
                      r"_uab_collina=162821804995209647858107; miid=3757869492043328732; "
                      r"enc=osTaUsLgBp8ey9n6tnzhrr33Bt7yJEMpJ1b65a4m8BzhPSbNt5NwkOMyvCP/WvPANueaPUVZHo5kpTrsk6acaQ==; "
                      r"thw=cn; sgcookie=E100vaQIWQ+L5AdlAtTzSItnF+WUmeu2b+aETVugecU7YVRGjyo9QJURBD+E+NErKeUa+qAjq2FVZ+2PZ9W+/F5bWYlVGQhLrU8VWpv5Gqc/Xur7OFdB9EadynHwr37cdsA; "
                      r"uc3=lg2=URm48syIIVrSKA==&nk2=30tKUmiDUKc=&id2=UU6oKt9sUs63&vt3=F8dCvCPU0Pb02QvIZL8=; lgc=\u5BB6\u5BB6\u5546\u4E1A; "
                      r"uc4=nk4=0@3b8IvKu8JdBvtM3EChzCQ+AZNA==&id4=0@U2xlpFDZPEfPDETwMRxZRoDSHaM=; _cc_=VT5L2FSpdA==; mt=ci=-1_0; "
                      r"t=3169a7d30354ba7c68f00da216deda16; cookie2=25db1cb21dd854476591d79781a8734d; "
                      r"_tb_token_=7133576e31e4a; _m_h5_tk=4fa41447e4c9ffb5f100fcbc549943f7_165785545787; "
                      r"_m_h5_tk_enc=d858a7086419e1b3f7d98d8285790ad8; xlly_s=1; alitrackid=www.taobao.com; "
                      r"lastalitrackid=www.taobao.com; uc1=cookie14=UoexNTlbJMjAug==; JSESSIONID=7EFE1263A4A977076475A083876EFF95; "
                      r"isg=BObmTjUMuKHnu2xm_4FgzljyN1xoxyqBw2gALtCN64noU4RtOFJmkYlhr09feyKZ; "
                      r"l=eBIYydy7LfGLN59BBO5aourza77TwQAbzsPzaNbMiInca1PVtUs5KNCHHAVBSdtjgtfjyetzgmaXvdEDri4dg2HvCbKrCyCkQYvw-; "
                      r"tfstk=cVilBRGuV4zSRsDZL0ZWvtNsQ8OaOSUsDoj0L59N9lYgsk4UsfduNyWCKVk1Q7C."
            ,
            "referer": "https://s.taobao.com/search?q=&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20210303&ie=utf8&sort=sale-desc"
        }
        r = requests.get(start_url, headers=headers, params=params)
        if r.status_code == 200:
            content_json = r.text
            content_dict = json.loads(content_json)
            content = content_dict["mods"]["itemlist"]["data"]["auctions"]
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
                name = content["raw_title"]  # 宝贝名称
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

                writer.writerow([count, name, price, number, nick, inner, item_loc, detail_url, pic_url])
                print(count, name, price, number, nick, inner, item_loc, detail_url, pic_url)


class Tk_TaoBao:

    def main(self, *args):
        date_time = datetime.now().strftime("%Y%m%d%H%M%S")
        try:
            datavalue = []
            taobao = GetTaoBao(enfocus.get(), date_time)
            for data_value in range(0, ((int(enpages.get()) - 1) * 44 + 1), 44):
                datavalue = datavalue + taobao.get_info(data_value)
                time.sleep(1)
            taobao.GoodList(datavalue)
            tk.messagebox.showinfo("消息提示", "抓取成功!")
        except:
            tk.messagebox.showerror("消息提示", "抓取失败!")

    def key(self):
        bt1 = tk.Button(text="抓  取", width=12, height=1)
        bt1.grid(row=2, column=1, padx=(10, 0), pady=10)

        bt1.bind("<Button-1>", self.main)

    def win(self):
        global enfocus, enpages
        win = tk.Tk()
        win.title("淘宝数据抓取工具")

        scrw = win.winfo_screenwidth()
        scrh = win.winfo_screenheight()
        x = (scrw - 480) // 2
        y = (scrh - 200) // 2
        win.geometry(f"400x200+{x}+{y}")
        win.resizable(False, False)

        date = tk.Label(win, text='关键字：')
        date.grid(row=0, column=0, pady=10, )
        enfocus = tk.Entry(win)
        enfocus.grid(row=0, column=1, ipadx=60, pady=10)

        pages = tk.Label(win, text="页数（每页44）")
        pages.grid(row=1, column=0, pady=10)
        enpages = tk.Entry(win)
        enpages.grid(row=1, column=1, ipadx=60, pady=10)

        self.key()

        win.mainloop()  # 主程序


if __name__ == '__main__':
    win = Tk_TaoBao()
    win.win()

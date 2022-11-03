import time

import jingdong
import taobao


def tasl_type(num):
    try:
        if num == "1":
            jd = jingdong.Tk_JingDong()
            jd.jd_win()
            del jd
        elif num == "2":
            tb = taobao.Tk_TaoBao()  # GUI
            tb.TBwin()
            del tb
        else:
            print('输入错误，重新输入。')
    except Exception as e:
        print(f"运行错误{e}")


if __name__ == "__main__":
    while True:
        num = input('''
\033[1;34m输入运行任务：\033[0m
\033[4;32m1、京东\033[0m
\033[4;35m2、淘宝\033[0m
\033[1;31m退出输入exit\033[0m
你的选择是（1/2）：''')
        if num == "exit":
            print("感谢您的使用，再见！\n" * 3)
            time.sleep(2)
            break
        tasl_type(num)

import jingdong
import taobao

def main():
    jd=jingdong.Tk_JingDong()
    tb=taobao.Tk_TaoBao()
    while True:
        type = input('''
        输入运行任务：
        1、京东
        2、淘宝
        你的选择是（1/2）：''')
        if type =="1":
            jd.win()
        elif type =="2":
            tb.win()
        else:
            print('输入错误，重新输入')


if __name__ == "__main__":
    main()

from tkinter import filedialog
from tkinter import messagebox
from lxml import html
from glob import glob
import tkinter as tk
import threading
import requests
import time
import re
import os
import json
import random
import urllib.request

# 默認設定
template_RJ = 'workno title '  # 默認RJ命名模板(Voice)
template_BJ = 'workno title '  # 默認BJ命名模板(Comic)
template_VJ = 'workno title '  # 默認VJ命名模板(Game)

replace_rules = []  # 替換規則

RJ_WEBPATH = 'https://www.dlsite.com/maniax/work/=/product_id/'
RJ_G_WEBPATH = 'https://www.dlsite.com/home/work/=/product_id/'
BJ_WEBPATH = 'https://www.dlsite.com/books/work/=/product_id/'
BJ_G_WEBPATH = 'https://www.dlsite.com/comic/work/=/product_id/'
VJ_WEBPATH = 'https://www.dlsite.com/pro/work/=/product_id/'
VJ_G_WEBPATH = 'https://www.dlsite.com/soft/work/=/product_id/'
R_COOKIE = {'adultchecked': '1'}

# re.compile()返回一個匹配對像
# ensure path name is exactly RJ\d\d\d\d\d\d or BJ\d\d\d\d\d\d or VJ\d\d\d\d\d\d
pattern = re.compile("[BRV][EJ]\d+|$")
pattern6 = re.compile("[BRV][EJ]\d{6}|$")
pattern8 = re.compile("[BRV][EJ]\d{8}|$")

# filter to substitute illegal filenanme characters to " "
filter = re.compile('[\\\/:"*?<>|]+')


# 避免ERROR: Max retries exceeded with url
requests.adapters.DEFAULT_RETRIES = 5  # 增加重連次數
s = requests.session()
s.keep_alive = False  # 關閉多餘連接
# s.get(url) # 你需要的網址

# 查找母串內所有子串的位置, 查找失敗返回-1

# Random User Agent List
USER_AGENT_LIST = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    ]

USER_AGENT = random.choice(USER_AGENT_LIST)
headers = {
 'user-agent': USER_AGENT
}


# 把字串半形轉全形
def strB2Q(s):
    rstring = ""
    for uchar in s:
        u_code = ord(uchar)
        if u_code == 32:  # 全形空格直接轉換
            u_code = 12288
        elif 33 <= u_code <= 126:  # 全形字元（除空格）根據關係轉化
            u_code += 65248
        rstring += chr(u_code)
    return rstring

def match_code(code):
    # requests函示庫是一個常用於http請求的模組
    if code[0] == "R":
        url = RJ_WEBPATH + code
    if code[0] == "B":
        url = BJ_WEBPATH + code
    if code[0] == "V":
        url = VJ_WEBPATH + code
    try:
        # allow_redirects=False 禁止重定向
        r = s.get(url, allow_redirects=False, cookies=R_COOKIE, headers=headers)
        # HTTP狀態碼==200表示請求成功
        if r.status_code != 200:
            #print("    Status code:", r.status_code, "\nurl:", url)
            try:
                ## 改成一般向網址
                if code[0] == "R":
                    url = RJ_G_WEBPATH + code
                if code[0] == "B":
                    url = BJ_G_WEBPATH + code
                if code[0] == "V":
                    url = VJ_G_WEBPATH + code
                r = s.get(url, allow_redirects=False, cookies=R_COOKIE)
                if r.status_code != 200:
                    return r.status_code, "", "", "", [], [], "", "", ""
            except os.error as err:
                text.insert(tk.END, "**請求超時1!\n")
                text.insert(tk.END, "  請檢查網絡連接\n")
                return "", "", "", "", [], [], "", "", ""

        # fromstring()在解析xml格式時, 將字串轉換為Element對像, 解析樹的根節點
        # 在python中, 對get請求返回的r.content做fromstring()處理, 可以方便進行後續的xpath()定位等
        tree = html.fromstring(r.content)
        try:
            img_url = tree.xpath('//meta[@name="twitter:image:src"]/@content')[0]
        except os.error as err:
            text.insert(tk.END, "**作品封面不存在!\n")
            img_url = ""
        title = tree.xpath('//h1[@id="work_name"]/text()')[0]
        circle = tree.xpath(
            '//span[@itemprop="brand" and @class="maker_name"]/*/text()')[0]
        cvList = tree.xpath(
            '//*[@id="work_outline"]/tr/th[contains(text(), "声優")]/../td/a/text()')
        authorList = tree.xpath(
            '//*[@id="work_maker"]/tr/th[contains(text(), "著者")]/../td/a/text()')
        type = tree.xpath(
            '//*[@id="work_outline"]/tr/th[contains(text(), "作品形式")]/../td/div/a/span/text()')[0]
        # 精簡遊戲類型
        game_type_list = ["アクション", "クイズ", "アドベンチャー", "ロールプレイング", "テーブル", "デジタルノベル", "シミュレーション", "タイピング", "シューティング", "パズル", "その他ゲーム"]
        if type in game_type_list:
            type = "ゲーム"
        
        work_age = tree.xpath(
            '//*[@id="work_outline"]/tr/th[contains(text(), "年齢指定")]/../td/div/a/span/text()')
        if not work_age:
            work_age = tree.xpath(
                '//*[@id="work_outline"]/tr/th[contains(text(), "年齢指定")]/../td/div/span/text()')
        release_date = tree.xpath(
            '//*[@id="work_outline"]/tr/th[contains(text(), "販売日")]/../td/a/text()')[0]
        # 精簡日期: 20ab年cd月ef日 => abcdef
        if len(release_date) >= 11:
            release_date = release_date[2]+release_date[3]+release_date[5]+release_date[6]+release_date[8]+release_date[9]

        return 200, img_url, title, circle, cvList, authorList, work_age[0], release_date, type

    except os.error as err:
        text.insert(tk.END, "**請求超時2!\n")
        text.insert(tk.END, "  請檢查網絡連接\n")
        return "", "", "", "", [], [], "", "", ""

def nameChange():
    # askdirectory()檔案對話框, 選擇目錄, 返回目錄名
    path = filedialog.askdirectory()
    if path == "":
        messagebox.showinfo(title="錯誤", message="請選擇路徑!" + "\n")
    else:
        cbtn_deltext.config(state=tk.DISABLED)
        cbtn_dlcover.config(state=tk.DISABLED)
        cbtn_recursive.config(state=tk.DISABLED)
        btn.config(state=tk.DISABLED)
        btn['text'] = "等待完成"
        text.insert(tk.END, "選擇路徑: " + path + "\n")
        # os.listdir()返回指定的資料夾包含的檔案或資料夾的名字的列表
        if recursive.get(): # 遞迴檢索
            files = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*'))]
        else: # 根目錄檢索
            files = os.listdir(path)
        for file in files:
                if recursive.get(): # 遞迴檢索需要修正路徑
                    path = os.path.split(file)[0]
                # 嘗試獲取code
                code_len = len (re.findall(pattern, file.upper())[0])
                if code_len == 10:
                    code = re.findall(pattern8, file.upper())[0]
                elif code_len == 8:
                    code = re.findall(pattern6, file.upper())[0]
                else:
                    code = re.findall(pattern, file.upper())[0]

                # 如果沒能提取到code
                if not code:
                    continue  # 跳過該資料夾/檔案
                else:
                    #print('Processing: ' + code)
                    text.insert(tk.END, 'Processing: ' + code + '\n')
                    r_status, img_url, title, circle, cvList, authorList, work_age, release_date, type = match_code(code)
                    # 如果順利爬取網頁訊息
                    if r_status == 200 and title and circle:
                        if deltext.get():
                            # 刪除title中的【.*?】
                            title = re.sub(u"\\【.*?】", "", title)

                        if code[0] == "R":
                            new_name = template_RJ.replace("workno", code)
                        if code[0] == "B":
                            new_name = template_BJ.replace("workno", code)
                        if code[0] == "V":
                            new_name = template_VJ.replace("workno", code)

                        new_name = new_name.replace("title", title)
                        new_name = new_name.replace("circle", circle)
                        new_name = new_name.replace("work_age", work_age)
                        new_name = new_name.replace("release_date", release_date)
                        new_name = new_name.replace("type", type)

                        author = ""
                        if authorList:  # 如果authorList非空
                            for name in authorList:
                                author += "," + name
                            new_name = new_name.replace("author", author[1:])
                        else:
                            new_name = new_name.replace("(author)", "")  

                        cv = ""
                        if cvList:  # 如果cvList非空
                            for name in cvList:
                                cv += "," + name
                            new_name = new_name.replace("cv", cv[1:])
                        else:
                            new_name = new_name.replace("(CV. cv)", "")
                            

                        # 要下載封面且是資料夾
                        if dlcover.get() and img_url and os.path.isdir(os.path.join(path, file)):
                            try: # 嘗試下載封面
                                store_path = os.path.join(path, file, "cover.jpg")
                                if not os.path.isfile(store_path):
                                    text.insert(tk.END, "  下載封面...\n")
                                    urllib.request.urlretrieve(img_url, store_path)
                                else:
                                    text.insert(tk.END, "**封面已存在，跳過下載!\n")
                            except os.error as err:
                                text.insert(tk.END, "**下載封面過程中出現錯誤!\n")

                        # 1. 將Windows文件名中的非法字元替換成空白
                        # re.sub(pattern, repl, string)
                        # new_name = re.sub(filter, " ", new_name)
                          
                        # 1. 將Windows文件名中的非法字元替換成全形
                        # re.match(pattern, string, flags=0)
                        fixed_filename = "";
                        for char in new_name:
                            if re.match(filter, char):
                                fixed_filename += strB2Q(char)
                            else:
                                fixed_filename += char
                                
                        # 2. 多空格轉單空格
                        new_name = ' '.join(fixed_filename.split())

                        # 嘗試重命名
                        try:
                            # strip() 去掉字串兩邊的空格
                            if os.path.isfile(os.path.join(path, file)):  # 如果是檔案
                                temp, file_extension = os.path.splitext(file)
                                os.rename(os.path.join(path, file),
                                        os.path.join(path, new_name.strip()+file_extension))
                            else:  # 如果是資料夾
                                os.rename(os.path.join(path, file),
                                        os.path.join(path, new_name.strip()))
                        except os.error as err:
                            text.insert(tk.END, "**重命名失敗!\n")
                            text.insert(
                                tk.END, "  " + os.path.join(path, file) + "\n")
                            text.insert(tk.END, "  請檢查是否存在重複的名稱\n")
                    elif r_status == 404:
                        text.insert(tk.END, "**爬取DLsite過程中出現錯誤!\n")
                        text.insert(tk.END, "  請檢查本作是否已經下架或被收入合集\n")
                    elif r_status != "":
                        text.insert(tk.END, "**爬取DLsite過程中出現錯誤!\n")
                        text.insert(tk.END, "  網頁 URL: " +
                                    RJ_WEBPATH + code + "\n")
                        text.insert(tk.END, "  HTTP 狀態碼: " +
                                    str(r_status) + "\n")

                    # set delay to avoid being blocked from server
                    time.sleep(0.1)
        # print("~Finished.")
        text.insert(tk.END, "*******完成!*******\n\n\n\n")
        tk.messagebox.showinfo(title="提示", message="完成!")

        cbtn_deltext.config(state=tk.NORMAL)
        cbtn_dlcover.config(state=tk.NORMAL)
        cbtn_recursive.config(state=tk.NORMAL)
        btn.config(state=tk.NORMAL)
        btn['text'] = "選擇路徑"


def thread_it(func, *args):
    '''將函數打包進線程'''
    # 建立
    t = threading.Thread(target=func, args=args)
    # 守護 !!!
    t.setDaemon(True)
    # 啟動
    t.start()
    # 阻塞--卡死界面！
    # t.join()


root = tk.Tk()  # 實例化object，建立視窗root
root.title('DLsite重命名工具 v3.5')  # 給視窗的標題取名字
#root.eval('tk::PlaceWindow . center')
root.geometry('350x450')  # 設定視窗的大小(橫向 * 縱向)

text = tk.Text(root)
text.pack()

# 讀取配置文件
# os.path.dirname(__file__) 當前腳本所在路徑
basedir = os.path.abspath(os.path.dirname(__file__))
fname = os.path.join('config.json')
try:
    #fname = os.path.join(basedir, 'config.json')
    with open(fname, 'r', encoding='utf-8') as f:
        config = json.load(f)
        for tag in config['replace_rules']:  # 模板非空
            if ("workno" in tag['to']):
                if tag['type'] == "rj":
                    text.insert(tk.END, "**使用自定義RJ命名模板:\n")
                    template_RJ = tag['to']
                    text.insert(tk.END, "  " + template_RJ.strip() + "\n\n")
                if tag['type'] == "bj":
                    text.insert(tk.END, "**使用自定義BJ命名模板:\n")
                    template_BJ = tag['to']
                    text.insert(tk.END, "  " + template_BJ.strip() + "\n\n")
                if tag['type'] == "vj":
                    text.insert(tk.END, "**使用自定義VJ命名模板:\n")
                    template_VJ = tag['to']
                    text.insert(tk.END, "  " + template_VJ.strip() + "\n\n")
            else:
                text.insert(tk.END, "**模板格式錯誤: 模板中必須包含\"workno\"!\n")
                text.insert(tk.END, "  使用默認命名模板:\n")
                text.insert(tk.END, "  workno title \n\n")

            if 'proxy' in config and len(config['proxy']) > 0:
                text.insert(tk.END, "**使用代理:\n")
                text.insert(tk.END, "  " + config['proxy'] + "\n\n")
                proxies = {
                    "https": config['proxy'],
                    "http": config['proxy'],
                }

    if "replace_rules" in config and type(config["replace_rules"]) == list and len(config["replace_rules"]):
        replace_rules = config["replace_rules"]

except os.error as err:
    # 生成配置文件
    json_data = {
        "replace_rules":
        [
            {
                "type": "rj",
                "from": "",
                "to": "workno title ",
                "proxy": ""
            },
            {
                "type": "bj",
                "from": "",
                "to": "workno title ",
                "proxy": ""
            },
            {
                "type": "vj",
                "from": "",
                "to": "workno title ",
                "proxy": ""
            }
        ]
    }
    with open(fname, "w", encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, sort_keys=False,indent=4)
        text.insert(tk.END, "**使用默認命名模板:\n")
        text.insert(tk.END, "  workno title \n")

deltext = tk.IntVar()  # 定義整數變數用來存放選擇行為返回值
dlcover = tk.IntVar()
recursive = tk.IntVar()
cbtn_deltext = tk.Checkbutton(root, text='去除title中【】之間的內容', variable=deltext,
                      onvalue=1, offvalue=0)  # 傳值原理類似於radiobutton物件
cbtn_dlcover = tk.Checkbutton(root, text='下載封面', variable=dlcover,
                      onvalue=1, offvalue=0)
cbtn_recursive = tk.Checkbutton(root, text='遞迴檢索', variable=recursive,
                      onvalue=1, offvalue=0)                    

btn = tk.Button(root, text='選擇路徑', command=lambda: thread_it(nameChange))

btn.pack()
cbtn_deltext.pack()
cbtn_dlcover.pack()
cbtn_recursive.pack()

root.mainloop()

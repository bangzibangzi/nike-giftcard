import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import requests
import json
import openpyxl
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_balance(account, password, cookies):
    # 构造请求数据
    data = {
        "accountNumber": account,
        "currency": "CNY",
        "pin": password
    }
    # 构造请求头
    headers = {
        "Host": "api.nike.com.cn",
        "appId": "orders",
        "x-nike-visitorid": "6f5e1df0-0f45-465f-9578-e48e929ce73f",
        "Accept": "application/json",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "x-nike-visitid": "26",
        "Content-Type": "application/json",
        "Origin": "https://www.nike.com.cn",
        "Content-Length": "71"
    }
    # 发送请求
    response = requests.post("https://api.nike.com.cn/payment/giftcard_balance/v1/",
                             headers=headers, cookies=cookies, data=json.dumps(data))
    # 解析响应 json 数据，返回账号、密码和余额
    if response.status_code == 200:
        response_data = json.loads(response.text)
        balance = response_data.get("balance")
        return (account, password, balance)
    else:
        return (account, password, None)

def select_file():
    file_path = filedialog.askopenfilename()
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)

def start():
    # 读取 txt 文件，每行用 ":" 分割成账号和密码
    accounts = []
    with open(file_path_entry.get(), 'r', encoding='utf-8') as f:
        for line in f:
            account, password = line.strip().split(':')
            accounts.append((account, password))
    # 设置请求 cookie
    cookies = {
        "acw_sc__v2": cookie_entry.get()
    }
    # 创建线程池并提交任务
    results = []

def select_file():
    file_path = filedialog.askopenfilename()
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)

def start():
    # 读取 txt 文件，每行用 ":" 分割成账号和密码
    accounts = []
    with open(file_path_entry.get(), 'r', encoding='utf-8') as f:
        for line in f:
            account, password = line.strip().split(':')
            accounts.append((account, password))
    # 设置请求 cookie
    cookies = {
        "acw_sc__v2": cookie_entry.get()
    }
    # 创建线程池并提交任务
    results = []
    count = 0
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_balance,
                                   account, password, cookies) for account, password in accounts]
        for future in as_completed(futures):
            count += 1
            result = future.result()
            results.append(result)
            # 更新进度条
            progress_bar["value"] = count / len(accounts) * 100
            progress_bar.update()
    # 将结果写入 txt 文件
    with open("result.txt", 'w', encoding='utf-8') as f:
        for result in results:
            f.write(f"{result[0]}	{result[1]}	{result[2]}\n")
    messagebox.showinfo("提示", "查询完成！")

# 创建主窗口
window = tk.Tk()
window.title("Nike礼品卡余额查询")
window.geometry("400x300")

# 创建文件路径输入框和选择文件按钮
file_path_label = tk.Label(window, text="文件路径：")
file_path_label.pack()
file_path_entry = tk.Entry(window, width=30)
file_path_entry.pack()
select_file_button = tk.Button(window, text="选择文件", command=select_file)
select_file_button.pack()

# 创建 cookie 输入框
cookie_label = tk.Label(window, text="Cookie：")
cookie_label.pack()
cookie_entry = tk.Entry(window, width=30)
cookie_entry.pack()

# 创建开始按钮
start_button = tk.Button(window, text="开始查询", command=start)
start_button.pack()

# 创建进度条
progress_bar = tk.ttk.Progressbar(window, length=200, mode="determinate")
progress_bar.pack()

window.mainloop()

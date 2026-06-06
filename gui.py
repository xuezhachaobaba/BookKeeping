import customtkinter as ctk
#退出程序
def quit_record():
    print("退出记账本，感谢使用！")
    exit()

app = ctk.CTk()
app.title("记账本")
app.geometry("500x450")

title = ctk.CTkLabel(app,text="=====记账本=====",font=ctk.CTkFont(size=20))
title.pack(pady = 12)

btn1 = ctk.CTkButton(app,text="1. 记一笔",width=200)
btn1.pack(pady = 8)

btn2 = ctk.CTkButton(app,text="2. 查看所有记录",width=200)
btn2.pack(pady = 8)

btn3 = ctk.CTkButton(app,text="3. 查看本月统计",width=200)
btn3.pack(pady = 8)

btn4 = ctk.CTkButton(app,text="4. 按类型统计支出",width=200)
btn4.pack(pady = 8)

btn5 = ctk.CTkButton(app,text="5. 搜索记录",width=200)
btn5.pack(pady = 8)

btn6 = ctk.CTkButton(app,text="6. 删除记录",width=200)
btn6.pack(pady = 8)

btn7 = ctk.CTkButton(app,text="7. 修改记录",width=200)
btn7.pack(pady = 8)

btn8 = ctk.CTkButton(app,text="8. 退出",width=200,command = quit_record)
btn8.pack(pady = 8)

app.mainloop()

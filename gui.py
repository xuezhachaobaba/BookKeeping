import customtkinter as ctk
import json
from datetime import datetime

records = []
with open("records.json","r",encoding="utf-8") as f:
    records = (json.load(f))

#退出程序
def quit_record():
    exit()

#将记录保存进本地json
def Save_date():
    with open("records.json","w",encoding="utf-8") as f:
        json.dump(records,f,ensure_ascii=False,indent=4)


def record_transaction():
    def r_save_fuc():
        t_type = r_Typ.get()
        amount = r_amount.get()
        category = r_cate.get()
        note = r_note.get()
        times = datetime.now().strftime("%Y-%m-%d")
        try :
            amount = float(amount)
            record = {
                "type": t_type,
                "amount": amount,
                "category": category,
                "note": note,
                "time": times
            }
            records.append(record)
            Save_date()
            rec_tra.destroy()
            print("保存数据")
        except ValueError:
            print("请输入有效金额!!!!不保存数据")
        

    rec_tra = ctk.CTkToplevel()
    rec_tra.title("记一笔")
    rec_tra.geometry("400x300")

    rec_tra.grab_set()
    rec_tra.transient(app)

    r_Typ = ctk.CTkOptionMenu(rec_tra,values=["收入","支出"])
    r_Typ.set("支出")
    r_Typ.pack()

    r_amount = ctk.CTkEntry(rec_tra,placeholder_text="请输入金额 ")
    r_amount.pack()

    r_category = ["餐饮","交通","购物","娱乐","工资"]
    r_cate = ctk.CTkOptionMenu(rec_tra,values=r_category)
    r_cate.set("餐饮")
    r_cate.pack()

    r_note = ctk.CTkEntry(rec_tra,placeholder_text="请输入备注 ")
    r_note.pack()
   
    r_save = ctk.CTkButton(rec_tra,text="保存",command=r_save_fuc)
    r_save.pack()

def view_all_records():
    rec_view_a = ctk.CTkToplevel()
    rec_view_a.title("查看所有记录")
    rec_view_a.geometry("600x400")
    rec_view_a.grab_set()
    rec_view_a.transient(app)
    
    text_box = ctk.CTkTextbox(rec_view_a,width=550, height=300)
    for idx,record in enumerate(records,1):
        temp_time = record.get("time","未知时间")
        text_box.insert(f"end",f"{idx}. {record['type']} - {record['amount']} - {record['category']} - {record['note']} - {temp_time}\n")
    text_box.configure(state="disabled")
    text_box.pack()

    r_shutup_Button = ctk.CTkButton(rec_view_a,text="关闭",command=rec_view_a.destroy)
    r_shutup_Button.pack()

def view_monthly_summary():
    rec_view_m = ctk.CTkToplevel()
    rec_view_m.title("查看本月统计")
    rec_view_m.geometry("500x400")
    rec_view_m.grab_set()
    rec_view_m.transient(app)

    text_box = ctk.CTkTextbox(rec_view_m,width=400,height=300)
    temptime = datetime.now()
    all_income = 0
    all_expense = 0
    for record in records:
        if not record.get("time"):
            continue
        if datetime.strptime(record.get("time"),"%Y-%m-%d").month != temptime.month:
            continue
        if record.get("type") == "收入":
            all_income += record.get("amount")
        if record.get("type") == "支出":
            all_expense += record.get("amount")
    all_balance = all_income - all_expense
    text_box.insert("end",f"{temptime.year}年{temptime.month}月数据统计如下\n")
    text_box.insert("end",f"月总收入为{all_income}\n")
    text_box.insert("end",f"月总支出为{all_expense}\n")
    text_box.insert("end",f"月总结余为{all_balance}\n")
    text_box.pack()

    r_button = ctk.CTkButton(rec_view_m,text="关闭",command=rec_view_m.destroy)
    r_button.pack()

def expense_category_stat():
    exp_cate_stat = ctk.CTkToplevel()
    exp_cate_stat.title("按分类统计支出")
    exp_cate_stat.grab_set()
    exp_cate_stat.transient(app)
    exp_cate_stat.geometry("500x400")

    text_box = ctk.CTkTextbox(exp_cate_stat,width=400,height=300)
    category_total = {}
    for record in records:
        if record.get("type") != "支出" :
            continue
        temp_category = record["category"]
        category_total[temp_category] = category_total.get(temp_category,0) + record["amount"]
    for key,value in category_total.items():
        text_box.insert("end",f"{key}的总支出为：{value}\n")
    text_box.pack()
    
    r_button = ctk.CTkButton(exp_cate_stat,text="关闭",command=exp_cate_stat.destroy)
    r_button.pack()

def research_of_category():
    res_cate = ctk.CTkToplevel()
    res_cate.title("搜索记录")
    res_cate.geometry("500x400")
    res_cate.grab_set()
    res_cate.transient(app)

    def res_of_category():
        res = ctk.CTkToplevel()
        res.title("按分类搜索")
        res.geometry("450x400")
        res.grab_set()
        res.transient(res_cate)

        text_box = ctk.CTkTextbox(res,width=400,height=300)
        text_box.pack(fill="both",expand=True)

        def res_of_cate():
            
            num = 0
            cate1 = entry1.get()
            text_box.configure(state="normal")
            text_box.delete("1.0","end")
            for record in records:
                if record["category"] == cate1:
                    num += 1
                    temptime = record.get("time","未知时间")
                    text_box.insert("end",f"{num}. {record['type']} - {record['amount']} - {record['category']} - {record['note']} - {temptime}\n")
            if num == 0:
                text_box.insert("end","没有该类型的数据")
            text_box.configure(state = "disabled")
            

        entry1 = ctk.CTkEntry(res,placeholder_text="请输入想搜索的类型: ")
        entry1.pack()
        
        but1 = ctk.CTkButton(res,text="搜索",command=res_of_cate)
        but1.pack()
        but2 = ctk.CTkButton(res,text="退出",command=res.destroy)
        but2.pack()

    def res_of_amount():
        res = ctk.CTkToplevel()
        res.title("按金额范围搜索")
        res.geometry("450x400")
        res.grab_set()
        res.transient(res_cate)

        text_box = ctk.CTkTextbox(res,width=400,height=300)
        text_box.pack(fill="both",expand=True)

        def res_amo():
            num = 0
            text_box.configure(state="normal")
            text_box.delete("1.0","end")
            min_amount = float(entry1.get())
            max_amount = float(entry2.get())
            for record in records:
                r_amount = record.get("amount")
                if r_amount >= min_amount and r_amount <= max_amount:
                    num = num + 1
                    temptime = record.get("time","未知时间")
                    text_box.insert("end",f"{num}. {record['type']} - {record['amount']} - {record['category']} - {record['note']} - {temptime}\n")
            if num == 0:
                text_box.insert("end","没有该金额范围的记录！ \n")
            text_box.configure(state="disabled")

        entry1 = ctk.CTkEntry(res,placeholder_text="请输入最小金额")
        entry1.pack()
        entry2 = ctk.CTkEntry(res,placeholder_text="请输入最大金额")
        entry2.pack()
        but1 = ctk.CTkButton(res,text="搜索",command=res_amo)
        but1.pack()
        but2 = ctk.CTkButton(res,text="退出",command=res.destroy)
        but2.pack()
        

    def res_of_datetime():
        res = ctk.CTkToplevel()
        res.title("按时间范围搜索")
        res.geometry("450x400")
        res.grab_set()
        res.transient(res_cate)

        text_box = ctk.CTkTextbox(res,width=400,height=300)
        text_box.pack()

        def res_time():
            text_box.configure(state = "normal")
            text_box.delete("1.0","end")
            start_time = datetime.strptime(entry1.get(),"%Y-%m-%d")
            end_time = datetime.strptime(entry2.get(),"%Y-%m-%d")
            num = 0
            for record in records:
                if not record.get("time"):
                    continue
                r_time = datetime.strptime(record.get("time"),"%Y-%m-%d")
                if r_time >= start_time and r_time <= end_time:
                    num = num + 1
                    text_box.insert("end",f"{num}. {record['type']} - {record['amount']} - {record['category']} - {record['note']} - {record["time"]}\n")
            if num == 0:
                text_box.insert("end","没有该日期范围的记录！ \n")
            text_box.configure(state = "disabled")
            pass

        entry1 = ctk.CTkEntry(res,placeholder_text="请输入开始时间")
        entry1.pack()
        entry2 = ctk.CTkEntry(res,placeholder_text="请输入结束时间")
        entry2.pack()
        but1 = ctk.CTkButton(res,text="搜索",command=res_time)
        but1.pack()
        but2 = ctk.CTkButton(res,text="退出",command=res.destroy)
        but2.pack()

    button1 = ctk.CTkButton(res_cate,text="1. 按分类搜索",command=res_of_category)
    button1.pack(pady = 8)

    button2 = ctk.CTkButton(res_cate,text="2. 按金额范围搜索",command=res_of_amount)
    button2.pack(pady = 8)

    button3 = ctk.CTkButton(res_cate,text="3. 按日期范围搜索",command=res_of_datetime)
    button3.pack(pady = 8)

    button4 = ctk.CTkButton(res_cate,text="4. 退出",command=res_cate.destroy)
    button4.pack(pady = 8)


    pass

app = ctk.CTk()
app.title("记账本")
app.geometry("500x450")

title = ctk.CTkLabel(app,text="=====记账本=====",font=ctk.CTkFont(size=20))
title.pack(pady = 12)

btn1 = ctk.CTkButton(app,text="1. 记一笔",width=200,command=record_transaction)
btn1.pack(pady = 8)

btn2 = ctk.CTkButton(app,text="2. 查看所有记录",width=200,command=view_all_records)
btn2.pack(pady = 8)

btn3 = ctk.CTkButton(app,text="3. 查看本月统计",width=200,command=view_monthly_summary)
btn3.pack(pady = 8)

btn4 = ctk.CTkButton(app,text="4. 按类型统计支出",width=200,command=expense_category_stat)
btn4.pack(pady = 8)

btn5 = ctk.CTkButton(app,text="5. 搜索记录",width=200,command=research_of_category)
btn5.pack(pady = 8)

btn6 = ctk.CTkButton(app,text="6. 删除记录",width=200)
btn6.pack(pady = 8)

btn7 = ctk.CTkButton(app,text="7. 修改记录",width=200)
btn7.pack(pady = 8)

btn8 = ctk.CTkButton(app,text="8. 退出",width=200,command = quit_record)
btn8.pack(pady = 8)

app.mainloop()

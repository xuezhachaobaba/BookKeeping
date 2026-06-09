import json
import os
import subprocess
from datetime import datetime

records = []
if os.path.exists("records.json"):
    with open("records.json", "r", encoding="utf-8") as f:
        records = json.load(f)

#===数据读写===
#将records内容写入文件
def write_records():
    with open("records.json","w",encoding="utf-8") as f:
        json.dump(records,f,ensure_ascii=False,indent=4)

#抽象出查找所有数据
def get_all_records():
    for idx, record in enumerate(records,1):
        time = record.get("time","未知时间")
        print(f"{idx}. {record['type']} - {record['amount']} - {record['category']} - {record['note']} - {time}")


#===输入辅助===
#添加新数据
def add_data(str1,str2,str3,str4):
    t_type = input(str1)
    amount = float(input(str2))
    category = input(str3)
    note = input(str4)
    create_time = datetime.now().strftime("%Y-%m-%d")
    record = {
        "type": t_type,
        "amount": amount,
        "category": category,
        "note": note,
        "time": create_time
    }
    return record

#验证用户输入的记录编号
def input_record_index(str_hint):
    while True:
        user_num =  int(input(str_hint))
        if user_num > len(records):
            print("记录没这么长,请输入长度内的数字")
            continue
        if user_num <= 0:
            print("请输入大于0的记录编号")
            continue
        break 
    return user_num

#获取日期
def get_user_date(str):
    while True:
        user_input = input(str)
        try:
            date_obj = datetime.strptime(user_input,"%Y-%m-%d")
            return date_obj
        except ValueError:
            print("格式错误! 请按YYYY-MM-DD 输入，例如 2026-06-05") 


#===功能函数===
#记账
def record_transaction():
    while True:
        print("======记账本======")
        record = add_data("记一笔什么？(收入还是支出)","金额是多少？","分类是什么？(餐饮/交通/购物...)","备注是什么？")
        records.append(record)
        write_records()
        print("记录成功！")
        continue_choice = input("是否需要继续下一笔记录？(是/否)")
        if continue_choice == "否":
            break

#删除记录
def delete_record():
    if len(records) == 0:
        print("记录为空,无法删除")
        return 
    get_all_records()
    str_hint = "请输入要删除的编号记录: "
    del_num = input_record_index(str_hint)
    if input("确认要删除这条记录吗？ (是/否) ") == "是":
        records.pop(del_num-1)
        print("删除成功")
        write_records()

#修改记录
def rec_record():
    if len(records) == 0:
        print("记录为空，无法修改")
        return
    get_all_records()
    str_hint = "请输入要修改的记录编号: "
    rec_num = input_record_index(str_hint)
    if input("确认要修改这条记录吗? (是/否)") == "是":
        record = add_data("修改类型为？(收入还是支出)","修改金额为？","修改分类为？(餐饮/交通/购物...)","修改备注为？")
        records[rec_num-1] = record
        print("修改成功")
        write_records() 

#查看所有记录
def view_all_records():
    print("======所有记录======")
    get_all_records()
    input("按回车键返回菜单")

#统计当月的数据
def view_monthly_summary():
    print("======本月统计======")
    #查看本月时间
    current_time = datetime.now()
    #计算总收入
    total_income = 0
    #计算总支出
    total_expense = 0
    for record in records:
        if not record.get("time"):
            continue
        if datetime.strptime(record.get("time"),"%Y-%m-%d").year != current_time.year:
            continue
        if datetime.strptime(record.get("time"),"%Y-%m-%d").month != current_time.month:
            continue
        if record["type"] == "收入" : 
            total_income += record["amount"]
        else :
            total_expense += record["amount"]
    total_balance = total_income - total_expense
    print(f"本月收入为:{total_income}")
    print(f"本月支出为:{total_expense}")
    print(f"结余为:{total_balance}")
    input("按回车键返回菜单")

#按分类统计支出
def expense_category_stat():
    print("======按分类统计支出======")
    category_total = {}
    for record in records:
        if record.get("type") != "支出" :
            continue
        temp_category = record["category"]
        category_total[temp_category] = category_total.get(temp_category,0) + record["amount"]
    for key,value in category_total.items():
        print(f"{key}的总支出为：{value}")
    input("按回车返回菜单")

#按分类搜索
def research_of_category():
    print("======按分类搜索======")
    research_cate = input("输入想搜索的类型: ")
    num = 0
    for record in records:
        if record["category"] == research_cate:
            num = num + 1
            temptime = record.get("time","未知时间")
            print(f"{num}. {record['type']} - {record['amount']} - {record['category']} - {record['note']} - {temptime}")
    if num == 0:
        print("没有该类型的记录！ ")
    input("请输入回车继续！ ")

#按金额范围搜索
def research_of_amount():
    print("======按金额范围搜索======")
    min_amount = float(input("请输入最小金额"))
    max_amount = float(input("请输入最大金额"))
    num = 0
    for record in records:
        r_amount = record.get("amount")
        if r_amount >= min_amount and r_amount <= max_amount:
            num = num + 1
            temptime = record.get("time","未知时间")
            print(f"{num}. {record['type']} - {record['amount']} - {record['category']} - {record['note']} - {temptime}")
    if num == 0:
        print("没有该金额范围的记录！ ")
    input("请输入回车继续！ ")


#按日期范围搜索
def research_of_datetime():
    print("======按日期范围搜索======")
    while True:
        start_date = get_user_date("请输入开始日期(格式:YYYY-MM-DD): ")
        end_date = get_user_date("请输入结束日期(格式:YYYY-MM-DD): ")
        if start_date <= end_date:
            break
        else:
            print("开始时间要在结束时间之前，请重新输入")
    num = 0
    for record in records:
        if not record.get("time"):
            continue
        r_time = datetime.strptime(record.get("time"),"%Y-%m-%d")
        if r_time >= start_date and r_time <= end_date:
            num = num + 1
            print(f"{num}. {record['type']} - {record['amount']} - {record['category']} - {record['note']} - {record["time"]}")
    if num == 0:
        print("没有该日期范围的记录！ ")
    input("请输入回车继续！ ")

#退出程序
def quit_record():
    print("退出记账本，感谢使用！")
    exit()

#清屏
def clean_screen():
    if os.name == 'nt':
        subprocess.run('cls', shell=True)
    else:
        subprocess.run('clear', shell=True)  

#===菜单===
#菜单
def menu():
    print("======记账本======")
    print("1. 记一笔")
    print("2. 查看所有记录")
    print("3. 查看本月统计(总收入、总支出、结余)")
    print("4. 按类型统计总支出")
    print("5. 搜索记录")
    print("6. 删除记录")
    print("7. 修改记录")
    print("8. 退出记账本")
    print("================")

#搜索菜单
def menu_of_research():
    print("======搜索记录======")
    print("1. 按分类搜索")
    print("2. 按金额范围搜索")
    print("3. 按日期范围搜索")
    print("4. 退出")
    print("================")

#菜单选择
def choice():
    option = input("请选择操作(1-8): ")
    match option:
        case "1":            record_transaction()
        case "2":            view_all_records()
        case "3":            view_monthly_summary()
        case "4":            expense_category_stat()
        case "5":            
            while True: 
                #clean_screen()
                menu_of_research()
                if research_choice():
                    break
        case "6":            delete_record()
        case "7":            rec_record()
        case "8":            quit_record()
        case _:              input("无效的选择，请重新输入！")

#搜索选择
def research_choice():
    option = input("请选择操作(1-4): ")
    match option:
        case "1":
            research_of_category() 
            return False
        case "2": 
            research_of_amount()
            return False
        case "3": 
            research_of_datetime()
            return False
        case "4": 
            return True
        case _: input("无效的选择,请重新输入! ")

def main():
    while True:
        clean_screen()    
        menu()
        choice()

if __name__ == "__main__":
    main()
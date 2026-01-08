import core.manager as manager

import utils.file_handler as file_hander

def main_menu():
    all_student = file_hander.load_data()

    while True:
        print("\n" + "="*30)
        print("     学生成绩管理系统 V6     ")
        print("="*30)
        print("1. 录入成绩 (Add)")
        print("2. 查看全班 (show)")
        print("3. 查找学生 (Search)")
        print("4. 删除学生 (Delete)")
        print("5. 成绩排序 (sort)")
        print("6. 保存退出 (Save & Exit)")
        print("="*30)

        choice = input("[提示] 请输入选项: ").strip()
        
        if choice == "1":
            all_student = manager.input_student(all_student)
        elif choice == "2":
            manager.show_all_students(all_student)
        elif choice == "3":
            s = manager.afind_student(all_student)
            if s:
                s.print_report()
        elif choice == "4":
            manager.delete_student(all_student)
        elif choice == "5":
            manager.sort_student(all_student)
        elif choice == "6":
            file_hander.save_data(all_student)
            print("[系统] 数据已保存，程序结束")
            break 
        else:
            print("[错误] 无效命令")  
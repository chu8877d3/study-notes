from models.student import Student

def input_student(student_list=None):
    '''
    用于循环录入对象学生;返回对象列表
    :param student_list: 输入和输出的都应该为对象列表
    '''
    if student_list is None:
        student_list = []

    print("请先设定本次录入的科目 (用空格隔开) ")
    subjects_input = input("科目列表:").strip()
    
    if not subjects_input:
        print("[提示] 未检测到科目输入, 将启用传统输入模式")
        subjects_template = []
    else:
        subjects_template = subjects_input.split()
        print(f"[系统] 已锁定科目: {subjects_template}")
    
    while True:
        name = input("请输入学生姓名:").strip()
        if name.lower() == "exit":
            break
        sex = input("性别:").strip()

        one_stu = Student(name, sex)

        if subjects_template:
            print(f"请输入 {name} 的成绩")
            for sub in subjects_template:
                while True:
                    try:
                        sc = float(input(f"{sub}成绩:").strip())
                        success = one_stu.add_score(sub, sc)
                        if success:
                            break
                    except ValueError:
                        print("[提示] 请输入数字")
                
        else:
            while True:
                sub = input("请输入科目:").strip()
                if sub.lower() == "exit":
                    break

                try:
                    sc = float(input(f"请输入{sub}成绩:").strip())
                    one_stu.add_score(sub, sc)
                    print(f"[系统] {sub} 成绩已存入")
                except ValueError:
                    print("[提示] 请输入数字")
            
        student_list.append(one_stu)
        print(f"[系统] {name} 数据录入完成！")
    return student_list

def show_all_students(student_list):
    '''
    用于实现数据统计与展示
    '''
    if not student_list:
        print("\n[提示] 当前没有学生数据")
        return
    
    print(f"\n======== 全班成绩单 ({len(student_list)}人) ========")

    for s in student_list:
        s.print_report()
        print("-" * 20)
    print("=" * 40)

def find_student(student_list):
    name = input("请输入要查找学生的姓名:").strip()
    for s in student_list:
        if s.name == name:
            return s
        
    print(f"[提示] 查无此人: {name}")
    return None

def delete_student(student_list):
    print("---- 删除模式 ----")
    target = find_student(student_list)

    if target:
        confirm = input(f"真的要删除{target.name}吗 (哭) (y/n):").lower()
        if confirm == 'y':
            student_list.remove(target)
            print(f"已成功删除 {target.name}")
        else:
            print("操作已取消")

def sort_student(student_list):
    '''
    将平均分按降序排序
    '''        
    if not student_list:
        print("无数据，无法排序")
        return 
    
    student_list.sort(key=lambda s: s.get_average(), reverse=True)

    print("[系统] 已按平均分从高到低排序！")

    show_all_students(student_list)
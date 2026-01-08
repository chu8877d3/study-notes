class Student:
    def __init__(self, name, sex, grades = None):
        self.name = name
        self.sex = sex
        #如果没传成绩，就创建一个空字典
        if grades is None:
            self.grades = {}
        else:
            self.grades = grades

    #只负责给分和科目，分数不合法就报错
    def add_score(self, subject, score):      
        if not (0 <= score <= 150):
            print(f"[错误]录入失败：{score}分超出范围(0-150)")
            return False
        
        self.grades[subject] = score

        return True
    
    def get_average(self):

        if len(self.grades) == 0:
            return 0
        return sum(self.grades.values()) /len(self.grades)
    
    def print_report(self):

        avg = self.get_average()

        print(f"--- {self.name} ({self.sex}) 的成绩单 ---")
        ##items()用于将字典中的每对键值组成一个元组，再将这些元组组成列表再返回
        for sub, sc in self.grades.items():
            print(f"{sub}:{sc}分")
        print("---------------------------")
        print(f"总平均分：{avg:.2f}")

    # 序列化，将对象变为字典，方便存入json
    def to_dict(self):
        return{
            "name":self.name,
            "sex":self.sex,
            "grades":self.grades
        }
    
    # 反序列化：把字典变回对象
    # @classmethod 意味着这个方法不需要实例就能调用，它属于“类”本身
    @classmethod
    def from_dict(cls, data):
        '''
        from_dict 的 Docstring
        
        :param cls: cls 代表“ Student ”这个类
        :param data: data 就是从 json 里读出来的字典
        '''
        return cls(data["name"],data["sex"],data["grades"])
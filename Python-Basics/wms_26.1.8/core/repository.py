from models.product import Product
class Repository:
    def __init__(self):
        self.products = {}
    
    # 进货
    def add_product(self, name, price, stock):
        #自动生成ID(max+1)
        if len(self.products) == 0:
            new_id = 1001
        else:
            all_ids = self.products.keys()
            new_id = max(all_ids) + 1

        new_p = Product(new_id, name, price, stock)
        self.products[new_id] = new_p
        print(f"[系统] 成功入库: {new_p.name} (ID: {new_id})")

    # 通过id进行查找
    def find_by_id(self,target_id):
        # 找到则返回id，没找到则默认返回None
        return self.products.get(target_id)
    # 列出所有
    def list_all(self, sort_by="id", reverse=False):
        print("\n--- 仓库清单 ---")
        if len(self.products) == 0:
            print(" 空空如也 ")
            return
        all_obj = self.products.values()
        sort_list = sorted(all_obj, key=lambda p:getattr(p, sort_by), reverse=reverse)
        for p in sort_list:
            print(p)
        print("----------------")
        
    # 通过修改库存
    def update(self, target_id, mode, new_stock):
        p = self.find_by_id(target_id)
        if p is not None:
            if mode == "set":
                p.stock = new_stock
                print(f"[系统] {p.name} 库存已修改为 {p.stock}")
            elif mode == "add":
                p.stock += new_stock
                print(f"[系统] {p.name} 库存已增加至 {p.stock}")
            else:
                p.stock -= new_stock
                if p.stock < 0:
                    p.stock = 0
                print(f"[系统] {p.name} 库存已减少至 {p.stock}")
        else:
            print(f"[错误] 找不到 ID: {target_id}")
    # 通过id删除产品
    def remove_product(self, target_id):
         
        p = self.find_by_id(target_id)
        if p is not None:
            self.products.pop(target_id)
            print(f"[系统] {p.name} 已从仓库中删除")
        else:
            print(f"[错误] 找不到 ID: {target_id}, 无法删除")
    # 将对象转为字典列表
    def to_data_list(self):
        return [product_obj.to_dict() for product_obj in self.products.values()]
    # 将字典列表转为UID和对象一一对应的字典
    def load(self, data):
        if not data:
            return
        self.products = {}
        self.products = {p["id"]:Product.from_dict(p) for p in data}

        print(f"[系统] 仓库数据装载完成, 共{len(self.products)}") 
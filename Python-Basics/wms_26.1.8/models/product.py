class Product:
    def __init__(self, p_id , name , price , stock):
        self.id = p_id
        self.name = name
        self.price = price
        self.stock = stock
    
    def __str__(self):
        # 格式化输出
        return f"[ID:{self.id}] {self.name} | 单价{self.price} | 库存: {self.stock}"
    

    # 序列化
    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }
    # 反序列化
    @classmethod
    def from_dict(cls, data):

        return cls(data["id"], data["name"], data["price"], data["stock"])
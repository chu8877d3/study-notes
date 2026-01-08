from models.product import Product
class ShoppingCart:
    def __init__(self):
        self.shoplist = []
    # 添加至清单
    def add_to_cart(self, product_obj, quantity):
        if product_obj.stock < quantity:
            print(f"[系统] 库存不足! {product_obj.name} 只有 {product_obj.stock}")
            return 
        
        for p in self.shoplist:
            if product_obj == p['product']:
                p['buy_qut'] +=  quantity
                print(f"[购物车] {product_obj.name} 数量增加至 {p['buy_qut']}")
                return
        self.shoplist.append({'product': product_obj, 'buy_qut': quantity})
        print(f"[购物车] 已成功添加 {product_obj.name} | {quantity}")    

    # 从清单中移除
    def remove_from_cart(self, product_obj):
        for p in self.shoplist:
            if  product_obj == p['product']:
                self.shoplist.remove(p)
                print(f"[购物车] 已移除 {product_obj.name}")
                return
        print(f"[购物车] 未找到 {product_obj.name}")   
        
    # 查看清单内容
    def get_cart_view(self):
        print("\n———————— 购物清单 ————————")
        if not self.shoplist:
            print("(空的)")
            return
        total_money = 0
        for s in self.shoplist:
            p = s['product']
            q = s['buy_qut']
            subtotal = p.price * q
            total_money += subtotal
            print(f"{p.name} | 数量: {q} | 单价: {p.price} | 小计: {subtotal}")
        print(f"总金额：{total_money}")
        print("\n——————————————————————————")
            
    #清空清单
    def clear_all(self):
        count = len(self.shoplist)
        self.shoplist.clear()
        print(f"[购物车] 已清空{count}条项目")
        
    # 结算并扣除库存
    def checkout(self):
        if not self.shoplist:
            print("[提示] 购物车是空的，无法结算")
            return
        
        for s in self.shoplist:
            p = s['product']
            q = s['buy_qut']
            
            if q <= p.stock:
                p.stock -= q
                print(f"√ 购买{p.name}成功，扣除库存{q}")
            else:
                print(f"× {p.name}库存不足, 购买失败")
        self.shoplist = []
        print("[系统] 交易成功!")
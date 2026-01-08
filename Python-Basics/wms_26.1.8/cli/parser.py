class CommandParser:
    def __init__(self, repo, cart, json):
        self.repo = repo
        self.cart = cart
        self.json = json
        self.command_map = {
            # --- 仓库管理 ---
            "list":   {"func": self._handle_list,   "usage": "list [-p/-i/-s/-n] [desc]",      "help": "查看仓库/排序"},
            "find":   {"func": self._handle_find,   "usage": "find <ID>",               "help": "查询单品"},
            "add":    {"func": self._handle_add,    "usage": "add <名> <价> <存>",      "help": "新品入库"},
            "update": {"func": self._handle_update, "usage": "update <ID> <模式> <数>", "help": "盘点/改库存"},
            "remove": {"func": self._handle_remove, "usage": "remove <ID>",             "help": "删除商品"},
            
            # --- 购物车 ---
            "buy":    {"func": self._handle_buy,    "usage": "buy <ID> <数>",           "help": "加入购物车"},
            "cart":   {"func": self._handle_cart,   "usage": "cart",                    "help": "查看购物车"},
            "pay":    {"func": self._handle_pay,    "usage": "pay",                     "help": "结账买单"},
            "clear":  {"func": self._handle_clear,  "usage": "clear",                   "help": "清空购物车"},
            
            # --- 系统 ---
            "help":   {"func": self._handle_help,   "usage": "help",                    "help": "显示此页"},
            "exit":   {"func": self._handle_exit,   "usage": "exit",                    "help": "退出"}
        }

    def execute(self, raw_input):
        parts = raw_input.strip().split()
        if not parts:
            return True
        
        action = parts[0].lower()
        args = parts[1:]
        #取出整个档案
        command_info = self.command_map.get(action)

        if command_info:
            handler_func = command_info['func']
            return handler_func(args)
        else:
            print(f"[错误] 未知指令: {action} (输入 help 查看列表)")
            return True

    def _handle_add(self,args):
        if len(args) < 3:
            print("[提示] 用法: add <名称> <价格> <数量>")
            return True
        try:
            name = args[0]
            price = float(args[1])
            stock = int(args[2])

            if price < 0 or stock < 0:
                print("[错误] 价格和库存不能是负数!")
                return True
            
            self.repo.add_product(name, price, stock)
        except ValueError:
            print("[错误] 价格和库存必须是数字!")
        return True

    def _handle_list(self, args):
        valid_sort_fields = {"id", "name", "price", "stock"}

        key_sort = "id"
        is_descending = False

        if len(args)>= 1:
            input_fields =args[0].lower()
            alias_sort_map = {"-i":"id", "-n":"name", "-p":"price", "-s":"stock"}
            key_sort = alias_sort_map.get(input_fields, input_fields)
            
            if key_sort not in valid_sort_fields:
                print(f"[错误] 不存在 {input_fields} 排序方法, 已启用默认ID排序")
                key_sort = "id"
            
        if len(args)>= 2:
            input_order = args[1].lower()
            if input_order in {"desc","down","降序"}:
                is_descending = True

        self.repo.list_all(key_sort, is_descending)
        return True

    def _handle_update(self,args):


        if len(args) < 3 or args[1] not in ["set", "add", "remove"]:
            print("[提示] 用法: update <ID> <set/add/remove> <数量>")
            return True
        try:
            target_id = int(args[0])
            mode = args[1]
            stock = int(args[2])
            if stock < 0:
                print("[错误] 库存不能为负数!")
                return True
            self.repo.update(target_id, mode, stock)
        except ValueError:
            print("[错误] ID和库存必须为整数!")
        return True

    def _handle_remove(self,args):
        if len(args) < 1:
            print("[提示] 用法: remove <ID>")
            return True
        try:
            target_id = int(args[0])
            self.repo.remove_product(target_id)
        except ValueError:
            print("[错误] ID必须为整数!")
        return True
    
    def _handle_find(self,args):
        if len(args) < 1:
            print("[提示] 用法: find <ID>")
            return True
        try:
            target_id = int(args[0])
            product_obj = self.repo.find_by_id(target_id)
            print(product_obj)
        except ValueError:
            print("[错误] ID必须为整数!")
        return True
    
    def _handle_buy(self,args):
        if len(args) < 2:
            print("[提示] 用法: buy <ID> <数量>")
            return True
        try:
            target_id = int(args[0])
            qut = int(args[1])
            product_obj = self.repo.find_by_id(target_id)

            if qut < 0:
                print("[错误] 数量不能为负数!")
                return True

            self.cart.add_to_cart(product_obj, qut)
        except ValueError:
            print("[错误] ID和数量必须为整数!")
        return True
    
    def _handle_cart(self,args):
        self.cart.get_cart_view()
        return True
    
    def _handle_clear(self,args):
        self.cart.clear_all()
        return True
    
    def _handle_pay(self,args):
        self.cart.checkout()
        return True
    
    def handle_save(self):
        data_list = self.repo.to_data_list()
        self.json.save(data_list)
        return True
        
    def _handle_help(self, args):
        print("\n" + " WMS 指令手册 ".center(50, "="))
        
        for cmd, info in self.command_map.items():
            print(f" {cmd:<8} {info['usage']:<28} -> {info['help']}")
            
        print("=" * 50)
        print(" * 模式提示: set(设置), add(增加), remove(减少)")
        print(" * 排序提示: list price desc (按价格降序)")
        return True
    
    def _handle_exit(self,args):
        self.handle_save()
        print("已退出WMS系统")
        return False
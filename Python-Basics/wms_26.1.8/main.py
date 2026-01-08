from cli.parser import CommandParser
from core.cart import ShoppingCart
from core.repository import Repository
from utils.json_handler import Jsonhandler

if __name__ == "__main__":
    
    json = Jsonhandler()
    repo = Repository()
    cart = ShoppingCart()

    data_list = json.load()
    repo.load(data_list)

    parser = CommandParser(repo, cart, json)

    print("[系统] WMS 仓库管理系统启动")
    print("[系统] 输入 help 以查看指令列表")

    is_running = True

    while is_running:
        try:
            cmd = input("\nWMS>")
            is_running = parser.execute(cmd)
        except KeyboardInterrupt:    
            parser.handle_save()
            print("\n强制退出, 已自动保存")
            break

    

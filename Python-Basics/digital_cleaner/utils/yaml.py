import os

import yaml
from loguru import logger

current_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_path)
filename = "config.yaml"
file_path = os.path.join(project_root, filename)


class YamlParser:
    def __init__(self):
        self.config = {}
        self.load_yaml()
        self.setting = self.config.get("setting", {})
        self.blacklist = self.config.get("blacklist", {})

    @property
    def extension_map(self):
        map = self.config.get("extension_map", {})
        return {ext: category for category, ext_list in map.items() for ext in ext_list}

    @property
    def mode(self):
        return self.setting.get("whitelist_mode", False)

    @property
    def black_extensions(self):
        return self.blacklist.get("extensions", [])

    @property
    def black_filenames(self):
        return self.blacklist.get("filenames", [])

    def load_yaml(self):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.config = yaml.safe_load(f)
            return True
        except yaml.YAMLError as exc:
            return False, logger.error(f"YAML 格式错误: {exc}")
        except FileNotFoundError:
            return False, logger.error("YAML 文件不存在")

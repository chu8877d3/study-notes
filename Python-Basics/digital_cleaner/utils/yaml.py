import yaml


filename = "config.yaml"
class YamlParser:
    def __init__(self):
        with open(filename, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

    @property
    def extension_map(self):
        map = self.config["extension_map"]
        return {ext: category for category, ext_list in map.items() for ext in ext_list}

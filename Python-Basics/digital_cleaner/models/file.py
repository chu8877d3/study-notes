import os


class FileItem:
    def __init__(self, parent, basename, ext, target_folder):
        self.parent = parent
        self.basename = basename
        self.ext = ext
        self.target_folder = target_folder

    @property
    def full_name(self):
        return self.basename + self.ext

    @property
    def full_path(self):
        return os.path.join(self.parent, self.full_name)

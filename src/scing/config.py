import os
from pathlib import Path


class Config:

    _10x_eula_cookie_key = "sw-eula-full"

    @property
    def ten_x_eula_cookie_key(self) -> str:
        return type(self)._10x_eula_cookie_key

    def __init__(self):
        self.path_home = os.path.join(Path.home(), ".scing")
        self.path_10x_eula_cfg = os.path.join(self.path_home, "10x-eula.cfg")
        os.makedirs(self.path_home, exist_ok=True)

    def write_10x_eula_cookie(self, value: str):
        with open(self.path_10x_eula_cfg, "wt") as fout:
            print(value, file=fout)

    def read_10x_eula_cookie(self) -> str:
        with open(self.path_10x_eula_cfg, "rt") as fout:
            value = fout.read().strip()
            cookies = dict()
            cookies[self._10x_eula_cookie_key] = value
            return cookies

    def has_10x_eula_cookie(self) -> bool:
        return os.path.exists(self.path_10x_eula_cfg)

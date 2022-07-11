import json
import os

class DB_json:

    def __init__(self, path):
        self.path = path

    def __setitem__(self, key, item):
        try:
            with open(self.path, "w") as f:
                load = json.load(f)
                load[key] = item
                json.dump(
                    load,
                    f,
                    indent=4
                )
        except OSError:
            raise KeyError(f"Path {self.path} not found")

    def __getitem__(self, key):
        try:
            with open(self.path, "r") as f:
                return json.load(f)[item]
        except KeyError:
            raise KeyError(f"Key in path {self.path} not found")
        except OSError:
            raise KeyError(f"Path {self.path} not found")
        
    def __delitem__(self, key):
        try:
            with open(self.path, "w") as f:
                load = json.load(f)
                del load[key]
                json.dump(
                    load,
                    f,
                    indent=4
                )
        except OSError:
            raise KeyError(f"Path {self.path} not found")
import os
import json

class DB_json:

    def __init__(self, path, cached=False):
        if cached:
            try:
                with open(path, "r") as f:
                    self.data: dict = json.load(f)
            except OSError:
                self.data = {}
        self.cached = cached
        self.path = path

    def __getitem__(self, key):
        if self.cached:
            return self.data.__getitem__(key)
        else:
            try:
                with open(self.path, "r") as f:
                    return json.load(f).__getitem__(key)
            except OSError:
                raise KeyError(f"Path {self.path} not found")

    def __setitem__(self, key, value):
        if self.cached:
            self.data.__setitem__(key, value)
        try:
            with open(self.path, "w") as f:
                json.dump(
                    json.load(f).__setitem__(key, value), 
                    f, 
                   indent=4
                )
        except OSError:
            os.makedirs(os.path.dirname(self.key))
            with open(self.path, "w") as f:
                json.dump(
                    json.load(f).__setitem__(key, value), 
                    f, 
                    indent=4
                )

    def __delitem__(self, key):
        if self.cached:
            self.data.__delitem__(key)
        try:
            with open(self.path, "w") as f:
                json.dump(
                    json.load(f).__delitem__(key),
                    f,
                    indent=4
                )
        except OSError:
            raise KeyError(f"Path {self.path} not found")

    def __contains__(self, key):
        if self.cached:
            return self.data.__contains__(key)
        with open(self.path, "w") as f:
            return json.load(f).__contains__(key)

    def dump(self, load):
        try:
            with open(self.path, "w") as f:
                json.dump(
                    load,
                    f,
                    indent=4
                )
        except OSError:
            os.makedirs(os.path.dirname(self.key))
            with open(self.path, "w") as f:
                json.dump(
                    load, 
                    f, 
                    indent=4
                )
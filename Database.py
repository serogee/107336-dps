import os
import json
from collections import MutableMapping

class DB_dict(object):

    _control = dict()

    def __new__(cls, parent, key, value, autoupdate=True):
        ppath = parent.path
        if ppath.endswith(".json"):
            try:
                if key in cls._control[ppath]:
                    return cls._control[ppath][key]
            except KeyError:
                pass
        return super(DB_dict, cls).__new__(cls, parent, key, value, autoupdate)

    def __init__(self, parent, key, value, autoupdate=True):
        ppath = parent.path
        if ppath.endswith(".json"):
            try:
                self._control[ppath][key] = self
            except KeyError:
                self._control[ppath] = {key: self}
        self.parent = parent
        self.autoupdate = autoupdate
        self.key = key
        self.value = value

    def __getitem__(self, key):
        return self.value[key]

    def __setitem__(self, key, value):
        self.value.__setitem__()
        if self.autoupdate:
            self._update()

    def __delitem__(self, key):
        del self.value[key]
        if self.autoupdate:
            self.update()

    def __len__(self):
        return self.value.__len__()

    def __iter__(self):
        return self.value__iter__()
    
    def __contains__(self, key):
        return self.value.contains(key)

    def __str__(self):
        return self.key

    def __repr__(self):
        return f""

    def pop(self, key):
        value = self.value.pop(key)
        if self.autoupdate:
            self._update()
        return value

    def pop_items(self, keys):
        for key in keys:
            try:
                yield self.value.pop(key)
            except KeyError:
                yield None
        if self.autoupdate:
            self._update()

    def update(self, update):
        self.value.__update__(update)
        if self.autoupdate:
            self._update()

    def copy(self):
        return self.value

    def items(self):
        return self.value.items()

    def dump(self, value):
        self.parent.__setitem__(self.key, value)
        self.value = value

    def _update(self):
        self.parent.__setitem__(self.key, self.value)

class DB_json(object):

    _control = dict()

    def __new__(cls, path, cached=False):
        if path in cls._control:
            return cls._control[path]
        else:
            return super(DB_json, cls).__new__(cls, path, cached)

    def __init__(self, path, cached=False):
        self.control[path] = self
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
                    value = json.load(f).__getitem__(key)
                    if type(value) is dict:
                        return DB_dict(self, key, value)
                    return value
            except OSError:
                raise KeyError(f"Path {self.path} not found")

    def __setitem__(self, key, value):
        if self.cached:
            self.data.__setitem__(key, value)
        while True:
            try:
                with open(self.path, "w") as f:
                    load = json.load(f)
                    load.__setitem__(key, value)
                    json.dump(
                        load, 
                        f, 
                        indent=4
                    )
                break
            except OSError:
                os.makedirs(os.path.dirname(self.key))

    def __delitem__(self, key):
        if self.cached:
            self.data.__delitem__(key)
        try:
            with open(self.path, "w") as f:
                load = json.load(f)
                load.__delitem__(key)
                json.dump(
                    load,
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

    def __iter__(self):
        if self.cached:
            return self.data.__iter__()
        with open(self.path, "r") as f:
            return json.load(f).__iter__()

    def __len__(self):
        if self.cached:
            return self.cached.__len__()
        with open(self.path, "r") as f:
            return json.load(f).__len__()

    def __str__(self):
        return self.path

    def pop(self, key):
        with open(self.path, "w") as f:
            if self.cached:
                load = self.data
                value = self.data.pop(key)
            else:
                load = json.load(f)
                value = load.pop(key)
            json.dump(
                load,
                f,
                indent=4
            )
            if type(value) is dict:
                return DB_dict(self, key, value)
            return value
                
    def pop_items(self, keys):
        """Deletes keys from an iterable and yields their values"""
        with open(self.path, "w") as f:
            if self.cached:
                load = self.data
            else:
                load = json.load(f)
            for key in keys:
                try:
                    value = load.pop(key)
                    if type(value) is dict:
                        yield DB_dict(self, key, value)
                    else:
                        yield value
                except KeyError:
                    yield None
            json.dump(
                load,
                f,
                indent=4
            )

    def get_items(self, keys):
        """Yields the values of keys in an iterable"""
        if self.cached:
            for key in keys:
                yield key, self.cached.__getitem__(key)
        else:
            with open(self.path, "r") as f:
                load: dict = json.load(f)
                for key in keys:
                    try:
                        value = load.__getitem__(key)
                        if type(value) is dict:
                            yield key, DB_dict(self, key, value)
                        else:
                            yield key, value
                    except KeyError:
                        yield key, None

    def update(self, items: dict):
        with open(self.path, "w") as f:
            load = json.load(f)
            load.update(items)
            json.dump(
                load,
                f,
                indent=4
            )
        if self.cached:
            self.data = load

    def items(self):
        if self.cached:
            return self.data.items()

    def copy(self):
        if self.cached:
            return self.data.copy()
        with open(self.path, "r"):
            return json.load(f)

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

class DB(object):

    def __init__(self, path, cached=False):
        self.path = path
        self.cached
    
    def __getitem__(self, key):
        return DB_json(self.path, self.cached)

    def __setitem__(self, key, value):
        while True:
            try:
                with open(f"{self.path}/{key}") as f:
                    json.dump(
                        value,
                        f,
                        indent=4
                    )
                break
            except OSError:
                os.makedirs(os.path.dirname(f"{self.path}/{key}"))

    def __delitem__(self, key):
        try:
            os.remove(f"{self.path}/{key}")
        except OSError:
            raise KeyError(f"File {key} not found")
    
    def __contains__(self, key):
        try:
            return key in os.listdir(self.path)
        except OSError:
            return False

    def __len__(self):
        try:
            return len(os.listdir(self.path))
        except OSError:
            return 0

    def __iter__(self):
        return iter(os.listdir(self.path))

    def keys(self):
        return os.listdir(self.path)

    def items(self):
        for key in os.listdir(self.path):
            with open(f"{self.path}/{key}", "w") as f:
                yield key, json.load(f)

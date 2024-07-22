from typing import Union, Tuple

Color = Union[Tuple[int, int, int], str]
Coordinate = Tuple[int, int]


class AttrDict(dict):
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value

import sys
import importlib
import importlib.abc

NUMBA_LOCATION = "/home/gmarkall/numbadev/numba"
NUMBA_CUDA_LOCATION = "/home/gmarkall/numbadev/numba_cuda/numba_cuda"


class TestFinder(importlib.abc.MetaPathFinder):
    def __init__(self, meta_path):
        self._meta_path = meta_path.copy()

    def find_spec(self, name, path, target):
        if "numba.cuda" in name:
            oot_path = [p.replace(NUMBA_LOCATION, NUMBA_CUDA_LOCATION)
                        for p in path]
            for finder in self._meta_path:
                spec = finder.find_spec(name, oot_path, target)
                if spec is not None:
                    return spec


def install():
    print("Installing")
    sys.meta_path.insert(0, TestFinder(sys.meta_path))

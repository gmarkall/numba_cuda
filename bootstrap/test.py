import sys

NUMBA_LOCATION = "/home/gmarkall/numbadev/numba"
NUMBA_CUDA_LOCATION = "/home/gmarkall/numbadev/numba_cuda"


class TestFinder:
    def __init__(self, meta_path):
        self._meta_path = meta_path.copy()

    def find_spec(self, name, path, target):
        if "numba.cuda" in name:
            print(f"{name} :: {path} :: {target}")
            oot_path = [p.replace(NUMBA_LOCATION, NUMBA_CUDA_LOCATION)
                        for p in path]
            for finder in self._meta_path:
                spec = finder.find_spec(name, oot_path, target)
                if spec is not None:
                    breakpoint()
                    return spec


sys.meta_path.insert(0, TestFinder(sys.meta_path))

from numba import cuda  # noqa: E402, F401

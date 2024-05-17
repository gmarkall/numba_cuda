import os
import sys

from numba import cuda
import numba_cuda

# Run the test suite

if __name__ == '__main__':
    cuda.test()

    # Ensure we haven't imported anything from the Numba package location by
    # checking that all numba.cuda imports came from the numba_cuda package's
    # directory tree

    numba_cuda_path = os.path.dirname(numba_cuda.__file__)

    unexpected_path = False
    for name, module in sys.modules.items():
        if "numba.cuda" in name:
            if numba_cuda_path not in module.__file__:
                print("Warning - unexpected path for "
                      f"{name}: {module.__file__}")
                unexpected_path = True

    sys.exit(unexpected_path)

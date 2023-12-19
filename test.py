import numba_cuda

numba_cuda.install()

from numba import cuda  # noqa: E402

if __name__ == '__main__':
    cuda.test()


# Need to ensure that all CUDA modules are imported from this package at this
# point.

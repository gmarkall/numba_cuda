import numba_cuda as cuda


@cuda.jit(device=True)
def cuda_module_in_device_function():
    return cuda.threadIdx.x

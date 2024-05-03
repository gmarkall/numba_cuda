def initialize_all():
    # Import models to register them with the data model manager
    import numba_cuda.models  # noqa: F401

    from numba_cuda.decorators import jit
    from numba_cuda.dispatcher import CUDADispatcher
    from numba.core.target_extension import (target_registry,
                                             dispatcher_registry,
                                             jit_registry)

    cuda_target = target_registry["cuda"]
    jit_registry[cuda_target] = jit
    dispatcher_registry[cuda_target] = CUDADispatcher

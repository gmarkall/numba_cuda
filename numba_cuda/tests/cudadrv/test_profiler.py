import unittest
from numba_cuda.testing import ContextResettingTestCase
import numba_cuda as cuda
from numba_cuda.testing import skip_on_cudasim


@skip_on_cudasim('CUDA Profiler unsupported in the simulator')
class TestProfiler(ContextResettingTestCase):
    def test_profiling(self):
        with cuda.profiling():
            a = cuda.device_array(10)
            del a

        with cuda.profiling():
            a = cuda.device_array(100)
            del a


if __name__ == '__main__':
    unittest.main()

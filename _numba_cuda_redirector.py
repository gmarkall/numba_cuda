import importlib
import sys
import warnings

multiple_locations_msg = ("Multiple submodule search locations for {}. "
                          "Cannot redirect numba.cuda to numba_cuda")

no_spec_msg = ("Couldn't get spec for {}. "
               "Cannot redirect numba.cuda to numba_cuda")


class NumbaCudaFinder(importlib.abc.MetaPathFinder):
    def __init__(self):
        #self._meta_path = meta_path.copy()
        self.initialized = None

    def ensure_initialized(self):
        if self.initialized is not None:
            return self.initialized

        numba_spec = importlib.util.find_spec('numba')

        if numba_spec is None:
            warnings.warn(no_spec_msg.format('numba'))
            self.initialized = False
            return False

        numba_cuda_spec = importlib.util.find_spec('numba_cuda')

        if numba_spec is None:
            warnings.warn(no_spec_msg.format('numba_cuda'))
            self.initialized = False
            return False

        numba_search_locations = numba_spec.submodule_search_locations
        numba_cuda_search_locations = numba_cuda_spec.submodule_search_locations

        if len(numba_search_locations) != 1:
            warnings.warn(multiple_locations_msg.format('numba'))
            self.initialized = False
            return False

        if len(numba_cuda_search_locations) != 1:
            warnings.warn(multiple_locations_msg.format('numba_cuda'))
            self.initialized = False
            return False

        self.numba_path = numba_search_locations[0]
        self.numba_cuda_path = numba_cuda_search_locations[0]
        self.initialized = True
        return True

    def find_spec(self, name, path, target):
        if "numba.cuda" in name and "numba.cuda.tests" not in name:
            initialized = self.ensure_initialized()
            if not initialized:
                return None

            if any(self.numba_cuda_path in p for p in path):
                # Re-entrancy - return and carry on
                return None

            oot_path = [p.replace(self.numba_path, self.numba_cuda_path)
                        for p in path]
            oot_name = f"numba_cuda.{name}"
            #print(name, path, oot_path)
            for finder in sys.meta_path:
                spec = finder.find_spec(oot_name, oot_path, target)
                if spec is not None:
                    new_spec = importlib.util.spec_from_file_location(name,
                                                                      spec.origin)
                    #print("---", new_spec)
                    return new_spec


finder = NumbaCudaFinder()
sys.meta_path.insert(0, finder)

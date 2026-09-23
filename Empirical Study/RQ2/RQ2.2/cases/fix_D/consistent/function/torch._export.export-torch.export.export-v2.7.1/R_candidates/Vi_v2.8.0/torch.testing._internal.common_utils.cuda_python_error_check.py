    def cuda_python_error_check(function_call_output):
        """Makes calls to cuda-python's cuda runtime functions more
        pythonic by throwing an exception if they return a status
        which is not cudaSuccess
        """
        import cuda.bindings  # type: ignore[import]

        error, *others = function_call_output
        if error != cuda.bindings.runtime.cudaError_t.cudaSuccess:
            raise ValueError(f"CUDA failure! {error}")
        else:
            return tuple(others)

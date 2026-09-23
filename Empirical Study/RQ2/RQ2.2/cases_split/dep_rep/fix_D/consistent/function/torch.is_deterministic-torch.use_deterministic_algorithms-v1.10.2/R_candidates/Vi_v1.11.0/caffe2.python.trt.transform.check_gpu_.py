def check_gpu_():
    try:
        C.get_cuda_version()
    except Exception as _:
       raise Exception("TensorRT related functions require CUDA support")

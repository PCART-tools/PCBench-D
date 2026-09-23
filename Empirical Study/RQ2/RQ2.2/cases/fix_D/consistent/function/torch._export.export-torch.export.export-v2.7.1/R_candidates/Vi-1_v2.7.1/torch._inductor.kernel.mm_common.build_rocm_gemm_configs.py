def build_rocm_gemm_configs(configs):
    rocm_num_stages = get_backend_num_stages()
    return tuple((c[0], c[1], c[2], rocm_num_stages, c[4]) for c in configs)

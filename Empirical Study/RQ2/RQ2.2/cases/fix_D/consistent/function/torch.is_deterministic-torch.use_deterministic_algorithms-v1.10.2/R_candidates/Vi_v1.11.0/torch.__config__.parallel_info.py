def parallel_info():
    r"""Returns detailed string with parallelization settings"""
    return torch._C._parallel_info()

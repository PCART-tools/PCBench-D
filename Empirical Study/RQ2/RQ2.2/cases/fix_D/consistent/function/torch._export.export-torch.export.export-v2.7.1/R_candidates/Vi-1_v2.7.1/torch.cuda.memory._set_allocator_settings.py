def _set_allocator_settings(env: str):
    return torch._C._cuda_cudaCachingAllocator_set_allocator_settings(env)

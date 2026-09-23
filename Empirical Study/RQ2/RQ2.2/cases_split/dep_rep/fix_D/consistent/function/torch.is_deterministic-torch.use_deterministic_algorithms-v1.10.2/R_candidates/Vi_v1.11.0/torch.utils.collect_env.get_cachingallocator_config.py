def get_cachingallocator_config():
    ca_config = os.environ.get('PYTORCH_CUDA_ALLOC_CONF', '')
    return ca_config

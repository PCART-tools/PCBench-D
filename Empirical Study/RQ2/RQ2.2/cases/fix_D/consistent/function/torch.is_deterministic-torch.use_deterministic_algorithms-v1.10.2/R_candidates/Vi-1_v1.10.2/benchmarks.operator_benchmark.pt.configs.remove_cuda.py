def remove_cuda(config_list):
    cuda_config = {'device': 'cuda'}
    return [config for config in config_list if cuda_config not in config]

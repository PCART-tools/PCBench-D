def _construct_format_dict():
    dct = {
        'ModuleList': 'torch.nn.modules.container.ModuleList',
        'AdaptiveAvgPool2d': 'torch.nn.modules.pooling.AdaptiveAvgPool2d',
        'AdaptiveMaxPool2d': 'torch.nn.modules.pooling.AdaptiveMaxPool2d',
        'Tensor': 'torch._tensor.Tensor',
        'Adagrad': 'torch.optim.adagrad.Adagrad',
        'Adam': 'torch.optim.adam.Adam',
    }
    return dct

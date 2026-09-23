def _dtype_default_type_hack(name: str) -> str:
    if name.startswith('randperm') or name == 'tril_indices' or name == 'triu_indices':
        return 'torch.int64'
    else:
        return 'None'

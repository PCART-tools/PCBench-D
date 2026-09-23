def is_bf16_supported():
    r"""Returns a bool indicating if the current CUDA device supports dtype bfloat16"""
    cu_vers = torch.version.cuda
    if cu_vers is not None:
        cuda_maj_decide = int(cu_vers.split('.')[0]) >= 11

    else:
        cuda_maj_decide = False
    return torch.cuda.get_device_properties(torch.cuda.current_device()).major >= 8 and cuda_maj_decide

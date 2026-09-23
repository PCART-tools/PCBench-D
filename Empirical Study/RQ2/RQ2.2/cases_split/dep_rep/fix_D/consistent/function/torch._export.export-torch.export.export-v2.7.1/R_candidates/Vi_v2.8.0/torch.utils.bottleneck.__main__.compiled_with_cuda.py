def compiled_with_cuda(sysinfo):
    if sysinfo.cuda_compiled_version:
        return f'compiled w/ CUDA {sysinfo.cuda_compiled_version}'
    return 'not compiled w/ CUDA'

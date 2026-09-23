def compiled_with_cuda(sysinfo):
    if sysinfo.cuda_compiled_version:
        return 'compiled w/ CUDA {}'.format(sysinfo.cuda_compiled_version)
    return 'not compiled w/ CUDA'

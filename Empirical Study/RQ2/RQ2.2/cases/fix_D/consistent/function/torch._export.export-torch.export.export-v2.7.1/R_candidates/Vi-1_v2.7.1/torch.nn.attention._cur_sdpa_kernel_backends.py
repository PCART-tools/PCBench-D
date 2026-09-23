def _cur_sdpa_kernel_backends():
    backends: list[SDPBackend] = []
    for name, val in _backend_names.items():
        if getattr(torch.backends.cuda, f"{name}_sdp_enabled")():
            backends.append(getattr(SDPBackend, val))
    return backends

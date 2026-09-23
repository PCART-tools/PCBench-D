def _sdpa_kernel(backends: Iterable[SDPBackend]):
    for name, val in _backend_names.items():
        enabled = getattr(SDPBackend, val) in backends
        getattr(torch.backends.cuda, f"enable_{name}_sdp")(enabled)

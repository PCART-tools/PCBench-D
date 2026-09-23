def _get_rocm_config(query, mode: Mode) -> tuple[int, int, int, int]:
    dtype = query.get_dtype()
    head_dim = V.graph.sizevars.evaluate_static_shape(query.get_size()[-1])
    fwd_config = None

    if mode == Mode.fwd:
        if head_dim <= 256:
            if dtype == torch.float32:
                fwd_config = (64, 64, 4, 1)
            else:
                fwd_config = (128, 64, 8, 1)
            fwd_config = _rocm_default_config.get((dtype, head_dim), fwd_config)
        else:  # modest hardware or extremely large head_dim
            if dtype == torch.float32:
                fwd_config = (32, 16, 4, 1)
            else:
                fwd_config = (64, 32, 4, 1)
        return fwd_config
    else:  # bwd
        assert mode == Mode.bwd
        if dtype == torch.float32:
            return (16, 16, 4, 1)
        elif head_dim <= 256:
            if head_dim == 64:
                return (64, 64, 4, 1)
            elif head_dim == 128:
                return (64, 128, 8, 1)
            else:
                return (64, 64, 4, 1)
        else:  # modest hardware or extremely large head_dim
            return (16, 16, 4, 1)

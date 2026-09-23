def _get_nv_config(query, mode: Mode) -> tuple[int, int, int, int]:
    dtype = query.get_dtype()
    head_dim = V.graph.sizevars.evaluate_static_shape(query.get_size()[-1])
    fwd_config = None
    bwd_config = None
    capability = torch.cuda.get_device_capability()

    if mode == Mode.fwd:
        if head_dim <= 256:
            if dtype == torch.float32:
                fwd_config = (64, 64, 4, 3)
            else:
                fwd_config = (128, 64, 4, 3)
            if capability >= (9, 0):
                fwd_config = _h100_default_config.get((dtype, head_dim), fwd_config)
            elif capability >= (8, 0):
                fwd_config = _a100_default_config.get((dtype, head_dim), fwd_config)
        else:  # modest hardware or extremely large head_dim
            if dtype == torch.float32:
                fwd_config = (32, 16, 4, 3)
            else:
                fwd_config = (64, 32, 4, 3)
        return fwd_config

    else:  # bwd
        assert mode == Mode.bwd
        if dtype == torch.float32:
            bwd_config = (16, 16, 4, 1)
        elif head_dim <= 256 and capability >= (9, 0):  # H100
            if head_dim == 64:
                bwd_config = (64, 64, 4, 3)
            elif head_dim == 128:
                bwd_config = (64, 128, 8, 3)
            else:
                bwd_config = (64, 64, 4, 2)
        elif capability >= (8, 0):
            if head_dim >= 64:
                bwd_config = (32, 128, 4, 3)
            elif head_dim == 128:
                # SM86/89 have smaller shared memory sizes
                num_stages = 3 if capability[-1] == 0 else 2
                bwd_config = (64, 64, 4, num_stages)
            else:
                bwd_config = (64, 64, 4, 2)
        else:  # modest hardware or extremely large head_dim
            bwd_config = (16, 16, 4, 1)
        return bwd_config

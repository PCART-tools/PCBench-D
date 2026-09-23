def _allow_in_graph_einops():
    import einops

    try:
        # requires einops > 0.6.1, torch >= 2.0
        from einops._torch_specific import (  # type: ignore[attr-defined]  # noqa: F401
            _ops_were_registered_in_torchdynamo,
        )

        # einops > 0.6.1 will call the op registration logic as it is imported.
    except ImportError:
        # einops <= 0.6.1
        allow_in_graph(einops.rearrange)
        allow_in_graph(einops.reduce)
        if hasattr(einops, "repeat"):
            allow_in_graph(einops.repeat)  # available since einops 0.2.0
        if hasattr(einops, "einsum"):
            allow_in_graph(einops.einsum)  # available since einops 0.5.0
        if hasattr(einops, "pack"):
            allow_in_graph(einops.pack)  # available since einops 0.6.0
        if hasattr(einops, "unpack"):
            allow_in_graph(einops.unpack)  # available since einops 0.6.0

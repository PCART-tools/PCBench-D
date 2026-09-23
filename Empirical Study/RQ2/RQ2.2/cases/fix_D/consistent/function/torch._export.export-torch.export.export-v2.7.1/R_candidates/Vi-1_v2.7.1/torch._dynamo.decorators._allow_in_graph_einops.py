def _allow_in_graph_einops():
    mod = sys.modules.get("einops")
    if mod is None:
        return
    else:
        # version > 0.8.1 does allow_in_graph out of tree
        # for BC we need to keep this in fbcode
        # internal xref https://fb.workplace.com/groups/1026248852325474/permalink/1107135774236781/
        if Version(mod.__version__) <= Version("0.8.1") or is_fbcode():
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

def dump_file(filename: str) -> None:
    if "eval_with_key" not in filename:
        return
    if filename in DUMPED_FILES:
        return
    DUMPED_FILES.add(filename)
    from torch.fx.graph_module import _loader

    torch._logging._internal.trace_structured(
        "dump_file",
        metadata_fn=lambda: {
            "name": filename,
        },
        payload_fn=lambda: _loader.get_source(filename),
    )

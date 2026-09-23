def propagate_metadata(orig_gm, split_gm) -> None:
    for name, module in split_gm.named_modules():
        if "." not in name and len(name):
            # TODO: add split id to CompileId: https://github.com/pytorch/tlparse/pull/83/files#r1880649384
            module.meta = orig_gm.meta
            module._param_name_to_source = orig_gm._param_name_to_source

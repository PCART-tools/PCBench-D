def fuse_fx(gm: torch.fx.GraphModule, example_inputs) -> torch.fx.GraphModule:
    is_cpu = is_cpu_device(example_inputs)
    # pyre-fixme[16]: Module `torch._dynamo.utils` has no attribute `detect_fake_mode`
    fake_mode = detect_fake_mode(example_inputs)

    gm = sink_cat_after_pointwise(gm)
    if config.permute_fusion and not is_cpu:
        # For linear permute fusion, we need to check input info to identify
        # and perform proper permutation/transpose
        ShapeProp(gm, fake_mode=fake_mode).propagate(*example_inputs)
        with GraphTransformObserver(gm, "linear_permute_fusion"):
            gm = linear_permute_fusion(gm)
        with GraphTransformObserver(gm, "permute_linear_fusion"):
            gm = permute_linear_fusion(gm)
        with GraphTransformObserver(gm, "permute_matmul_fusion"):
            gm = permute_matmul_fusion(gm)

    # make sure the autograd is disabled.
    if torch.is_grad_enabled() or not is_cpu:
        return gm
    if config.freezing:
        with GraphTransformObserver(gm, "remove_identity"):
            gm = remove_identity(gm)
        with GraphTransformObserver(gm, "fuse_conv_bn"):
            gm = fuse_conv_bn(gm)
    return gm

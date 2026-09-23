def run_frozen_optimizations(mod, optimize_numerics: bool = True):
    r"""
    Runs a series of optimizations looking for patterns that occur in frozen graphs.
    The current set of optimizations is:
        - Dropout Removal
        - Conv -> Batchnorm folding
        - Conv -> Add/Sub folding
        - Conv -> Mul/Div folding

    Args:
        mod (:class:`ScriptModule`): a frozen module to be optimized

        optimize_numerics (bool): If ``True``, a set of optimization passes will be run that does not strictly
        preserve numerics. These optimizations preserve default rtol and atol of `torch.testing.assert_allclose`
        when applied on a single transformation, however in a module where many transformations are applied
        the rtol or atol may no longer fall within the default `assert_allclose` tolerance. Conv -> Batchnorm folding,
        Conv-Add/Sub, and Conv -> Mul/Div folding all may alter numerics.

    Returns:
        None

    Note:
        In rare occassions, this can result in slower execution.

    Example (Freezing a module with Conv->Batchnorm)
    .. code-block:: python
        import torch
        in_channels, out_channels = 3, 32
        conv = torch.nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=2, bias=True)
        bn = torch.nn.BatchNorm2d(out_channels, eps=.001)
        mod = torch.nn.Sequential(conv, bn)
        # set optimize to False here, by default freezing runs run_frozen_optimizations
        frozen_mod = torch.jit.freeze(torch.jit.script(mod.eval()), optimize=False)
        # inspect frozen mod
        assert "batch_norm" in str(frozen_mod.graph)
        torch.jit.run_frozen_optimizations(frozen_mod)
        assert "batch_norm" not in str(frozen_mod.graph)

    """
    # xxx: keep in sync with frozen_graph_optimization.cpp
    # intentionally duplicated to make to make it easier to create custom optimization sequence
    torch._C._jit_pass_remove_dropout(mod._c)
    if optimize_numerics:
        # run a couple times to capture Conv -> Mul -> Add etc
        for _ in range(2):
            torch._C._jit_pass_fold_frozen_conv_bn(mod.graph)
            torch._C._jit_pass_fold_frozen_conv_add_or_sub(mod.graph)
            torch._C._jit_pass_fold_frozen_conv_mul_or_div(mod.graph)

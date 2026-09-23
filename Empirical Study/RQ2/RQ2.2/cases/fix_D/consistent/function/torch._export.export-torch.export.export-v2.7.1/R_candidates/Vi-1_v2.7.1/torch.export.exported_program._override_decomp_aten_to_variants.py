@contextmanager
def _override_decomp_aten_to_variants():
    # Preserve variants of aten::to understanding that they are mutating/aliasing
    # and their CompositeImplicitAutograd kernels will not become NotImplemented.
    # We will later replace them with aten._to_copy when functionalizing.
    with _override_composite_implicit_decomp(
        {
            torch.ops.aten.to.dtype_layout: _special_op_to_preserve_cia,
            torch.ops.aten.to.dtype: _special_op_to_preserve_cia,
        },
        safe=False,
    ):
        yield

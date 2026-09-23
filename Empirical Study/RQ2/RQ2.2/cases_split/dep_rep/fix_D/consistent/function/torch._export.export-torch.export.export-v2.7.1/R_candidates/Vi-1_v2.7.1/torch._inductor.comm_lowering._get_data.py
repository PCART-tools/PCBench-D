def _get_data(x: ir.TensorBox) -> ir.IRNode:
    if isinstance(x.data, ir.BaseView):
        # TensorBox -> *View -> StorageBox -> IRNode
        return x.data.unwrap_view().data
    elif isinstance(x.data, ir.StorageBox):
        # TensorBox -> StorageBox -> IRNode
        return cast(ir.Buffer, x.data.data)
    else:
        raise AssertionError(
            "Expect the data attr of a `TensorBox` to be either "
            f"an `ir.BaseView` or `ir.StorageBox` (got {x.data})."
        )

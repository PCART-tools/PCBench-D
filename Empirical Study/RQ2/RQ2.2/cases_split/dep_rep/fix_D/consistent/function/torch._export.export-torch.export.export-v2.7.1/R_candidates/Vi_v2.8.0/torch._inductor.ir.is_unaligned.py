def is_unaligned(node: IRNode) -> bool:
    if isinstance(node, (TensorBox, StorageBox)):
        return is_unaligned(node.data)

    if isinstance(node, ReinterpretView):
        layout = node.layout
        has_unaligned_layout = not statically_known_true(
            layout.offset * get_dtype_size(layout.dtype) % GPU_ALIGN_BYTES == 0
        )
        return is_unaligned(node.data) or has_unaligned_layout

    if isinstance(node, Buffer):
        return node.get_name() in V.graph.unaligned_buffers

    # assume to be aligned otherwise
    return False

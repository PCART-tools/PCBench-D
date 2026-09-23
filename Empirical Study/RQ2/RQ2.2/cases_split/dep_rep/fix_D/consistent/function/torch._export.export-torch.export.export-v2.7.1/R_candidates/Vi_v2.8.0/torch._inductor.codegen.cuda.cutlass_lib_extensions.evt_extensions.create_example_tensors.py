    def create_example_tensors(
        var_name_to_buffer_name: dict[str, str],
        name_to_buffer: dict[str, Buffer],
        size_hint_fn: Callable[[Union[Expr, int]], int],
    ) -> dict[str, CutlassTensor]:
        def cutlass_tensor_from_buffer(buffer: Buffer) -> CutlassTensor:
            shape = buffer.get_layout().size
            stride = buffer.get_layout().stride
            shape = tuple(size_hint_fn(x) for x in shape)
            stride = tuple(size_hint_fn(x) for x in stride)

            is_row_major = is_contiguous_strides_for_shape(stride, shape)
            is_column_major = is_contiguous_strides_for_shape(stride[::-1], shape[::-1])

            if not is_row_major and not is_column_major:
                raise RuntimeError(
                    f"Cannot create example tensor for {buffer.get_name()} with \
non-contiguous layout, received stride: {stride} and shape: {shape}"
                )

            return CutlassTensor(
                shape=shape,
                layout_tag=LayoutType.RowMajor
                if is_row_major
                else LayoutType.ColumnMajor,
                element=torch_dtype_to_cutlass_type(buffer.get_layout().dtype),
            )

        return {
            key: cutlass_tensor_from_buffer(name_to_buffer[name])
            for key, name in var_name_to_buffer_name.items()
        }

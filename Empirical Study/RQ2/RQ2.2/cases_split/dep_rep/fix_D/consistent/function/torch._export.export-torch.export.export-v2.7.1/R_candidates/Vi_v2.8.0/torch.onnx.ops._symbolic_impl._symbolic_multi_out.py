@torch.library.custom_op(
    "onnx_symbolic::_symbolic_multi_out",
    mutates_args=(),
    schema=(
        "(Tensor?[] inputs, str op_type, int[] onnx_dtypes, *,"
        " SymInt[][] shapes, str[] attr_keys, str[] attr_types, int[][] attr_pos,"
        " int[] attr_ints, float[] attr_floats, str[] attr_strs, str[] metadata_props_keys,"
        " str[] metadata_props_values, str domain='', int? version=None"
        ") -> Tensor[]"
    ),
)
def _symbolic_multi_out(
    inputs: Sequence[Optional[torch.Tensor]],
    op_type: str,
    onnx_dtypes: Sequence[int],
    *,
    shapes: Sequence[Sequence[Union[int, torch.SymInt]]],
    attr_keys: Sequence[str],
    attr_types: Sequence[str],
    attr_pos: Sequence[tuple[int, int]],
    attr_ints: Sequence[int],
    attr_floats: Sequence[float],
    attr_strs: Sequence[str],
    metadata_props_keys: Sequence[str] = (),
    metadata_props_values: Sequence[str] = (),
    domain: str = "",
    version: Optional[int] = None,
) -> list[torch.Tensor]:
    outputs = []
    torch._check(
        len(shapes) == len(onnx_dtypes),
        lambda: f"Number of shapes ({len(shapes)}) must match number of ONNX dtypes ({len(onnx_dtypes)})",
    )
    for shape, onnx_dtype in zip(shapes, onnx_dtypes):
        torch._check(
            onnx_dtype in _dtype_mappings.ONNX_DTYPE_TO_TORCH_DTYPE,
            lambda: f"{onnx_dtype} is invalid as an ONNX data type. Valid values are {list(_dtype_mappings.ONNX_DTYPE_TO_TORCH_DTYPE.keys())}",
        )
        outputs.append(
            torch.zeros(
                shape, dtype=_dtype_mappings.ONNX_DTYPE_TO_TORCH_DTYPE[onnx_dtype]
            )
        )
    return outputs

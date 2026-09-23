@impl(
    quantized_decomposed_lib,
    "convert_element_type.no_fuse",
    "CompositeExplicitAutograd",
)
def convert_element_type(input: torch.Tensor, dtype: torch.dtype) -> torch.Tensor:
    return torch.ops.prims.convert_element_type.default(input, dtype)

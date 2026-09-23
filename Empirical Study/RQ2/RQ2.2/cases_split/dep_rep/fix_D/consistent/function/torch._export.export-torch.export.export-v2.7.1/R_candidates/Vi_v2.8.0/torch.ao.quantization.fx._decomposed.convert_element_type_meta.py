@impl(quantized_decomposed_lib, "convert_element_type.no_fuse", "Meta")
def convert_element_type_meta(input: torch.Tensor, dtype: torch.dtype) -> torch.Tensor:
    return torch.empty_like(input, dtype=dtype)

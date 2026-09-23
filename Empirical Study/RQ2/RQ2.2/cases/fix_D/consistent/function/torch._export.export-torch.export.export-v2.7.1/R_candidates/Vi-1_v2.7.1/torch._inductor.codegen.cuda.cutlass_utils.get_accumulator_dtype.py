def get_accumulator_dtype(
    input_torch_dtypes: list[torch.dtype],
) -> Optional[torch.dtype]:
    """
    Given a pair of input torch dtypes, returns the inferred accumulator torch dtype.
    """

    if len(input_torch_dtypes) != 2:
        return None

    torch_dtype = None
    if input_torch_dtypes[0] == input_torch_dtypes[1]:
        torch_dtype = input_torch_dtypes[0]
    else:
        size0 = torch.tensor([], dtype=input_torch_dtypes[0]).element_size()
        size1 = torch.tensor([], dtype=input_torch_dtypes[1]).element_size()
        if size0 > size1:
            dtype0, dtype1 = input_torch_dtypes
        else:
            dtype1, dtype0 = input_torch_dtypes
        if dtype0 in [torch.half, torch.bfloat16] and dtype1 in [
            torch.int8,
            torch.uint8,
        ]:
            torch_dtype = dtype0

    if torch_dtype in (torch.float16, torch.bfloat16, torch.float):
        return torch.float
    if torch_dtype == torch.int8:
        return torch.int32
    raise NotImplementedError(f"Unsupported data types: {input_torch_dtypes=}")

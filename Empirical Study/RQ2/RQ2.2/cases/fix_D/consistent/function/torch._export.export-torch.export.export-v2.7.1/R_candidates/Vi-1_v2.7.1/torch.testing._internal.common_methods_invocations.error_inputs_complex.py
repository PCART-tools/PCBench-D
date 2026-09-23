def error_inputs_complex(op_info, device, is_ref=False, **kwargs):
    make_arg = partial(make_tensor, dtype=torch.float32, device=device)

    if is_ref:
        error_float = "Expected both inputs to be Half, Float or Double tensors but got torch.float32 and torch.int32"
        error_dtype = "Expected object of scalar type torch.float32 but got scalar type torch.float64 for second argument"
        error_out = "Expected out tensor to have dtype torch.complex128 but got torch.complex64 instead"
    else:
        error_float = "Expected both inputs to be Half, Float or Double tensors but got Float and Int"
        error_dtype = "Expected object of scalar type Float but got scalar type Double for second argument"
        error_out = "Expected object of scalar type ComplexDouble but got scalar type ComplexFloat for argument 'out'"

    yield ErrorInput(SampleInput(make_arg(M, S), make_arg(M, S, dtype=torch.int)),
                     error_type=RuntimeError, error_regex=error_float)

    yield ErrorInput(SampleInput(make_arg(M, S), make_arg(M, S, dtype=torch.float64)),
                     error_type=RuntimeError, error_regex=error_dtype)

    yield ErrorInput(SampleInput(make_arg(M, S, dtype=torch.float64), make_arg(M, S, dtype=torch.float64),
                                 out=make_arg(M, S, dtype=torch.complex64)),
                     error_type=RuntimeError, error_regex=error_out)

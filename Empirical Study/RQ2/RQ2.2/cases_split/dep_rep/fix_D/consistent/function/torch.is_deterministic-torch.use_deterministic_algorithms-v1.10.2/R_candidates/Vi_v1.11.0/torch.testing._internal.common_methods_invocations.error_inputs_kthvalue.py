def error_inputs_kthvalue(op_info, device, **kwargs):
    # tests overlapping output fails
    t = make_tensor(10, dtype=torch.float32, device=device)
    indices = torch.empty((), device=device, dtype=torch.long)
    si = SampleInput(t, args=(5,), kwargs={'out': (t, indices)})

    k_out_of_range_err = "selected number k out of range for dimension"
    return (ErrorInput(si, error_type=RuntimeError, error_regex="unsupported operation"),
            ErrorInput(SampleInput(torch.randn(2, 2, device=device), args=(3, 0)),
                       error_type=RuntimeError, error_regex=k_out_of_range_err),
            ErrorInput(SampleInput(torch.randn(2, 2, device=device), args=(3,)),
                       error_type=RuntimeError, error_regex=k_out_of_range_err),
            ErrorInput(SampleInput(torch.tensor(2, device=device), args=(3,)),
                       error_type=RuntimeError, error_regex=k_out_of_range_err),)

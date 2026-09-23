def sample_inputs_to_sparse(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    return (SampleInput(make_arg((S, S)), args=(), output_process_fn_grad=lambda x: x.to_dense()),
            SampleInput(make_arg((S, S)), args=(1,), output_process_fn_grad=lambda x: x.to_dense()),)

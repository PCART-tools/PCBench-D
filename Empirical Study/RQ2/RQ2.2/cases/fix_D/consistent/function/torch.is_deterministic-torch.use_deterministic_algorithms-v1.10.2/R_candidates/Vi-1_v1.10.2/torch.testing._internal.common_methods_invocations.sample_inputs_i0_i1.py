def sample_inputs_i0_i1(op_info, device, dtype, requires_grad, **kwargs):

    samples = (SampleInput(make_tensor((S,), device, dtype,
                                       requires_grad=requires_grad)),
               SampleInput(make_tensor((), device, dtype,
                                       requires_grad=requires_grad)))

    if requires_grad and op_info.op == torch.special.i0e:
        # NOTE: `i0e`'s first-order gradient is not continous
        # at `0`, hence we don't test `i0e` with any input being `0`.
        # TODO: Remove this when `make_tensor` supports excluding `0`.
        with torch.no_grad():
            for sample in samples:
                t = sample.input
                t[t == 0] = torch.finfo(dtype).eps  # type: ignore[index]
    elif requires_grad and op_info.op != torch.special.i0e:
        # Special Case for gradient
        # Sample with `0` in the input
        t = make_tensor((S,), device, dtype,
                        requires_grad=requires_grad)

        with torch.no_grad():
            t[0] = 0

        samples += (SampleInput(t),)  # type: ignore[assignment]

    return samples

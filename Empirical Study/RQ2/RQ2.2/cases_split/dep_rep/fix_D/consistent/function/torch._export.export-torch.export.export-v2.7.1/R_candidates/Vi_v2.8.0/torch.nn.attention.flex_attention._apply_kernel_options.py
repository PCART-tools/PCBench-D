def _apply_kernel_options(
    query: Tensor, key: Tensor, value: Tensor, return_lse: bool, kernel_options
):
    kernel_options = {} if kernel_options is None else dict(kernel_options)

    kernel_options.setdefault("PRESCALE_QK", False)
    kernel_options.setdefault("ROWS_GUARANTEED_SAFE", False)
    kernel_options.setdefault("BLOCKS_ARE_CONTIGUOUS", False)
    # This forces all biases grad scatters to be done in the DQ iteration loop of the backwards
    kernel_options.setdefault("WRITE_DQ", True)

    # If forward kernel needs to return logsumexp is decided by this rule internally.
    assert "OUTPUT_LOGSUMEXP" not in kernel_options
    kernel_options["OUTPUT_LOGSUMEXP"] = True
    if not return_lse:
        # We used to check if q,k,v required grads but since captured buffers can require grad
        # we always write unless in no_grad
        output_logsumexp = torch.is_grad_enabled()
        kernel_options["OUTPUT_LOGSUMEXP"] = output_logsumexp
        any_inputs_on_cpu_device = (
            query.device.type == "cpu"
            or key.device.type == "cpu"
            or value.device.type == "cpu"
        )
        if any_inputs_on_cpu_device:
            # CPU with torch.compile now supports infernece, and will not return lse
            # TODO: support CPU for training and return lse
            kernel_options["OUTPUT_LOGSUMEXP"] = False

    return kernel_options

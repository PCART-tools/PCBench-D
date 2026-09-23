def sample_inputs_linalg_eig(op_info, device, dtype, requires_grad=False):
    """
    This function generates input for torch.linalg.eigh with UPLO="U" or "L" keyword argument.
    """
    def out_fn(output):
        return output[0], abs(output[1])

    samples = sample_inputs_linalg_invertible(op_info, device, dtype, requires_grad)
    for sample in samples:
        sample.output_process_fn_grad = out_fn

    return samples

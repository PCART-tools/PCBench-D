def sample_inputs_lu_unpack(op_info, device, dtype, requires_grad=False, **kwargs):
    for lu_sample in sample_inputs_lu(op_info, device, dtype, requires_grad, **kwargs):
        lu_data, pivots = torch.linalg.lu_factor(lu_sample.input)
        lu_data.requires_grad_(requires_grad)
        yield SampleInput(lu_data, args=(pivots,))

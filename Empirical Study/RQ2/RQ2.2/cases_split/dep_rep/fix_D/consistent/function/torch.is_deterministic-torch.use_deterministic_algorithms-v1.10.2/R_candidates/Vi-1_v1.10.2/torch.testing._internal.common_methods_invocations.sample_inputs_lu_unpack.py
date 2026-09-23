def sample_inputs_lu_unpack(op_info, device, dtype, requires_grad=False, **kwargs):
    # not needed once OpInfo tests support Iterables
    def generate_samples():
        for lu_sample in sample_inputs_lu(op_info, device, dtype, requires_grad, **kwargs):
            lu_data, pivots = lu_sample.input.lu()
            yield SampleInput(lu_data, args=(pivots,))

            # generate rectangular inputs
            lu_data_shape = lu_data.shape
            batch_shape = lu_data_shape[:-2]
            n = lu_data_shape[-2]

            for shape_inc in ((1, 0), (0, 1)):
                lu_data, pivots = make_tensor(
                    batch_shape + (n + shape_inc[0], n + shape_inc[1]),
                    device, dtype,
                    requires_grad=False,
                    low=None, high=None
                ).lu()
                lu_data.requires_grad_(requires_grad)
                yield SampleInput(lu_data, args=(pivots,))

    return list(generate_samples())

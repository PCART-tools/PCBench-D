def sample_inputs_hinge_embedding_loss(op_info, device, dtype, requires_grad, **kwargs):
    for input, target, d in _generate_sample_inputs_nn_loss(op_info, device, dtype, requires_grad, **kwargs):
        d['margin'] = random.uniform(-9, 9)
        yield SampleInput(input, args=(target, ), kwargs=d)

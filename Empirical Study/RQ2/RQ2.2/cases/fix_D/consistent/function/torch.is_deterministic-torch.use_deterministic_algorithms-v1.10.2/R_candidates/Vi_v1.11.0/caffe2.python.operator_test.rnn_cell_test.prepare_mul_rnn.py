def prepare_mul_rnn(model, input_blob, shape, T, outputs_with_grad, num_layers):
    print("Shape: ", shape)
    t, n, d = shape
    cells = [MulCell(name="layer_{}".format(i)) for i in range(num_layers)]
    cell = rnn_cell.MultiRNNCell(name="multi_mul_rnn", cells=cells)
    if T is not None:
        cell = rnn_cell.UnrolledCell(cell, T=T)
    states = [
        model.param_init_net.ConstantFill(
            [], "initial_state_{}".format(i), value=1.0, shape=[1, n, d])
        for i in range(num_layers)]
    _, results = cell.apply_over_sequence(
        model=model,
        inputs=input_blob,
        initial_states=states,
        outputs_with_grads=[
            x + 2 * (num_layers - 1) for x in outputs_with_grad
        ],
        seq_lengths=None,
    )
    return results[-2:]

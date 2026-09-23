def max_grad(grad_out, outputs, inputs):
    flat_inputs = inputs[0].flatten()
    flat_outputs = np.array(outputs[0]).flatten()
    flat_grad_in = np.zeros(flat_inputs.shape)
    flat_grad_out = np.array(grad_out).flatten()
    blocks = inputs[0].shape[0]
    if blocks == 0:
        return np.zeros(inputs[0].shape)
    block_size = flat_inputs.shape[0] // blocks

    for i in range(block_size):
        out_grad = flat_grad_out[i]
        out = flat_outputs[i]
        for j in range(blocks):
            idx = j * block_size + i
            # we can produce multiple outputs for max
            if out == flat_inputs[idx]:
                flat_grad_in[idx] = out_grad

    return np.resize(flat_grad_in, inputs[0].shape)

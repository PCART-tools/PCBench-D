def sum_grad(grad_out, outputs, inputs):
    return np.repeat(
        np.expand_dims(grad_out, axis=0),
        inputs[0].shape[0],
        axis=0
    )

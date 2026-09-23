def mean_grad(grad_out, outputs, inputs):
    return np.repeat(
        np.expand_dims(grad_out / inputs[0].shape[0], 0),
        inputs[0].shape[0],
        axis=0
    )

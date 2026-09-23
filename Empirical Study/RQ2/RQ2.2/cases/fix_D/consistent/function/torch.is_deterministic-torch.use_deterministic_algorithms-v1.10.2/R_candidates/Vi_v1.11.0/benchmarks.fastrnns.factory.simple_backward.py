def simple_backward(output, grad_output, **kwargs):
    return output.backward(grad_output, **kwargs)

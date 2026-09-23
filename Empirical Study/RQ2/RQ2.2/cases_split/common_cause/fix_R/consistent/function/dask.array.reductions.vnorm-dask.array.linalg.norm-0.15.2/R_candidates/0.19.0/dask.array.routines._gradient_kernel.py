def _gradient_kernel(f, grad_varargs, grad_kwargs):
    return np.gradient(f, *grad_varargs, **grad_kwargs)

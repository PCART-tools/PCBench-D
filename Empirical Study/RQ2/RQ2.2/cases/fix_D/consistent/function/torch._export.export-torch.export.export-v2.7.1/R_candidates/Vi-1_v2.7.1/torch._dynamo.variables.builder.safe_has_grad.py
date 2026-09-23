def safe_has_grad(t):
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", "The .grad attribute of a Tensor")
        return hasattr(t, "grad")

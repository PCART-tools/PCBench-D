def squareCheckInputs(self: Tensor, f_name: str):
    assert self.dim() >= 2, (
        f"{f_name}: The input tensor must have at least 2 dimensions."
    )
    assert self.size(-1) == self.size(-2), (
        f"{f_name}: A must be batches of square matrices, but they are {self.size(-2)} by {self.size(-1)} matrices"
    )

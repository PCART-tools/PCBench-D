def _validate_pruning_dim(t, dim):
    r"""
    Args:
        t (torch.Tensor): tensor representing the parameter to prune
        dim (int): index of the dim along which we define channels to prune
    """
    if dim >= t.dim():
        raise IndexError("Invalid index {} for tensor of size {}".format(dim, t.shape))

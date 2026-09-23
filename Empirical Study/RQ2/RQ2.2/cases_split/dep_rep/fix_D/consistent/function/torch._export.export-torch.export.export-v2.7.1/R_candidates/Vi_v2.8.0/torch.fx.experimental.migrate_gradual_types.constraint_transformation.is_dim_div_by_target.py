def is_dim_div_by_target(target: list[int], dim: list[DVar]):
    """
    Generate constraints to check if the input dimensions is divisible by the target dimensions
    Args:
        target: Target dimensions
        dim:  Input dimensions

    Returns: Constraints to check divisibility

    """
    return BinConstraintD(BinConstraintD(dim, Prod(target), op_mod), 0, op_eq)

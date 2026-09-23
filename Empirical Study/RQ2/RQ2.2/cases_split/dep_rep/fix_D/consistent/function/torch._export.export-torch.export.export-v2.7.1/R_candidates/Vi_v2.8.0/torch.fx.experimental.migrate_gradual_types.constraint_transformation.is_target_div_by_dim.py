def is_target_div_by_dim(target: list[int], dim: list[DVar]):
    """
    Generate constraints to check if the target dimensions are divisible by the input dimensions
    Args:
        target: Target dimensions
        dim: Input dimensions

    Returns: Constraints to check divisibility

    """
    return BinConstraintD(BinConstraintD(Prod(target), dim, op_mod), 0, op_eq)

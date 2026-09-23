def get_positive_dim(dim: int, dim_size: int) -> int:
    """
    Given an integer number that represents a dimension in the array,
    transform it to a positive integer dim if it's negative. Otherwise, do
    nothing.

    Args:
        dim (int): A integer number that represents a dimension in an array.
        dim_size (int): The size of the dimension in the array.

    Returns:
        A positive integer that represent the same dimension as the given dim.
    """
    if dim < 0:
        return dim % dim_size
    return dim

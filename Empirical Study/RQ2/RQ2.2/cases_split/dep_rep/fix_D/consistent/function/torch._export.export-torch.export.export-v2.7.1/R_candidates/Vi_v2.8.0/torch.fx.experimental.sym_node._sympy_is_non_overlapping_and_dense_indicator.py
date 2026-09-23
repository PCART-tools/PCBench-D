def _sympy_is_non_overlapping_and_dense_indicator(sizes, strides):
    from torch.utils._sympy.functions import IsNonOverlappingAndDenseIndicator

    return IsNonOverlappingAndDenseIndicator(*sizes, *strides)

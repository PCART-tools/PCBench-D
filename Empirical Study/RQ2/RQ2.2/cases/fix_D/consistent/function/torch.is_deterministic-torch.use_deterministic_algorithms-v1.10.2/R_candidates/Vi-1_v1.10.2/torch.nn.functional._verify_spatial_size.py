def _verify_spatial_size(size: List[int]) -> None:
    # Verify that there is > 1 spatial element for instance norm calculation.
    size_prods = 1
    for i in range(2, len(size)):
        size_prods *= size[i]
    if size_prods == 1:
        raise ValueError("Expected more than 1 spatial element when training, got input size {}".format(size))

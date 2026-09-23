def _check_max_grid_x(size_hints, x, num_warps):
    # Check if maxGridSize is exceeded - if so then must scale XBLOCK further
    max_grid_x = 2147483647
    warp_size = (
        64 if torch.version.hip else 32
    )  # TODO: query warp size once #129663 is merged
    num_blocks = (size_hints["x"] + x - 1) // x

    while (num_blocks * num_warps * warp_size) > max_grid_x and x < size_hints["x"]:
        x *= 2  # Scale up XBLOCK if grid exceeds limits
        num_blocks = num_blocks // 2
    if (num_blocks * num_warps * warp_size) > max_grid_x:
        raise AssertionError(
            "Reduction config exceeds cudaDeviceProp maxGridSize. Please raise a pytorch issue"
        )
    return x, num_blocks

def pooling_size(x, i, kernel_size, stride, padding, ceil_mode, *, dilation=None):
    if dilation is None:
        dilation = [1] * len(padding)

    x_out = FloorDiv(
        x + 2 * padding[i] - dilation[i] * (kernel_size[i] - 1) + (stride[i] - 1),
        stride[i],
    )

    if ceil_mode:
        x_alt = FloorDiv(
            x
            + 2 * padding[i]
            - dilation[i] * (kernel_size[i] - 1)
            + 2 * (stride[i] - 1),
            stride[i],
        )
        if V.graph.sizevars.size_hint((x_alt - 1) * stride[i] - x - padding[i]) >= 0:
            # Sliding windows must start within the input or left padding
            x_alt -= 1  # type: ignore[assignment]
            V.graph.sizevars.guard_leq(0, x_alt * stride[i] - x - padding[i])  # type: ignore[arg-type]
        if V.graph.sizevars.size_hint(x_out - x_alt) == 0:
            # ceil mode is actually a no-op, lets guard on that
            V.graph.sizevars.guard_equals(x_out, x_alt)
            ceil_mode = False
        else:
            x_out = x_alt
    return x_out, ceil_mode

def pool_output_shape(input_size, kernel_size, padding, stride,
                      dilation, ceiling_mode=False):
    if stride is None:
        stride = kernel_size
    output_size = (
        (input_size + 2 * padding - dilation * (kernel_size - 1) - 1
         + (stride - 1 if ceiling_mode else 0)) // stride + 1)
    if (ceiling_mode and
            ((output_size - 1) * stride >= input_size + padding)):
        output_size -= 1
    return output_size

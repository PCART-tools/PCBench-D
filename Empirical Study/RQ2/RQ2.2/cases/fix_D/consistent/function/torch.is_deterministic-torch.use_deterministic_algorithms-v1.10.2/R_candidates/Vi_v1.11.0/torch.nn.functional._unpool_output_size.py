def _unpool_output_size(
    input: Tensor, kernel_size: List[int], stride: List[int], padding: List[int], output_size: Optional[List[int]]
) -> List[int]:
    input_size = input.size()
    default_size = torch.jit.annotate(List[int], [])
    for d in range(len(kernel_size)):
        default_size.append((input_size[-len(kernel_size) + d] - 1) * stride[d] + kernel_size[d] - 2 * padding[d])
    if output_size is None:
        ret = default_size
    else:
        if len(output_size) == len(kernel_size) + 2:
            output_size = output_size[2:]
        if len(output_size) != len(kernel_size):
            raise ValueError(
                "output_size should be a sequence containing "
                "{} or {} elements, but it has a length of '{}'".format(
                    len(kernel_size), len(kernel_size) + 2, len(output_size)
                )
            )
        for d in range(len(kernel_size)):
            min_size = default_size[d] - stride[d]
            max_size = default_size[d] + stride[d]
            if not (min_size < output_size[d] < max_size):
                raise ValueError(
                    'invalid output_size "{}" (dim {} must be between {} and {})'.format(
                        output_size, d, min_size, max_size
                    )
                )

        ret = output_size
    return ret

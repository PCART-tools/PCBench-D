def generate_data_for_repeat():
    input_tensors = [torch.randn(*input_shape) for input_shape in input_shapes]
    total_num_elements = 0
    for input_tensor, repeat in zip(input_tensors, repeats):
        total_num_elements += input_tensor.numel()
        total_num_elements += input_tensor.numel() * np.prod(repeat)
    return input_tensors, (total_num_elements * DTYPE_TO_BYTES['float'])

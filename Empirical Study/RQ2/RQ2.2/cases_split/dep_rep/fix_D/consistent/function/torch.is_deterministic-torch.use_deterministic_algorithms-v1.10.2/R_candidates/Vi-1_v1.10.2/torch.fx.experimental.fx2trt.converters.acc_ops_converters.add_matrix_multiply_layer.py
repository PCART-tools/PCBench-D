def add_matrix_multiply_layer(network, input_val, other_val, name, transpose_input=False, transpose_other=False):
    """ Adds a matrix multiply layer to the TensorRT network
    Args:
        network: TensorRT Network
        input_val: input matrix/vector TensorRT ITensor
        other_val: another input matrix/vector TensorRT ITensor
        name: Name of the matrix multiply layer
        transpose_input: boolean indicating whether to transpose the input_val Tensor or not
        transpose_other: boolean indicaiton whether to transpose the other_val Tensor or not
    Returns:
        output TensorRT ITensor from the matrix multiply layer
    """
    input_matrix_op = other_matrix_op = trt.MatrixOperation.NONE
    preset_diff = 0

    if len(input_val.shape) == 1:
        assert not transpose_input, "can't transpose input vector"
        preset_diff -= 1
        input_matrix_op = trt.MatrixOperation.VECTOR
    elif transpose_input:
        input_matrix_op = trt.MatrixOperation.TRANSPOSE

    if len(other_val.shape) == 1:
        assert not transpose_input, "can't transpose other vector"
        preset_diff += 1
        other_matrix_op = trt.MatrixOperation.VECTOR
    elif transpose_other:
        other_matrix_op = trt.MatrixOperation.TRANSPOSE


    input_val, other_val = broadcast(network, input_val, other_val, f"{name}_input", f"{name}_other", preset_diff)
    layer = network.add_matrix_multiply(input_val, input_matrix_op, other_val, other_matrix_op)
    layer.name = name
    return layer.get_output(0)

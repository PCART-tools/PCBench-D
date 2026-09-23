def grad(output_grad, ref_outputs, inputs):
    return (divide_by_square_root(output_grad, inputs[1])[0],
            None)

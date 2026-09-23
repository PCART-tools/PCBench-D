def copy_slices_epilogue(needs_input_grad, result, res, grad_slice):
    grad_inputs = [None] * len(needs_input_grad)
    for i in range(len(needs_input_grad)):
        if needs_input_grad[i]:
            if res[i] is None:
                continue
            if i == 0:
                grad_slice.copy_(res[i])
                grad_inputs[i] = result
            else:
                grad_inputs[i] = res[i]
    return grad_inputs

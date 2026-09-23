def set_cpp_tensors_requires_grad(cpp_tensor_stmts, python_tensors):
    assert len(cpp_tensor_stmts) == len(python_tensors)
    return ['{}.requires_grad_(true)'.format(tensor_stmt) if tensor.dtype != torch.long else tensor_stmt
            for tensor_stmt, (_, tensor) in zip(cpp_tensor_stmts, python_tensors)]

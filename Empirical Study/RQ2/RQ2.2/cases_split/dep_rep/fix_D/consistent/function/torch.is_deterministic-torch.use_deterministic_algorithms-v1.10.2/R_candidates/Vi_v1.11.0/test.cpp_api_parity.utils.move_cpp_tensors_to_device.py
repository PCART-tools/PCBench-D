def move_cpp_tensors_to_device(cpp_tensor_stmts, device):
    return ['{}.to("{}")'.format(tensor_stmt, device) for tensor_stmt in cpp_tensor_stmts]

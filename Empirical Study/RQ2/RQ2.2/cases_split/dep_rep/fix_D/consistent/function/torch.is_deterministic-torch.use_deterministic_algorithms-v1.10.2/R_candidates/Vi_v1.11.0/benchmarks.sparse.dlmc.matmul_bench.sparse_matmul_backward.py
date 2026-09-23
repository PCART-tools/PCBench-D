def sparse_matmul_backward(a, b, grad_output):
    c = torch.sparse.mm(a, b)
    c.backward(grad_output)

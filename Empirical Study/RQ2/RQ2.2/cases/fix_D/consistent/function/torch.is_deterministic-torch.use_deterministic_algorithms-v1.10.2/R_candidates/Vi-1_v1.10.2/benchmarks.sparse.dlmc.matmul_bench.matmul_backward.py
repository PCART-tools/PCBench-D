def matmul_backward(a_dense, b_dense, grad_output):
    r1 = a_dense.matmul(b_dense)
    r1.backward(grad_output)

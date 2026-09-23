def sample_inputs_einsum(op_info, device, dtype, requires_grad=False, **kwargs):
    def c(t):
        return t.clone().requires_grad_(requires_grad)

    x = make_tensor((3,), device, dtype, requires_grad=requires_grad)
    y = make_tensor((4,), device, dtype, requires_grad=requires_grad)
    A = make_tensor((2, 3,), device, dtype, requires_grad=requires_grad)
    B = make_tensor((1, 3,), device, dtype, requires_grad=requires_grad)
    C = make_tensor((1, 2, 3,), device, dtype, requires_grad=requires_grad)
    D = make_tensor((1, 3, 4,), device, dtype, requires_grad=requires_grad)
    E = make_tensor((4, 4,), device, dtype, requires_grad=requires_grad)
    H = make_tensor((3, 3,), device, dtype, requires_grad=requires_grad)
    I = make_tensor((1, 3, 1,), device, dtype, requires_grad=requires_grad)

    inputs = []

    # Vector operations
    inputs.append(SampleInput([c(x)], args=('i->',)))                      # sum
    inputs.append(SampleInput([c(x), c(y)], args=('i,j->ij',)))               # outer

    # Matrix operations
    inputs.append(SampleInput([c(A)], args=("ij->i",)))                    # col sum
    inputs.append(SampleInput([c(A), c(B)], args=("ij,kj->ik",)))             # matmul
    inputs.append(SampleInput([c(A), c(E)], args=("ij,Ab->ijAb",)))           # matrix outer product

    # Tensor operations
    inputs.append(SampleInput([c(C), c(D)], args=("aij,ajk->aik",)))          # batch matmul
    inputs.append(SampleInput([c(D), c(E)], args=("aij,jk->aik",)))           # tensor matrix contraction
    inputs.append(SampleInput([c(C), c(B)], args=("ijk,ik->j",)))             # non contiguous

    # Test diagonals
    inputs.append(SampleInput([c(I)], args=('iji->j',)))                   # non-contiguous trace

    # Test ellipsis
    inputs.append(SampleInput([c(H)], args=("i...->...",)))
    inputs.append(SampleInput([c(C), c(x)], args=('...ik, ...j -> ij',)))

    return inputs

def sample_inputs_einsum(op_info, device, dtype, requires_grad=False, **kwargs):
    x = make_tensor((3,), device, dtype, requires_grad=requires_grad)
    y = make_tensor((4,), device, dtype, requires_grad=requires_grad)
    A = make_tensor((2, 3,), device, dtype, requires_grad=requires_grad, noncontiguous=True)
    B = make_tensor((1, 3,), device, dtype, requires_grad=requires_grad)
    C = make_tensor((1, 2, 3,), device, dtype, requires_grad=requires_grad)
    D = make_tensor((1, 3, 4,), device, dtype, requires_grad=requires_grad, noncontiguous=True)
    E = make_tensor((4, 4,), device, dtype, requires_grad=requires_grad)
    H = make_tensor((3, 3,), device, dtype, requires_grad=requires_grad, noncontiguous=True)
    I = make_tensor((1, 3, 1,), device, dtype, requires_grad=requires_grad)

    inputs = []

    # Vector operations
    inputs.append(SampleInput([x], args=('i->',)))                      # sum
    inputs.append(SampleInput([x, y], args=('i,j->ij',)))               # outer

    # Matrix operations
    inputs.append(SampleInput([A], args=("ij->i",)))                    # col sum
    inputs.append(SampleInput([A, B], args=("ij,kj->ik",)))             # matmul
    inputs.append(SampleInput([A, E], args=("ij,Ab->ijAb",)))           # matrix outer product

    # Tensor operations
    inputs.append(SampleInput([C, D], args=("aij,ajk->aik",)))          # batch matmul
    inputs.append(SampleInput([D, E], args=("aij,jk->aik",)))           # tensor matrix contraction
    inputs.append(SampleInput([C, B], args=("ijk,ik->j",)))             # non contiguous

    # Test diagonals
    inputs.append(SampleInput([I], args=('iji->j',)))                   # non-contiguous trace

    # Test ellipsis
    inputs.append(SampleInput([H], args=("i...->...",)))
    inputs.append(SampleInput([C, x], args=('...ik, ...j -> ij',)))

    return inputs

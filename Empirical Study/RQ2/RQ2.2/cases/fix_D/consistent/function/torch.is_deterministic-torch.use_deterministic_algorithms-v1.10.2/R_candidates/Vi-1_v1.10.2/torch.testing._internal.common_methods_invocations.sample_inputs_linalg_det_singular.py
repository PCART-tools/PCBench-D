def sample_inputs_linalg_det_singular(op_info, device, dtype, requires_grad):
    make_arg = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    def make_singular_matrix_batch_base(size, rank):
        assert size[-1] == size[-2]
        assert rank > 0 and rank <= size[-1]

        with torch.no_grad():
            n = size[-1]
            a = make_arg(size[:-2] + (n, rank)) / 10
            b = make_arg(size[:-2] + (rank, n)) / 10

            x = a @ b
            lu, pivs = x.lu()
            p, l, u = torch.lu_unpack(lu, pivs)
            u_diag_abs = u.diagonal(0, -2, -1).abs()
            u_diag_abs_largest = u_diag_abs.max(dim=-1, keepdim=True).values
            u_diag_abs_smallest_idxs = torch.topk(u_diag_abs, k=(n - rank), largest=False).indices
            u.diagonal(0, -2, -1).div_(u_diag_abs_largest)
            u.diagonal(0, -2, -1)[..., u_diag_abs_smallest_idxs] = torch.finfo(dtype).eps

            matrix = p @ l @ u

        assert (matrix.det().abs() < torch.finfo(dtype).eps * torch.linalg.matrix_norm(matrix)).all().item()

        matrix.requires_grad_(requires_grad)
        return matrix

    def sample_generator():
        for batch, size in product(((), (2,), (2, 2)), range(6)):
            shape = batch + (size, size)
            for rank in range(1, size):
                yield make_singular_matrix_batch_base(shape, rank)

    return [SampleInput(t) for t in sample_generator()]

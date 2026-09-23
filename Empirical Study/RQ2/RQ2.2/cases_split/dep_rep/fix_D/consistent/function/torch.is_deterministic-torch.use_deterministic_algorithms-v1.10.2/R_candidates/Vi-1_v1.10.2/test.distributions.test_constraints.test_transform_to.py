@pytest.mark.parametrize('constraint_fn, args', [(c[0], c[1:]) for c in CONSTRAINTS])
@pytest.mark.parametrize('is_cuda', [False,
                                     pytest.param(True, marks=pytest.mark.skipif(not TEST_CUDA,
                                                                                 reason='CUDA not found.'))])
def test_transform_to(constraint_fn, args, is_cuda):
    constraint = build_constraint(constraint_fn, args, is_cuda=is_cuda)
    t = transform_to(constraint)
    if constraint_fn is constraints.corr_cholesky:
        # (D * (D-1)) / 2 (where D = 4) = 6 (size of last dim)
        x = torch.randn(6, 6, dtype=torch.double)
    else:
        x = torch.randn(5, 5, dtype=torch.double)
    if is_cuda:
        x = x.cuda()
    y = t(x)
    assert constraint.check(y).all(), "Failed to transform_to({})".format(constraint)
    x2 = t.inv(y)
    y2 = t(x2)
    assert torch.allclose(y, y2), "Error in transform_to({}) pseudoinverse".format(constraint)

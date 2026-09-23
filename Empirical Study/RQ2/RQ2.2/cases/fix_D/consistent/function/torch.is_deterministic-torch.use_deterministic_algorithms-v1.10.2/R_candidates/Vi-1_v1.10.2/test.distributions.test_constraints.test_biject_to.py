@pytest.mark.parametrize('constraint_fn, args', [(c[0], c[1:]) for c in CONSTRAINTS])
@pytest.mark.parametrize('is_cuda', [False,
                                     pytest.param(True, marks=pytest.mark.skipif(not TEST_CUDA,
                                                                                 reason='CUDA not found.'))])
def test_biject_to(constraint_fn, args, is_cuda):
    constraint = build_constraint(constraint_fn, args, is_cuda=is_cuda)
    try:
        t = biject_to(constraint)
    except NotImplementedError:
        pytest.skip('`biject_to` not implemented.')
    assert t.bijective, "biject_to({}) is not bijective".format(constraint)
    if constraint_fn is constraints.corr_cholesky:
        # (D * (D-1)) / 2 (where D = 4) = 6 (size of last dim)
        x = torch.randn(6, 6, dtype=torch.double)
    else:
        x = torch.randn(5, 5, dtype=torch.double)
    if is_cuda:
        x = x.cuda()
    y = t(x)
    assert constraint.check(y).all(), '\n'.join([
        "Failed to biject_to({})".format(constraint),
        "x = {}".format(x),
        "biject_to(...)(x) = {}".format(y),
    ])
    x2 = t.inv(y)
    assert torch.allclose(x, x2), "Error in biject_to({}) inverse".format(constraint)

    j = t.log_abs_det_jacobian(x, y)
    assert j.shape == x.shape[:x.dim() - t.domain.event_dim]

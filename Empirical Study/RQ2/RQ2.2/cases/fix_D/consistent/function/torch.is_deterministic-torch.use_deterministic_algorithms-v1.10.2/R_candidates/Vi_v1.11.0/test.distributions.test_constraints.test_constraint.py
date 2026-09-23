@pytest.mark.parametrize('constraint_fn, result, value', EXAMPLES)
@pytest.mark.parametrize('is_cuda', [False,
                                     pytest.param(True, marks=pytest.mark.skipif(not TEST_CUDA,
                                                                                 reason='CUDA not found.'))])
def test_constraint(constraint_fn, result, value, is_cuda):
    t = torch.cuda.DoubleTensor if is_cuda else torch.DoubleTensor
    assert constraint_fn.check(t(value)).all() == result

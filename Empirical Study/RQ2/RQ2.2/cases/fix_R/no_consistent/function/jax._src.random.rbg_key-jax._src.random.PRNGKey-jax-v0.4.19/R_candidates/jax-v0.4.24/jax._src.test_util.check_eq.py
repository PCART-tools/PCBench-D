def check_eq(xs, ys, err_msg=''):
  assert_close = partial(_assert_numpy_allclose, err_msg=err_msg)
  tree_all(tree_map(assert_close, xs, ys))

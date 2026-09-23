def check_jvp(f, f_jvp, args, atol=None, rtol=None, eps=EPS, err_msg=''):
  atol = _merge_tolerance(atol, default_gradient_tolerance)
  rtol = _merge_tolerance(rtol, default_gradient_tolerance)
  rng = np.random.RandomState(0)
  tangent = tree_map(partial(rand_like, rng), args)
  v_out, t_out = f_jvp(args, tangent)
  _check_dtypes_match(v_out, t_out)
  v_out_expected = f(*args)
  _check_dtypes_match(v_out, v_out_expected)
  t_out_expected = numerical_jvp(f, args, tangent, eps=eps)
  # In principle we should expect exact equality of v_out and v_out_expected,
  # but due to nondeterminism especially on GPU (e.g., due to convolution
  # autotuning) we only require "close".
  check_close(v_out, v_out_expected, atol=atol, rtol=rtol,
              err_msg=f'{err_msg} primal' if err_msg else 'primal')
  check_close(t_out, t_out_expected, atol=atol, rtol=rtol,
              err_msg=f'{err_msg} tangent' if err_msg else 'tangent')

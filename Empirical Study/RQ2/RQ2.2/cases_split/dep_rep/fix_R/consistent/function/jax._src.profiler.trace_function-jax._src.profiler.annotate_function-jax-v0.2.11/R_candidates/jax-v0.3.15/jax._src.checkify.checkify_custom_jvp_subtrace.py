@lu.transformation_with_aux
def checkify_custom_jvp_subtrace(main, msgs, *args):
  # Like checkify_subtrace, but used specifically on the custom JVP rules
  # associated with a custom_jvp. This code is called in the context of a
  # jvp-of-checkify-of-custom_jvp. It takes both primal and tangent inputs,
  # flattened into a single args tuple, and similarly must produce flattened
  # primal and tangent outputs. Both primals and tangents include error values,
  # but the tangent error values are trivially zero.
  # The types to have in mind are:
  #   jvp : (a -> b) -> (a, T a) -> (b, T b)
  #   checkify : (a -> b) -> a -> Err b
  #   jvp-of-checkify : (a -> b) -> (a, T a) -> (Err b, T (Err b))
  # where because Err is a pytree, we necessarily have T (Err b) = Err' (T b)
  # where the other Err' components are trivial (of float0 dtype).
  # Semantically, we don't add checks to the JVP rule. To check the result of a
  # JVP rule, one must instead use checkify-of-jvp. Thus this implementation
  # just forwards the input error and code (and trivial tangents) to the output.
  del main
  n, ragged = divmod(len(args), 2)
  assert not ragged
  (err,), (code,), (payload,), primals = split_list(args[:n], [1, 1, 1])
  (err_dot,), (code_dot,), (pl_dot,), tangents = split_list(args[n:], [1, 1, 1])
  outs = yield (*primals, *tangents), {}
  m, ragged = divmod(len(outs), 2)
  assert not ragged
  out_primals, out_tangents = outs[:m], outs[m:]
  yield (err, code, payload, *out_primals,
         err_dot, code_dot, pl_dot, *out_tangents), dict(msgs)

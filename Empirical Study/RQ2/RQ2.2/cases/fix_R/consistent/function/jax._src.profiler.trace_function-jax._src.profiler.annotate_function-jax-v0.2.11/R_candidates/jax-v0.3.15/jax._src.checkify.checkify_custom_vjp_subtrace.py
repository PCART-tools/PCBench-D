@lu.transformation_with_aux
def checkify_custom_vjp_subtrace(main, msgs, err, code, payload, *args):
  # We don't add any checks; just drop input error values.
  del main, err, code, payload
  outs = yield args, {}
  yield outs, dict(msgs)

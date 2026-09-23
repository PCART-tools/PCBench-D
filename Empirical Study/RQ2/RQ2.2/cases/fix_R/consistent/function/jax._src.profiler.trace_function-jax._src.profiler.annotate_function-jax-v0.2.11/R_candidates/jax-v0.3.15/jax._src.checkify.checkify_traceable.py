@lu.transformation
def checkify_traceable(msgs, enabled_errors, err, code, payload, *args):
  with core.new_main(CheckifyTrace, enabled_errors=enabled_errors) as main:
    outs = yield (main, msgs, err, code, payload, *args), {}
    del main
  yield outs

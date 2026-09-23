def _typecheck_param(prim, param, name, msg_required, pred):
  if not pred:
    msg = (f'invalid {prim} param {name} of type {type(param).__name__}, '
           f'{msg_required} required:')
    param_str = str(param)
    sep = os.linesep if os.linesep in param_str else ' '
    msg = sep.join([msg, param_str])
    raise core.JaxprTypeError(msg)

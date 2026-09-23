def check_special(name, bufs):
  if needs_check_special():
    for buf in bufs:
      _check_special(name, buf.dtype, buf)

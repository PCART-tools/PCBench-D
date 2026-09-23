def fun_name(f):
  try:
    return f.__name__
  except:
    return str(f)

def format_exception_only(e):
  return ''.join(traceback.format_exception_only(type(e), e)).strip()

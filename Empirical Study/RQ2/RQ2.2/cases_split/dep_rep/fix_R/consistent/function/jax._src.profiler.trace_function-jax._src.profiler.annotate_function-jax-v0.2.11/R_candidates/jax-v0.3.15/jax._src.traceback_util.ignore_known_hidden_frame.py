def ignore_known_hidden_frame(f):
  return 'importlib._bootstrap' in f.f_code.co_filename

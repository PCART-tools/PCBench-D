def setnewattr(obj, name, val):
  sentinel = object()
  assert getattr(obj, name, sentinel) is sentinel
  setattr(obj, name, val)

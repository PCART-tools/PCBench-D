def _str(self):
    with torch.no_grad():
        return _str_intern(self)

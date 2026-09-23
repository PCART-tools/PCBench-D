  def join(self, xt, yt):
    xz, yz = type(xt) is Zero, type(yt) is Zero
    if xz == yz:
      return xt, yt
    elif yz and not xz:
      return xt, zeros_like_jaxval(xt)
    elif xz and not yz:
      return zeros_like_jaxval(yt), yt
    else:
      raise TypeError((xt, yt))

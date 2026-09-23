class _Bfloat16MachArLike:
  def __init__(self):
    smallest_normal = float.fromhex("0x1p-126")
    self.smallest_normal = bfloat16(smallest_normal)

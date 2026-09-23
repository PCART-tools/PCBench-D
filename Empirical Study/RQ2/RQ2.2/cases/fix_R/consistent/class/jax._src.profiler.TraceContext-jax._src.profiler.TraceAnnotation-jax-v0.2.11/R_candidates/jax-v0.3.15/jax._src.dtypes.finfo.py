class finfo(np.finfo):
  __doc__ = np.finfo.__doc__
  _finfo_cache: Dict[np.dtype, np.finfo] = {}
  @staticmethod
  def _bfloat16_finfo():
    def float_to_str(f):
      return "%12.4e" % float(f)

    bfloat16 = _bfloat16_dtype.type
    tiny = float.fromhex("0x1p-126")
    resolution = 0.01
    eps = float.fromhex("0x1p-7")
    epsneg = float.fromhex("0x1p-8")
    max = float.fromhex("0x1.FEp127")

    obj = object.__new__(np.finfo)
    obj.dtype = _bfloat16_dtype
    obj.bits = 16
    obj.eps = bfloat16(eps)
    obj.epsneg = bfloat16(epsneg)
    obj.machep = -7
    obj.negep = -8
    obj.max = bfloat16(max)
    obj.min = bfloat16(-max)
    obj.nexp = 8
    obj.nmant = 7
    obj.iexp = obj.nexp
    obj.precision = 2
    obj.resolution = bfloat16(resolution)
    obj._machar = _Bfloat16MachArLike()
    if not hasattr(obj, "tiny"):
      obj.tiny = bfloat16(tiny)

    obj._str_tiny = float_to_str(tiny)
    obj._str_smallest_normal = float_to_str(tiny)
    obj._str_max = float_to_str(max)
    obj._str_epsneg = float_to_str(epsneg)
    obj._str_eps = float_to_str(eps)
    obj._str_resolution = float_to_str(resolution)
    return obj

  def __new__(cls, dtype):
    if isinstance(dtype, str) and dtype == 'bfloat16' or dtype == _bfloat16_dtype:
      if _bfloat16_dtype not in cls._finfo_cache:
        cls._finfo_cache[_bfloat16_dtype] = cls._bfloat16_finfo()
      return cls._finfo_cache[_bfloat16_dtype]
    return super().__new__(cls, dtype)

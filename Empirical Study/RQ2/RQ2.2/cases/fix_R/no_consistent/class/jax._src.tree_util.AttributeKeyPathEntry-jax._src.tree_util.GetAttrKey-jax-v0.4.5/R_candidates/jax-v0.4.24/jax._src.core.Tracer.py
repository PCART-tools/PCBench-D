class Tracer(typing.Array, metaclass=StrictABCMeta):
  __array_priority__ = 1000
  __slots__ = ['_trace', '_line_info']

  dtype = _aval_property('dtype')
  ndim = _aval_property('ndim')
  size = _aval_property('size')
  shape = _aval_property('shape')

  def __init__(self, trace: Trace):
    self._trace = trace

  def _error_repr(self):
    if self.aval is None:
      return f"traced array with aval {self.aval}"
    return f"traced array with shape {raise_to_shaped(self.aval).str_short()}."

  def __array__(self, *args, **kw):
    raise TracerArrayConversionError(self)

  def __dlpack__(self, *args, **kw):
    raise ConcretizationTypeError(self,
      f"The __dlpack__() method was called on {self._error_repr()}."
      f"{self._origin_msg()}")

  def tolist(self):
    raise ConcretizationTypeError(self,
      f"The tolist() method was called on {self._error_repr()}."
      f"{self._origin_msg()}")

  def tobytes(self, order="C"):
    del order
    raise ConcretizationTypeError(self,
      f"The tobytes() method was called on {self._error_repr()}."
      f"{self._origin_msg()}")

  def __iter__(self):
    return iter(self.aval._iter(self))

  def __reversed__(self):
    return iter(self[::-1])

  def __len__(self):
    return self.aval._len(self)

  @property
  def sharding(self):
    # This attribute is part of the jax.Array API, but only defined on concrete arrays.
    # Raising a ConcretizationTypeError would make sense, but for backward compatibility
    # we raise an AttributeError so that hasattr() and getattr() work as expected.
    raise AttributeError(self,
      f"The 'sharding' attribute is not available on {self._error_repr()}."
      f"{self._origin_msg()}")

  @property
  def addressable_shards(self):
    raise ConcretizationTypeError(self,
      f"The 'addressable_shards' attribute is not available on {self._error_repr()}."
      f"{self._origin_msg()}")

  @property
  def at(self):
    return self.aval.at.fget(self)

  @property
  def aval(self):
    raise NotImplementedError("must override")

  def _assert_live(self) -> None:
    pass  # Override for liveness checking

  def get_referent(self) -> Any:
    return self  # Override for object equivalence checking

  def __bool__(self):
    check_bool_conversion(self)
    return self.aval._bool(self)

  def __int__(self):
    check_scalar_conversion(self)
    return self.aval._int(self)

  def __float__(self):
    check_scalar_conversion(self)
    return self.aval._float(self)

  def __complex__(self):
    check_scalar_conversion(self)
    return self.aval._complex(self)

  def __hex__(self):
    check_integer_conversion(self)
    return self.aval._hex(self)

  def __oct__(self):
    check_integer_conversion(self)
    return self.aval._oct(self)

  def __index__(self):
    check_integer_conversion(self)
    raise self.aval._index(self)

  # raises a useful error on attempts to pickle a Tracer.
  def __reduce__(self):
    raise ConcretizationTypeError(
      self, ("The error occurred in the __reduce__ method, which may "
             "indicate an attempt to serialize/pickle a traced value."))

  # raises the better error message from ShapedArray
  def __setitem__(self, idx, val): return self.aval._setitem(self, idx, val)

  # NumPy also only looks up special methods on classes.
  def __array_module__(self, types): return self.aval._array_module(self, types)

  def __getattr__(self, name):
    # if the aval property raises an AttributeError, gets caught here
    assert not config.enable_checks.value or name != "aval"

    try:
      attr = getattr(self.aval, name)
    except AttributeError as err:
      raise AttributeError(
          f"{self.__class__.__name__} has no attribute {name}"
      ) from err
    else:
      t = type(attr)
      if t is aval_property:
        return attr.fget(self)
      elif t is aval_method:
        return types.MethodType(attr.fun, self)
      else:
        return attr

  def _pretty_print(self):
    base = pp.text(f'Traced<{self.aval}>with<{self._trace}>')
    contents = [(name, attr._pretty_print() if isinstance(attr, Tracer)
                 else pp.text(repr(attr))) for name, attr in self._contents()]
    if contents:
      base = pp.group(pp.nest(2, pp.concat([
        base, pp.text(' with'), pp.brk(), pp.join(pp.brk(), [
          pp.text(f'{name} = ') + pp_payload
          for name, pp_payload in contents])
      ])))
    return base

  def __repr__(self):
    return self._pretty_print().format()

  def _contents(self):
    try:
      return [(name, getattr(self, name)) for name in self.__slots__]
    except AttributeError:
      return ()

  def _origin_msg(self) -> str:
    return ""

  # Methods that are only valid for materialized arrays
  def addressable_data(self, index):
    raise ConcretizationTypeError(self,
      f"The addressable_data() method was called on {self._error_repr()}."
      f"{self._origin_msg()}")

  @property
  def block_until_ready(self):
    # Raise AttribureError for backward compatibility with hasattr() and getattr() checks.
    raise AttributeError(self,
      f"The 'block_until_ready' method is not available on {self._error_repr()}."
      f"{self._origin_msg()}")

  @property
  def copy_to_host_async(self):
    # Raise AttribureError for backward compatibility with hasattr() and getattr() checks.
    raise AttributeError(self,
      f"The 'copy_to_host_async' method is not available on {self._error_repr()}."
      f"{self._origin_msg()}")

  def delete(self):
    raise ConcretizationTypeError(self,
      f"The delete() method was called on {self._error_repr()}."
      f"{self._origin_msg()}")

  def device(self):
    raise ConcretizationTypeError(self,
      f"The device() method was called on {self._error_repr()}."
      f"{self._origin_msg()}")

  def devices(self):
    raise ConcretizationTypeError(self,
      f"The devices() method was called on {self._error_repr()}."
      f"{self._origin_msg()}")

  @property
  def global_shards(self):
    raise ConcretizationTypeError(self,
      f"The global_shards property was called on {self._error_repr()}."
      f"{self._origin_msg()}")

  def is_deleted(self):
    raise ConcretizationTypeError(self,
      f"The is_deleted() method was called on {self._error_repr()}."
      f"{self._origin_msg()}")

  @property
  def is_fully_addressable(self):
    raise ConcretizationTypeError(self,
      f"The is_fully_addressable property was called on {self._error_repr()}."
      f"{self._origin_msg()}")

  @property
  def is_fully_replicated(self):
    raise ConcretizationTypeError(self,
      f"The is_fully_replicated property was called on {self._error_repr()}."
      f"{self._origin_msg()}")

  def on_device_size_in_bytes(self):
    raise ConcretizationTypeError(self,
      f"The on_device_size_in_bytes() method was called on {self._error_repr()}."
      f"{self._origin_msg()}")

  @property
  def traceback(self):
    raise ConcretizationTypeError(self,
      f"The traceback property was called on {self._error_repr()}."
      f"{self._origin_msg()}")

  def unsafe_buffer_pointer(self):
    raise ConcretizationTypeError(self,
      f"The unsafe_buffer_pointer() method was called on {self._error_repr()}."
      f"{self._origin_msg()}")

def StringifyProto(obj):
    """Stringify a protocol buffer object.

  Inputs:
    obj: a protocol buffer object, or a Pycaffe2 object that has a Proto()
        function.
  Outputs:
    string: the output protobuf string.
  Raises:
    AttributeError: if the passed in object does not have the right attribute.
  """
    if isinstance(obj, basestring):
        return obj
    else:
        if isinstance(obj, Message):
            # First, see if this object is a protocol buffer, which we can
            # simply serialize with the SerializeToString() call.
            return obj.SerializeToString()
        elif hasattr(obj, 'Proto'):
            return obj.Proto().SerializeToString()
        else:
            raise ValueError("Unexpected argument to StringifyProto of type " +
                             type(obj).__name__)

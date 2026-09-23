def to(g, self, *args):
    # ONNX doesn't have a concept of a device, so we ignore device casts
    if len(args) == 4:
        if args[0].node().kind() == "prim::device" or args[0].type().isSubtypeOf(ListType.ofInts()):
            # aten::to(Tensor, Device, bool, bool, memory_format)
            return self
        else:
            # TestONNXRuntime::test_ones_bool shows args[0] of aten::to() can be onnx::Constant[value=<Tensor>]()
            # In this case, the constant value is a tensor not int,
            # so sym_help._maybe_get_const(args[0], 'i') would not work.
            dtype = args[0]
            if sym_help._is_value(args[0]) and args[0].node().kind() == "onnx::Constant":
                tval = args[0].node()["value"]
                if isinstance(tval, torch.Tensor):
                    if len(tval.shape) == 0:
                        tval = tval.item()
                        dtype = int(tval)
                    else:
                        dtype = tval

            if sym_help._is_value(dtype) or isinstance(dtype, torch.Tensor):
                # aten::to(Tensor, Tensor, bool, bool, memory_format)
                dtype = args[0].type().scalarType()
                return g.op("Cast", self, to_i=sym_help.cast_pytorch_to_onnx[dtype])
            else:
                # aten::to(Tensor, ScalarType, bool, bool, memory_format)
                # memory_format is ignored
                return g.op("Cast", self, to_i=sym_help.scalar_type_to_onnx[dtype])
    elif len(args) == 5:
        # aten::to(Tensor, Device, ScalarType, bool, bool, memory_format)
        dtype = sym_help._get_const(args[1], "i", "dtype")
        # memory_format is ignored
        return g.op("Cast", self, to_i=sym_help.scalar_type_to_onnx[dtype])
    elif len(args) == 6:
        # aten::to(Tensor, ScalarType, Layout, Device, bool, bool, memory_format) -> Tensor
        dtype = sym_help._get_const(args[0], "i", "dtype")
        # Layout, device and memory_format are ignored
        return g.op("Cast", self, to_i=sym_help.scalar_type_to_onnx[dtype])
    elif len(args) == 7:
        # aten::to(Tensor, ScalarType, Layout, Device, bool, bool, bool, memory_format) -> Tensor
        dtype = sym_help._get_const(args[0], "i", "dtype")
        # Layout, device and memory_format are ignored
        return g.op("Cast", self, to_i=sym_help.scalar_type_to_onnx[dtype])
    else:
        raise NotImplementedError("Unknown aten::to signature")

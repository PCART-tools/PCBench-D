def index_put(g, self, indices_list_value, values, accumulate=False):
    if sym_help._is_packed_list(indices_list_value):
        indices_list = sym_help._unpack_list(indices_list_value)
    else:
        indices_list = [indices_list_value]
    if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK:
        args = [self] + indices_list + [values, accumulate]
        return g.op("ATen", *args, operator_s="index_put")

    from torch.onnx.symbolic_opset9 import add, expand
    accumulate = sym_help._parse_arg(accumulate, "b")

    if len(indices_list) == 0:
        return values

    if len(indices_list) > 1:
        for idx_ in range(len(indices_list)):
            if indices_list[idx_].type().scalarType() == 'Bool':
                indices_list[idx_] = g.op("NonZero", indices_list[idx_])
        index = indices_list[0]

        for ind in indices_list[1:]:
            index = add(g, index, ind)
        broadcast_index_shape = g.op("Shape", index)
        indices_list = [
            sym_help._unsqueeze_helper(g, expand(g, ind, broadcast_index_shape, None), [-1]) for ind in indices_list
        ]
        index = g.op("Concat", *indices_list, axis_i=-1)
    else:
        # Replace index_put node with masked_scatter or masked_fill
        # when inputs to the index_put node contains a single boolean input.
        #
        # index_put -> masked_fill
        #   * input index contains single tensor of Bool type (e.g.: %24 <- %23).
        #   * input value contains single element (e.g.: %18).
        #
        # Torch IR
        #   %mask : Float(2, 2, 2, strides=[4, 2, 1], requires_grad=0, device=cpu) = aten::clone(%0, %6)
        #   %16 : Bool(2, 2, 2, strides=[4, 2, 1], requires_grad=0, device=cpu) =
        #               aten::to(%8, %26, %27, %11, %12, %28, %29, %15)
        #   %18 : Float(requires_grad=0, device=cpu) = prim::Constant[value={1}]()
        #   %23 : Bool(8, strides=[1], device=cpu) = aten::view(%16, %22)
        #   %24 : Tensor?[] = prim::ListConstruct(%23)
        #   %25 : Float(2, 2, 2, strides=[4, 2, 1], requires_grad=0, device=cpu) =
        #                aten::index_put(%mask, %24, %18, %30)
        #   return (%25)
        #
        #
        # index_put -> masked_scatter
        #   * input index contains single tensor of Bool type (e.g.: %32 <- %31).
        #   * input value contains multiple elements (e.g.: %28).
        #
        # Torch IR
        #   %mask : Float(2, 2, 2, strides=[4, 2, 1], requires_grad=0, device=cpu) = aten::clone(%0, %6)
        #   %28 : Float(8, strides=[1], requires_grad=0, device=cpu)
        #                = prim::Constant[value= 1  1  1  1  1  1  1  1 [ CPUFloatType{8} ]]()
        #   %15 : Bool(2, 2, 2, strides=[4, 2, 1], requires_grad=0, device=cpu)
        #                = aten::ne(%mask, %some_const)
        #   %23 : Bool(2, 2, 2, strides=[4, 2, 1], requires_grad=0, device=cpu)
        #                = aten::to(%15, %34, %35, %18, %19, %36, %37, %22)
        #   %38 : Long(requires_grad=0, device=cpu) = prim::Constant[value={0}]()
        #   %30 : int[] = prim::Constant[value=[-1]]()
        #   %31 : Bool(8, strides=[1], device=cpu) = aten::view(%23, %30)
        #   %32 : Tensor?[] = prim::ListConstruct(%31)
        #   %33 : Float(2, 2, 2, strides=[4, 2, 1], requires_grad=0, device=cpu)
        #               = aten::index_put(%mask, %32, %28, %38)
        #   return (%33)
        index = indices_list[0]
        bool_inp = index
        if bool_inp.type() is not None and bool_inp.type().scalarType() == "Bool":
            rank = sym_help._get_tensor_rank(values)
            if rank is not None and rank == 0:
                from torch.onnx.symbolic_opset9 import masked_fill
                return masked_fill(g, self, bool_inp, values)
            return masked_scatter(g, self, bool_inp, values)
        broadcast_index_shape = g.op("Shape", index)
        index = sym_help._unsqueeze_helper(g, index, [-1])
    sub_data_shape = sym_help._slice_helper(
        g, g.op("Shape", self), axes=[0], starts=[len(indices_list)], ends=[maxsize])
    values_shape = g.op("Concat", broadcast_index_shape, sub_data_shape, axis_i=0)
    # Check if values is a singular value and expand accordingly
    rank = sym_help._get_tensor_rank(values)
    if rank is not None and rank == 0:
        values = expand(g, values, values_shape, None)
    values = sym_help._reshape_helper(g, values, values_shape)

    dtype = self.type().scalarType()
    if dtype is not None and dtype != values.type().scalarType():
        values = g.op("Cast", values, to_i=sym_help.cast_pytorch_to_onnx[dtype])
    dtype = sym_help.scalar_type_to_onnx.index(sym_help.cast_pytorch_to_onnx[dtype])
    dtype = sym_help.scalar_type_to_pytorch_type[dtype]

    if accumulate:
        zeros = g.op("ConstantOfShape", g.op("Shape", self), value_t=torch.tensor([0], dtype=dtype))
        result = g.op("ScatterND", zeros, index, values)
        result = add(g, self, result)
    else:
        result = g.op("ScatterND", self, index, values)

    return result

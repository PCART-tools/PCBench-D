    @tensorrt_converter(trt_transposed_matmul)
    def trt_transposed_matmul_converter(network, target, args, kwargs, name):
        lhs, rhs, lhs_transposed, rhs_transposed = args

        layer = network.add_matrix_multiply(
            lhs,
            trt.MatrixOperation.TRANSPOSE if lhs_transposed else trt.MatrixOperation.NONE,
            rhs,
            trt.MatrixOperation.TRANSPOSE if rhs_transposed else trt.MatrixOperation.NONE,
        )
        set_layer_name(layer, target, name)
        return layer.get_output(0)

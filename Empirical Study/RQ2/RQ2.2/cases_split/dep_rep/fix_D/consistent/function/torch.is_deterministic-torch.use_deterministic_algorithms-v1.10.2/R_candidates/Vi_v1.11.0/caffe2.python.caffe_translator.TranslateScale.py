@TranslatorRegistry.Register("Scale")
def TranslateScale(layer, pretrained_blobs, is_test, **kwargs):
    mul_op = BaseTranslate(layer, "Mul")
    scale_param = layer.scale_param
    AddArgument(mul_op, "axis", scale_param.axis)
    AddArgument(mul_op, "broadcast", True)
    if len(mul_op.input) == 1:
        # the scale parameter is in pretrained blobs
        if scale_param.num_axes != 1:
            raise RuntimeError("This path has not been verified yet.")

        output = mul_op.output[0]
        mul_op_param = output + 'scale_w'
        mul_op.input.append(mul_op_param)
        weights = []
        weights.append(utils.NumpyArrayToCaffe2Tensor(
            pretrained_blobs[0].flatten(), mul_op_param))

        add_op = None
        if len(pretrained_blobs) == 1:
            # No bias-term in Scale layer
            pass
        elif len(pretrained_blobs) == 2:
            # Caffe Scale layer supports a bias term such that it computes
            # (scale_param * X + bias), whereas Caffe2 Mul op doesn't.
            # Include a separate Add op for the bias followed by Mul.
            add_op = copy.deepcopy(mul_op)
            add_op.type = "Add"
            add_op_param = output + 'scale_b'
            internal_blob = output + "_internal"
            del mul_op.output[:]
            mul_op.output.append(internal_blob)
            del add_op.input[:]
            add_op.input.append(internal_blob)
            add_op.input.append(add_op_param)
            weights.append(utils.NumpyArrayToCaffe2Tensor(
                pretrained_blobs[1].flatten(), add_op_param))
        else:
            raise RuntimeError("Unexpected number of pretrained blobs in Scale")

        caffe_ops = [mul_op]
        if add_op:
            caffe_ops.append(add_op)
        assert len(caffe_ops) == len(weights)
        return caffe_ops, weights
    elif len(mul_op.input) == 2:
        # TODO(jiayq): find a protobuf that uses this and verify.
        raise RuntimeError("This path has not been verified yet.")
    else:
        raise RuntimeError("Unexpected number of inputs.")

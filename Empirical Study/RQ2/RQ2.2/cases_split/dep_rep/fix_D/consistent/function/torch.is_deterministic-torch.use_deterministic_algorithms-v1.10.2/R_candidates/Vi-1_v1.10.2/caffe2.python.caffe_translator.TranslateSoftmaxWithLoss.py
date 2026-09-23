@TranslatorRegistry.Register("SoftmaxWithLoss")
def TranslateSoftmaxWithLoss(layer, pretrained_blobs, is_test, **kwargs):
    softmax_op = core.CreateOperator(
        "Softmax", [layer.bottom[0]],
        layer.bottom[0] + "_translator_autogen_softmax")
    xent_op = core.CreateOperator(
        "LabelCrossEntropy",
        [softmax_op.output[0], layer.bottom[1]],
        layer.bottom[0] + "_translator_autogen_xent")
    loss_op = core.CreateOperator(
        "AveragedLoss",
        xent_op.output[0],
        layer.top[0])
    return [softmax_op, xent_op, loss_op], []

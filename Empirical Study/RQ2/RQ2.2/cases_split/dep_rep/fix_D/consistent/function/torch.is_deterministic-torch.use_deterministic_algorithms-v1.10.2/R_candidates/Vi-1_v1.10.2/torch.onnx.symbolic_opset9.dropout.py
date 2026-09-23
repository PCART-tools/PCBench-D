@parse_args("v", "f", "i")
def dropout(g, input, p, train):
    sym_help.check_training_mode(train, "dropout")
    # in eval mode, dropout is non-op - if the node's train param is set to False, dropout is non-op
    if not train:
        return input
    warnings.warn("Dropout is a training op and should not be exported in inference mode. "
                  "For inference, make sure to call eval() on the model and to export it with param training=False.")
    r, _ = g.op("Dropout", input, ratio_f=p, outputs=2)
    return r

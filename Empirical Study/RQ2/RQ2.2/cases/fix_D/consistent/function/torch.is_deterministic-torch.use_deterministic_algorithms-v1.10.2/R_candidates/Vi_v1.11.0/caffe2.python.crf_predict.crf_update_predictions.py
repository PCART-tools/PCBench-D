def crf_update_predictions(model, crf_with_loss, classes):
    return apply_crf(
        model.param_init_net,
        model.net,
        crf_with_loss.transitions,
        classes,
        crf_with_loss.num_classes,
    )

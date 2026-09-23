def _maybe_cuda(model, move_to_cuda):
    return model.cuda() if move_to_cuda else model

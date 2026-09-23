def build_fp16_sgd(model, base_learning_rate, **kwargs):
    fp16_sgd_optimizer = FP16SgdOptimizer(base_learning_rate, **kwargs)
    return _build(model, fp16_sgd_optimizer)

def build_yellowfin(model, base_learning_rate=0.1, **kwargs):
    yellowfin_optimizer = YellowFinOptimizer(alpha=base_learning_rate, **kwargs)
    return _build(model, yellowfin_optimizer)

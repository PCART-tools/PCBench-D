def get_default_qat_qconfig(backend='fbgemm', version=1):
    """
    Returns the default QAT qconfig for the specified backend.

    Args:
      * `backend`: a string representing the target backend. Currently supports `fbgemm`
        and `qnnpack`.
      * `version`: version, for backwards compatibility. Can be `None` or `1`.

    Return:
        qconfig
    """
    # Histogram observer is too slow for quantization aware training
    if version is None:
        if backend == 'fbgemm':
            qconfig = QConfig(activation=FakeQuantize.with_args(observer=MovingAverageMinMaxObserver,
                                                                quant_min=0,
                                                                quant_max=255,
                                                                reduce_range=True),
                              weight=default_per_channel_weight_fake_quant)
        elif backend == 'qnnpack':
            qconfig = QConfig(activation=FakeQuantize.with_args(observer=MovingAverageMinMaxObserver,
                                                                quant_min=0,
                                                                quant_max=255,
                                                                reduce_range=False),
                              weight=default_weight_fake_quant)
        else:
            qconfig = default_qat_qconfig
    # Use the fused observer + fake_quant modules for doing QAT.
    if version == 1:
        if backend == 'fbgemm':
            qconfig = QConfig(activation=FusedMovingAvgObsFakeQuantize.with_args(observer=MovingAverageMinMaxObserver,
                                                                                 quant_min=0,
                                                                                 quant_max=255,
                                                                                 reduce_range=True),
                              weight=default_fused_per_channel_wt_fake_quant)
        elif backend == 'qnnpack':
            qconfig = QConfig(activation=FusedMovingAvgObsFakeQuantize.with_args(observer=MovingAverageMinMaxObserver,
                                                                                 quant_min=0,
                                                                                 quant_max=255,
                                                                                 reduce_range=False),
                              weight=default_fused_wt_fake_quant)
        else:
            qconfig = default_qat_qconfig_v2
    return qconfig

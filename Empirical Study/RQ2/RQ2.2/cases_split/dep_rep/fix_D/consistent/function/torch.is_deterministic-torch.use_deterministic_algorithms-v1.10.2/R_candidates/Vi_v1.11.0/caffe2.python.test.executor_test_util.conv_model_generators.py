def conv_model_generators():
    return {
        'AlexNet': cb.AlexNet,
        'OverFeat': cb.OverFeat,
        'VGGA': cb.VGGA,
        'Inception': cb.Inception,
        'MLP': cb.MLP,
        'Resnet50': gen_test_resnet50,
    }

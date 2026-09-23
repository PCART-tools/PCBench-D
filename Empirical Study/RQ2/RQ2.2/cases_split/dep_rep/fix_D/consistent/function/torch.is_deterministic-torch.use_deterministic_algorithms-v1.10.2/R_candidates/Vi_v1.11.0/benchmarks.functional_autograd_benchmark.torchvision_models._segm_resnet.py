def _segm_resnet(name, backbone_name, num_classes, aux, pretrained_backbone=True):
    # backbone = resnet.__dict__[backbone_name](
    #     pretrained=pretrained_backbone,
    #     replace_stride_with_dilation=[False, True, True])
    # Hardcoded resnet 50
    assert backbone_name == "resnet50"
    backbone = resnet50(
        pretrained=pretrained_backbone,
        replace_stride_with_dilation=[False, True, True])

    return_layers = {'layer4': 'out'}
    if aux:
        return_layers['layer3'] = 'aux'
    backbone = IntermediateLayerGetter(backbone, return_layers=return_layers)

    aux_classifier = None
    if aux:
        inplanes = 1024
        aux_classifier = FCNHead(inplanes, num_classes)

    model_map = {
        # 'deeplabv3': (DeepLabHead, DeepLabV3), # Not used
        'fcn': (FCNHead, FCN),
    }
    inplanes = 2048
    classifier = model_map[name][0](inplanes, num_classes)
    base_model = model_map[name][1]

    model = base_model(backbone, classifier, aux_classifier)
    return model

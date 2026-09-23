def _load_model(arch_type, backbone, pretrained, progress, num_classes, aux_loss, **kwargs):
    if pretrained:
        aux_loss = True
    model = _segm_resnet(arch_type, backbone, num_classes, aux_loss, **kwargs)
    # if pretrained:
    #     arch = arch_type + '_' + backbone + '_coco'
    #     model_url = model_urls[arch]
    #     if model_url is None:
    #         raise NotImplementedError('pretrained {} is not supported as of now'.format(arch))
    #     else:
    #         state_dict = load_state_dict_from_url(model_url, progress=progress)
    #         model.load_state_dict(state_dict)
    return model

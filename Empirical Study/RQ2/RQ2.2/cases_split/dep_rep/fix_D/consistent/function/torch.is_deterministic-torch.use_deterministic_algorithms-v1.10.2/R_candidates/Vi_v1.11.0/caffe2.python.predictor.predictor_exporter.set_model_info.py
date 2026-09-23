def set_model_info(meta_net_def, project_str, model_class_str, version):
    assert isinstance(meta_net_def, metanet_pb2.MetaNetDef)
    meta_net_def.modelInfo.project = project_str
    meta_net_def.modelInfo.modelClass = model_class_str
    meta_net_def.modelInfo.version = version

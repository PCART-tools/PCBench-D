def text(tag, text):
    plugin_data = SummaryMetadata.PluginData(
        plugin_name='text', content=TextPluginData(version=0).SerializeToString())
    smd = SummaryMetadata(plugin_data=plugin_data)
    tensor = TensorProto(dtype='DT_STRING',
                         string_val=[text.encode(encoding='utf_8')],
                         tensor_shape=TensorShapeProto(dim=[TensorShapeProto.Dim(size=1)]))
    return Summary(value=[Summary.Value(tag=tag + '/text_summary', metadata=smd, tensor=tensor)])

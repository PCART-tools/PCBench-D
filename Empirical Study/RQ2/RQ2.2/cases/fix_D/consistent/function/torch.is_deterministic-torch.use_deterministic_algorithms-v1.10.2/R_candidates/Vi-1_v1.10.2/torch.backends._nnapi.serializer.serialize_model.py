def serialize_model(module, inputs, config=None):
    return _NnapiSerializer(config).serialize_model(module, inputs)

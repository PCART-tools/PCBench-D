def dataclass_fields(cls):
    return torch._dynamo.disable(dataclasses.fields)(cls)

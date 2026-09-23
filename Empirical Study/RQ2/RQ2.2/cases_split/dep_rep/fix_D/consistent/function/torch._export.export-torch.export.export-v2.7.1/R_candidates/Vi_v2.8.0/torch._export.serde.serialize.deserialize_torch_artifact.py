def deserialize_torch_artifact(
    serialized: Union[dict[str, Any], tuple[Any, ...], bytes]
):
    if isinstance(serialized, (dict, tuple)):
        return serialized
    if len(serialized) == 0:
        return {}
    buffer = io.BytesIO(serialized)
    buffer.seek(0)
    # weights_only=False as we want to load custom objects here (e.g. ScriptObject)
    artifact = torch.load(buffer, weights_only=False)
    assert isinstance(artifact, (tuple, dict))
    return artifact

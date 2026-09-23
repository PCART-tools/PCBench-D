def get_output_model_version(script_module: torch.nn.Module) -> int:
    buffer = io.BytesIO()
    torch.jit.save(script_module, buffer)
    buffer.seek(0)
    zipped_model = zipfile.ZipFile(buffer)
    try:
        version = int(zipped_model.read('archive/version').decode("utf-8"))
        return version
    except KeyError:
        version = int(zipped_model.read('archive/.data/version').decode("utf-8"))
        return version

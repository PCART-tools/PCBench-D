@deprecated(
    "Falling back to the old format < 1.6. This support will be "
    "deprecated in favor of default zipfile format introduced in 1.6. "
    "Please redo torch.save() to save it in the new zipfile format.",
    category=FutureWarning,
)
def _legacy_zip_load(
    filename: str,
    model_dir: str,
    map_location: MAP_LOCATION,
    weights_only: bool,
) -> dict[str, Any]:
    # Note: extractall() defaults to overwrite file if exists. No need to clean up beforehand.
    #       We deliberately don't handle tarfile here since our legacy serialization format was in tar.
    #       E.g. resnet18-5c106cde.pth which is widely used.
    with zipfile.ZipFile(filename) as f:
        members = f.infolist()
        if len(members) != 1:
            raise RuntimeError("Only one file(not dir) is allowed in the zipfile")
        f.extractall(model_dir)
        extraced_name = members[0].filename
        extracted_file = os.path.join(model_dir, extraced_name)
    return torch.load(
        extracted_file, map_location=map_location, weights_only=weights_only
    )

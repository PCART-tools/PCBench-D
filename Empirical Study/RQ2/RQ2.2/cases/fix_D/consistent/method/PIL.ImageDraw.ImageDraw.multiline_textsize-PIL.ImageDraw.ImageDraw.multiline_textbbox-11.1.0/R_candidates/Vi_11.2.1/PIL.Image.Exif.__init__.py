    def __init__(self) -> None:
        self._data: dict[int, Any] = {}
        self._hidden_data: dict[int, Any] = {}
        self._ifds: dict[int, dict[int, Any]] = {}
        self._info: TiffImagePlugin.ImageFileDirectory_v2 | None = None
        self._loaded_exif: bytes | None = None

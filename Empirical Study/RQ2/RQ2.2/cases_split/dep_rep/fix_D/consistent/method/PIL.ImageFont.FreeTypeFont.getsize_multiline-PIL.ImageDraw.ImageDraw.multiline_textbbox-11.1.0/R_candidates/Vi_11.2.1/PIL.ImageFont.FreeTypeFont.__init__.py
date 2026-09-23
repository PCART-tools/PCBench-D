    def __init__(
        self,
        font: StrOrBytesPath | BinaryIO,
        size: float = 10,
        index: int = 0,
        encoding: str = "",
        layout_engine: Layout | None = None,
    ) -> None:
        # FIXME: use service provider instead

        if isinstance(core, DeferredError):
            raise core.ex

        if size <= 0:
            msg = f"font size must be greater than 0, not {size}"
            raise ValueError(msg)

        self.path = font
        self.size = size
        self.index = index
        self.encoding = encoding

        try:
            from packaging.version import parse as parse_version
        except ImportError:
            pass
        else:
            if freetype_version := features.version_module("freetype2"):
                if parse_version(freetype_version) < parse_version("2.9.1"):
                    warnings.warn(
                        "Support for FreeType 2.9.0 is deprecated and will be removed "
                        "in Pillow 12 (2025-10-15). Please upgrade to FreeType 2.9.1 "
                        "or newer, preferably FreeType 2.10.4 which fixes "
                        "CVE-2020-15999.",
                        DeprecationWarning,
                    )

        if layout_engine not in (Layout.BASIC, Layout.RAQM):
            layout_engine = Layout.BASIC
            if core.HAVE_RAQM:
                layout_engine = Layout.RAQM
        elif layout_engine == Layout.RAQM and not core.HAVE_RAQM:
            warnings.warn(
                "Raqm layout was requested, but Raqm is not available. "
                "Falling back to basic layout."
            )
            layout_engine = Layout.BASIC

        self.layout_engine = layout_engine

        def load_from_bytes(f: IO[bytes]) -> None:
            self.font_bytes = f.read()
            self.font = core.getfont(
                "", size, index, encoding, self.font_bytes, layout_engine
            )

        if is_path(font):
            font = os.fspath(font)
            if sys.platform == "win32":
                font_bytes_path = font if isinstance(font, bytes) else font.encode()
                try:
                    font_bytes_path.decode("ascii")
                except UnicodeDecodeError:
                    # FreeType cannot load fonts with non-ASCII characters on Windows
                    # So load it into memory first
                    with open(font, "rb") as f:
                        load_from_bytes(f)
                    return
            self.font = core.getfont(
                font, size, index, encoding, layout_engine=layout_engine
            )
        else:
            load_from_bytes(cast(IO[bytes], font))

    def _get_image_filename(self, tool):
        """Resolve a tool icon's filename."""
        if not tool.image:
            return None
        if os.path.isabs(tool.image):
            filename = tool.image
        else:
            if "image" in getattr(tool, "__dict__", {}):
                raise ValueError("If 'tool.image' is an instance variable, "
                                 "it must be an absolute path")
            for cls in type(tool).__mro__:
                if "image" in vars(cls):
                    try:
                        src = inspect.getfile(cls)
                        break
                    except (OSError, TypeError):
                        raise ValueError("Failed to locate source file "
                                         "where 'tool.image' is defined") from None
            else:
                raise ValueError("Failed to find parent class defining 'tool.image'")
            filename = str(pathlib.Path(src).parent / tool.image)
        for filename in [filename, filename + self._icon_extension]:
            if os.path.isfile(filename):
                return os.path.abspath(filename)
        for fname in [  # Fallback; once deprecation elapses.
            tool.image,
            tool.image + self._icon_extension,
            cbook._get_data_path("images", tool.image),
            cbook._get_data_path("images", tool.image + self._icon_extension),
        ]:
            if os.path.isfile(fname):
                _api.warn_deprecated(
                    "3.9", message=f"Loading icon {tool.image!r} from the current "
                    "directory or from Matplotlib's image directory.  This behavior "
                    "is deprecated since %(since)s and will be removed in %(removal)s; "
                    "Tool.image should be set to a path relative to the Tool's source "
                    "file, or to an absolute path.")
                return os.path.abspath(fname)

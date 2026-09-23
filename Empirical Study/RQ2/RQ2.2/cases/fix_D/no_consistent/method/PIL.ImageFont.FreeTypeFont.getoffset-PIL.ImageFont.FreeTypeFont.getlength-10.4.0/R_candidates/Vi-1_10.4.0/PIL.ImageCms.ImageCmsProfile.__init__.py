    def __init__(self, profile: str | SupportsRead[bytes] | core.CmsProfile) -> None:
        """
        :param profile: Either a string representing a filename,
            a file like object containing a profile or a
            low-level profile object

        """

        if isinstance(profile, str):
            if sys.platform == "win32":
                profile_bytes_path = profile.encode()
                try:
                    profile_bytes_path.decode("ascii")
                except UnicodeDecodeError:
                    with open(profile, "rb") as f:
                        self._set(core.profile_frombytes(f.read()))
                    return
            self._set(core.profile_open(profile), profile)
        elif hasattr(profile, "read"):
            self._set(core.profile_frombytes(profile.read()))
        elif isinstance(profile, core.CmsProfile):
            self._set(profile)
        else:
            msg = "Invalid type for Profile"  # type: ignore[unreachable]
            raise TypeError(msg)

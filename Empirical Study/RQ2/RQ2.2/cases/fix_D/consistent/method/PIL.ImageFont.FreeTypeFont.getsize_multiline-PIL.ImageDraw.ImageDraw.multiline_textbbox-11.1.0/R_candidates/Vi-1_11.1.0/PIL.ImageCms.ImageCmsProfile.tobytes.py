    def tobytes(self) -> bytes:
        """
        Returns the profile in a format suitable for embedding in
        saved images.

        :returns: a bytes object containing the ICC profile.
        """

        return core.profile_tobytes(self.profile)

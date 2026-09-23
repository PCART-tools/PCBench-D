    def transformed(self, transform: Affine2D):
        """
        Return a new version of this marker with the transform applied.

        Parameters
        ----------
        transform : Affine2D, default: None
            Transform will be combined with current user supplied transform.
        """
        new_marker = MarkerStyle(self)
        if new_marker._user_transform is not None:
            new_marker._user_transform += transform
        else:
            new_marker._user_transform = transform
        return new_marker

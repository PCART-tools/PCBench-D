    def set_clip_path(self, path, transform=None):
        """
        Set the artist's clip path, which may be:

          * a `~matplotlib.patches.Patch` (or subclass) instance

          * a `~matplotlib.path.Path` instance, in which case
             an optional `~matplotlib.transforms.Transform`
             instance may be provided, which will be applied to the
             path before using it for clipping.

          * *None*, to remove the clipping path

        For efficiency, if the path happens to be an axis-aligned
        rectangle, this method will set the clipping box to the
        corresponding rectangle and set the clipping path to *None*.

        ACCEPTS: { (`.path.Path`, `.transforms.Transform`),
                  `.patches.Patch`, None }
        """
        super().set_clip_path(path, transform)
        self._update_clip_properties()

    def stop_rasterizing(self):
        """
        Used in MixedModeRenderer. Switch back to the vector renderer
        and draw the contents of the raster renderer as an image on
        the vector renderer.
        """

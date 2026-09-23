    def close(self):
        """
        (Consumer) Close the stream.

        :returns: An image object.
        :exception OSError: If the parser failed to parse the image file either
                            because it cannot be identified or cannot be
                            decoded.
        """
        # finish decoding
        if self.decoder:
            # get rid of what's left in the buffers
            self.feed(b"")
            self.data = self.decoder = None
            if not self.finished:
                msg = "image was incomplete"
                raise OSError(msg)
        if not self.image:
            msg = "cannot parse this image"
            raise OSError(msg)
        if self.data:
            # incremental parsing not possible; reopen the file
            # not that we have all data
            with io.BytesIO(self.data) as fp:
                try:
                    self.image = Image.open(fp)
                finally:
                    self.image.load()
        return self.image

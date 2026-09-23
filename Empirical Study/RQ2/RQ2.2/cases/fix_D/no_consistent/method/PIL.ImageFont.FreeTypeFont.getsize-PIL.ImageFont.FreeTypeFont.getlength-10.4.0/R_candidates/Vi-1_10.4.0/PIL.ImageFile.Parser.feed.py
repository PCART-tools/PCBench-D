    def feed(self, data):
        """
        (Consumer) Feed data to the parser.

        :param data: A string buffer.
        :exception OSError: If the parser failed to parse the image file.
        """
        # collect data

        if self.finished:
            return

        if self.data is None:
            self.data = data
        else:
            self.data = self.data + data

        # parse what we have
        if self.decoder:
            if self.offset > 0:
                # skip header
                skip = min(len(self.data), self.offset)
                self.data = self.data[skip:]
                self.offset = self.offset - skip
                if self.offset > 0 or not self.data:
                    return

            n, e = self.decoder.decode(self.data)

            if n < 0:
                # end of stream
                self.data = None
                self.finished = 1
                if e < 0:
                    # decoding error
                    self.image = None
                    raise _get_oserror(e, encoder=False)
                else:
                    # end of image
                    return
            self.data = self.data[n:]

        elif self.image:
            # if we end up here with no decoder, this file cannot
            # be incrementally parsed.  wait until we've gotten all
            # available data
            pass

        else:
            # attempt to open this file
            try:
                with io.BytesIO(self.data) as fp:
                    im = Image.open(fp)
            except OSError:
                pass  # not enough data
            else:
                flag = hasattr(im, "load_seek") or hasattr(im, "load_read")
                if flag or len(im.tile) != 1:
                    # custom load code, or multiple tiles
                    self.decode = None
                else:
                    # initialize decoder
                    im.load_prepare()
                    d, e, o, a = im.tile[0]
                    im.tile = []
                    self.decoder = Image._getdecoder(im.mode, d, a, im.decoderconfig)
                    self.decoder.setimage(im.im, e)

                    # calculate decoder offset
                    self.offset = o
                    if self.offset <= len(self.data):
                        self.data = self.data[self.offset :]
                        self.offset = 0

                self.image = im

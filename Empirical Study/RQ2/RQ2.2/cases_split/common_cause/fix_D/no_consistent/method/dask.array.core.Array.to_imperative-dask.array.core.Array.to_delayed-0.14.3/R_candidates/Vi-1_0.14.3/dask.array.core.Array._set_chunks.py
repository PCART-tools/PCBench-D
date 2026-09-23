    def _set_chunks(self, chunks):
        raise TypeError("Can not set chunks directly\n\n"
                        "Please use the rechunk method instead:\n"
                        "  x.rechunk(%s)" % str(chunks))

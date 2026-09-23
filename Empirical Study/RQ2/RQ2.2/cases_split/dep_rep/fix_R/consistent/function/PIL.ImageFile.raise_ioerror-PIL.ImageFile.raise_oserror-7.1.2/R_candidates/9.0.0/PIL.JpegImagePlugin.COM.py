def COM(self, marker):
    #
    # Comment marker.  Store these in the APP dictionary.
    n = i16(self.fp.read(2)) - 2
    s = ImageFile._safe_read(self.fp, n)

    self.info["comment"] = s
    self.app["COM"] = s  # compatibility
    self.applist.append(("COM", s))

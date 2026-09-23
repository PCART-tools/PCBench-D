    def __init__(self, filename):
        _log.debug('opening tfm file %s', filename)
        with open(filename, 'rb') as file:
            header1 = file.read(24)
            lh, bc, ec, nw, nh, nd = \
                struct.unpack('!6H', header1[2:14])
            _log.debug('lh=%d, bc=%d, ec=%d, nw=%d, nh=%d, nd=%d',
                       lh, bc, ec, nw, nh, nd)
            header2 = file.read(4*lh)
            self.checksum, self.design_size = \
                struct.unpack('!2I', header2[:8])
            # there is also encoding information etc.
            char_info = file.read(4*(ec-bc+1))
            widths = file.read(4*nw)
            heights = file.read(4*nh)
            depths = file.read(4*nd)

        self.width, self.height, self.depth = {}, {}, {}
        widths, heights, depths = \
            [struct.unpack('!%dI' % (len(x)/4), x)
             for x in (widths, heights, depths)]
        for idx, char in enumerate(range(bc, ec+1)):
            byte0 = char_info[4*idx]
            byte1 = char_info[4*idx+1]
            self.width[char] = _fix2comp(widths[byte0])
            self.height[char] = _fix2comp(heights[byte1 >> 4])
            self.depth[char] = _fix2comp(depths[byte1 & 0xf])

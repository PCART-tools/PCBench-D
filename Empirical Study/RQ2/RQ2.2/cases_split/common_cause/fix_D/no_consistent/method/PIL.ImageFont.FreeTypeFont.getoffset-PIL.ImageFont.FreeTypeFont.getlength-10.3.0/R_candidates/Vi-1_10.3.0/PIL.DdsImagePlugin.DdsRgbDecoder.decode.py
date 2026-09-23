    def decode(self, buffer):
        bitcount, masks = self.args

        # Some masks will be padded with zeros, e.g. R 0b11 G 0b1100
        # Calculate how many zeros each mask is padded with
        mask_offsets = []
        # And the maximum value of each channel without the padding
        mask_totals = []
        for mask in masks:
            offset = 0
            if mask != 0:
                while mask >> (offset + 1) << (offset + 1) == mask:
                    offset += 1
            mask_offsets.append(offset)
            mask_totals.append(mask >> offset)

        data = bytearray()
        bytecount = bitcount // 8
        dest_length = self.state.xsize * self.state.ysize * len(masks)
        while len(data) < dest_length:
            value = int.from_bytes(self.fd.read(bytecount), "little")
            for i, mask in enumerate(masks):
                masked_value = value & mask
                # Remove the zero padding, and scale it to 8 bits
                data += o8(
                    int(((masked_value >> mask_offsets[i]) / mask_totals[i]) * 255)
                )
        self.set_as_raw(data)
        return -1, 0

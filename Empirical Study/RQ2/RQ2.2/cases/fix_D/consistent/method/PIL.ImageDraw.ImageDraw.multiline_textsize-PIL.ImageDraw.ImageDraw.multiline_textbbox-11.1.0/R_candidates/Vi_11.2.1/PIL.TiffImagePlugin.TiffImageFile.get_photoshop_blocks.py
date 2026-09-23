    def get_photoshop_blocks(self) -> dict[int, dict[str, bytes]]:
        """
        Returns a dictionary of Photoshop "Image Resource Blocks".
        The keys are the image resource ID. For more information, see
        https://www.adobe.com/devnet-apps/photoshop/fileformatashtml/#50577409_pgfId-1037727

        :returns: Photoshop "Image Resource Blocks" in a dictionary.
        """
        blocks = {}
        val = self.tag_v2.get(ExifTags.Base.ImageResources)
        if val:
            while val.startswith(b"8BIM"):
                id = i16(val[4:6])
                n = math.ceil((val[6] + 1) / 2) * 2
                size = i32(val[6 + n : 10 + n])
                data = val[10 + n : 10 + n + size]
                blocks[id] = {"data": data}

                val = val[math.ceil((10 + n + size) / 2) * 2 :]
        return blocks

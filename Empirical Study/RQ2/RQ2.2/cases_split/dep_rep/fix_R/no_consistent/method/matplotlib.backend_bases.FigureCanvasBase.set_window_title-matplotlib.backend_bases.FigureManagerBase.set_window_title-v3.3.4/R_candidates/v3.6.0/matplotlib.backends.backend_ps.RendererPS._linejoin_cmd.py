    @staticmethod
    def _linejoin_cmd(linejoin):
        # Support for directly passing integer values is for backcompat.
        linejoin = {'miter': 0, 'round': 1, 'bevel': 2, 0: 0, 1: 1, 2: 2}[
            linejoin]
        return f"{linejoin:d} setlinejoin\n"

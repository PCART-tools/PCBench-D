    def __init__(self, size, table, channels=3, target_mode=None, **kwargs):
        if channels not in (3, 4):
            msg = "Only 3 or 4 output channels are supported"
            raise ValueError(msg)
        self.size = size = self._check_size(size)
        self.channels = channels
        self.mode = target_mode

        # Hidden flag `_copy_table=False` could be used to avoid extra copying
        # of the table if the table is specially made for the constructor.
        copy_table = kwargs.get("_copy_table", True)
        items = size[0] * size[1] * size[2]
        wrong_size = False

        numpy = None
        if hasattr(table, "shape"):
            try:
                import numpy
            except ImportError:  # pragma: no cover
                pass

        if numpy and isinstance(table, numpy.ndarray):
            if copy_table:
                table = table.copy()

            if table.shape in [
                (items * channels,),
                (items, channels),
                (size[2], size[1], size[0], channels),
            ]:
                table = table.reshape(items * channels)
            else:
                wrong_size = True

        else:
            if copy_table:
                table = list(table)

            # Convert to a flat list
            if table and isinstance(table[0], (list, tuple)):
                table, raw_table = [], table
                for pixel in raw_table:
                    if len(pixel) != channels:
                        msg = (
                            "The elements of the table should "
                            f"have a length of {channels}."
                        )
                        raise ValueError(msg)
                    table.extend(pixel)

        if wrong_size or len(table) != items * channels:
            msg = (
                "The table should have either channels * size**3 float items "
                "or size**3 items of channels-sized tuples with floats. "
                f"Table should be: {channels}x{size[0]}x{size[1]}x{size[2]}. "
                f"Actual length: {len(table)}"
            )
            raise ValueError(msg)
        self.table = table

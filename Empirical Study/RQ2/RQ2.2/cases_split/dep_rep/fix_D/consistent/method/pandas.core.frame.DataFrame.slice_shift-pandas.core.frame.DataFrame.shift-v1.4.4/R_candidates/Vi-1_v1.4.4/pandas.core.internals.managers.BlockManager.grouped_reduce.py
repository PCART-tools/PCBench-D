    def grouped_reduce(self: T, func: Callable, ignore_failures: bool = False) -> T:
        """
        Apply grouped reduction function blockwise, returning a new BlockManager.

        Parameters
        ----------
        func : grouped reduction function
        ignore_failures : bool, default False
            Whether to drop blocks where func raises TypeError.

        Returns
        -------
        BlockManager
        """
        result_blocks: list[Block] = []
        dropped_any = False

        for blk in self.blocks:
            if blk.is_object:
                # split on object-dtype blocks bc some columns may raise
                #  while others do not.
                for sb in blk._split():
                    try:
                        applied = sb.apply(func)
                    except (TypeError, NotImplementedError):
                        if not ignore_failures:
                            raise
                        dropped_any = True
                        continue
                    result_blocks = extend_blocks(applied, result_blocks)
            else:
                try:
                    applied = blk.apply(func)
                except (TypeError, NotImplementedError):
                    if not ignore_failures:
                        raise
                    dropped_any = True
                    continue
                result_blocks = extend_blocks(applied, result_blocks)

        if len(result_blocks) == 0:
            index = Index([None])  # placeholder
        else:
            index = Index(range(result_blocks[0].values.shape[-1]))

        if dropped_any:
            # faster to skip _combine if we haven't dropped any blocks
            return self._combine(result_blocks, copy=False, index=index)

        return type(self).from_blocks(result_blocks, [self.axes[0], index])

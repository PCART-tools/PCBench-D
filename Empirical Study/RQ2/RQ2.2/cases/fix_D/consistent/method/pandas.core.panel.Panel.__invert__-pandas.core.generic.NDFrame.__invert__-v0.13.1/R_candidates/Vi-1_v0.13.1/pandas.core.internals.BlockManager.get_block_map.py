    def get_block_map(self, copy=False, typ=None, columns=None,
                      is_numeric=False, is_bool=False):
        """ return a dictionary mapping the ftype -> block list

            Parameters
            ----------
            typ : return a list/dict
            copy : copy if indicated
            columns : a column filter list
            filter if the type is indicated """

        # short circuit - mainly for merging
        if (typ == 'dict' and columns is None and not is_numeric and
                not is_bool and not copy):
            bm = defaultdict(list)
            for b in self.blocks:
                bm[str(b.ftype)].append(b)
            return bm

        self._consolidate_inplace()

        if is_numeric:
            filter_blocks = lambda block: block.is_numeric
        elif is_bool:
            filter_blocks = lambda block: block.is_bool
        else:
            filter_blocks = lambda block: True

        def filter_columns(b):
            if columns:
                if not columns in b.items:
                    return None
                b = b.reindex_items_from(columns)
            return b

        maybe_copy = lambda b: b.copy() if copy else b

        def maybe_copy(b):
            if copy:
                b = b.copy()
            return b

        if typ == 'list':
            bm = []
            for b in self.blocks:
                if filter_blocks(b):
                    b = filter_columns(b)
                    if b is not None:
                        bm.append(maybe_copy(b))

        else:
            if typ == 'dtype':
                key = lambda b: b.dtype
            else:
                key = lambda b: b.ftype
            bm = defaultdict(list)
            for b in self.blocks:
                if filter_blocks(b):
                    b = filter_columns(b)
                    if b is not None:
                        bm[str(key(b))].append(maybe_copy(b))
        return bm

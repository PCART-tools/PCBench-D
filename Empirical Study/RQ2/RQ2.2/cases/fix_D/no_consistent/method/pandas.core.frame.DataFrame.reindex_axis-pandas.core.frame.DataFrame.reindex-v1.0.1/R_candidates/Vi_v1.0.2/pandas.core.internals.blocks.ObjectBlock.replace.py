    def replace(
        self, to_replace, value, inplace=False, filter=None, regex=False, convert=True
    ):
        to_rep_is_list = is_list_like(to_replace)
        value_is_list = is_list_like(value)
        both_lists = to_rep_is_list and value_is_list
        either_list = to_rep_is_list or value_is_list

        result_blocks = []
        blocks = [self]

        if not either_list and is_re(to_replace):
            return self._replace_single(
                to_replace,
                value,
                inplace=inplace,
                filter=filter,
                regex=True,
                convert=convert,
            )
        elif not (either_list or regex):
            return super().replace(
                to_replace,
                value,
                inplace=inplace,
                filter=filter,
                regex=regex,
                convert=convert,
            )
        elif both_lists:
            for to_rep, v in zip(to_replace, value):
                result_blocks = []
                for b in blocks:
                    result = b._replace_single(
                        to_rep,
                        v,
                        inplace=inplace,
                        filter=filter,
                        regex=regex,
                        convert=convert,
                    )
                    result_blocks = _extend_blocks(result, result_blocks)
                blocks = result_blocks
            return result_blocks

        elif to_rep_is_list and regex:
            for to_rep in to_replace:
                result_blocks = []
                for b in blocks:
                    result = b._replace_single(
                        to_rep,
                        value,
                        inplace=inplace,
                        filter=filter,
                        regex=regex,
                        convert=convert,
                    )
                    result_blocks = _extend_blocks(result, result_blocks)
                blocks = result_blocks
            return result_blocks

        return self._replace_single(
            to_replace,
            value,
            inplace=inplace,
            filter=filter,
            convert=convert,
            regex=regex,
        )

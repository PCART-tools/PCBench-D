    def replace(self, to_replace, value, inplace=False, filter=None,
                regex=False):
        blk = [self]
        to_rep_is_list = com.is_list_like(to_replace)
        value_is_list = com.is_list_like(value)
        both_lists = to_rep_is_list and value_is_list
        either_list = to_rep_is_list or value_is_list

        if not either_list and com.is_re(to_replace):
            blk[0], = blk[0]._replace_single(to_replace, value,
                                             inplace=inplace, filter=filter,
                                             regex=True)
        elif not (either_list or regex):
            blk = super(ObjectBlock, self).replace(to_replace, value,
                                                   inplace=inplace,
                                                   filter=filter, regex=regex)
        elif both_lists:
            for to_rep, v in zip(to_replace, value):
                blk[0], = blk[0]._replace_single(to_rep, v, inplace=inplace,
                                                 filter=filter, regex=regex)
        elif to_rep_is_list and regex:
            for to_rep in to_replace:
                blk[0], = blk[0]._replace_single(to_rep, value,
                                                 inplace=inplace,
                                                 filter=filter, regex=regex)
        else:
            blk[0], = blk[0]._replace_single(to_replace, value,
                                             inplace=inplace, filter=filter,
                                             regex=regex)
        return blk

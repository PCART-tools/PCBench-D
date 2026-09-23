def _pdmerge(left, right, how, left_on, right_on,
             left_index, right_index, indicator, suffixes,
             default_left, default_right):

    if not len(left):
        left = default_left

    if not len(right):
        right = default_right

    return pd.merge(left, right, how=how, left_on=left_on, right_on=right_on,
                    left_index=left_index, right_index=right_index,
                    suffixes=suffixes, indicator=indicator)

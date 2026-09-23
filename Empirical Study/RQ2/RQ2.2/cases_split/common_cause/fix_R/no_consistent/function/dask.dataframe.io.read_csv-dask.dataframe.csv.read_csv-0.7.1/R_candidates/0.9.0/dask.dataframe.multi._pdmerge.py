def _pdmerge(left, right, how, left_on, right_on,
             left_index, right_index, suffixes,
             default_left_columns, default_right_columns):

    if not len(left):
        left = pd.DataFrame(columns=default_left_columns)

    if not len(right):
        right = pd.DataFrame(columns=default_right_columns)

    result = pd.merge(left, right, how=how,
                      left_on=left_on, right_on=right_on,
                      left_index=left_index, right_index=right_index,
                      suffixes=suffixes)
    return result

def _cum_agg_aligned(part, cum_last, index, columns, func, initial):
    align = cum_last.reindex(part.set_index(index).index, fill_value=initial)
    align.index = part.index
    return func(part[columns], align)

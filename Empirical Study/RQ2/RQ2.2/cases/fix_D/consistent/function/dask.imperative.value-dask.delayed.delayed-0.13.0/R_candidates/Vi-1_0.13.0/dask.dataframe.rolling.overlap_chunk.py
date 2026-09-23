def overlap_chunk(func, prev_part, current_part, next_part, before, after,
                  args, kwargs):
    if ((prev_part is not None and prev_part.shape[0] != before) or
            (next_part is not None and next_part.shape[0] != after)):
        raise NotImplementedError("Partition size is less than overlapping "
                                  "window size. Try using ``df.repartition`` "
                                  "to increase the partition size.")
    parts = [p for p in (prev_part, current_part, next_part) if p is not None]
    combined = pd.concat(parts)
    out = func(combined, *args, **kwargs)
    if prev_part is None:
        before = None
    if next_part is None:
        return out.iloc[before:]
    return out.iloc[before:-after]

def combine_concat_plans(plans, concat_axis):
    """
    Combine multiple concatenation plans into one.

    existing_plan is updated in-place.
    """
    if len(plans) == 1:
        for p in plans[0]:
            yield p[0], [p[1]]

    elif concat_axis == 0:
        offset = 0
        for plan in plans:
            last_plc = None

            for plc, unit in plan:
                yield plc.add(offset), [unit]
                last_plc = plc

            if last_plc is not None:
                offset += last_plc.as_slice.stop

    else:
        num_ended = [0]
        def _next_or_none(seq):
            retval = next(seq, None)
            if retval is None:
                num_ended[0] += 1
            return retval

        plans = list(map(iter, plans))
        next_items = list(map(_next_or_none, plans))

        while num_ended[0] != len(next_items):
            if num_ended[0] > 0:
                raise ValueError("Plan shapes are not aligned")

            placements, units = zip(*next_items)

            lengths = list(map(len, placements))
            min_len, max_len = min(lengths), max(lengths)

            if min_len == max_len:
                yield placements[0], units
                next_items[:] = map(_next_or_none, plans)
            else:
                yielded_placement = None
                yielded_units = [None] * len(next_items)
                for i, (plc, unit) in enumerate(next_items):
                    yielded_units[i] = unit
                    if len(plc) > min_len:
                        # trim_join_unit updates unit in place, so only
                        # placement needs to be sliced to skip min_len.
                        next_items[i] = (plc[min_len:],
                                         trim_join_unit(unit, min_len))
                    else:
                        yielded_placement = plc
                        next_items[i] = _next_or_none(plans[i])

                yield yielded_placement, yielded_units

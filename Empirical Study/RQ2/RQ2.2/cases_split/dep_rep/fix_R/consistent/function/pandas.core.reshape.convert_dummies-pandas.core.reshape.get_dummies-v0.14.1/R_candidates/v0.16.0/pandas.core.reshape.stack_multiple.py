def stack_multiple(frame, level, dropna=True):
    # If all passed levels match up to column names, no
    # ambiguity about what to do
    if all(lev in frame.columns.names for lev in level):
        result = frame
        for lev in level:
            result = stack(result, lev, dropna=dropna)

    # Otherwise, level numbers may change as each successive level is stacked
    elif all(isinstance(lev, int) for lev in level):
        # As each stack is done, the level numbers decrease, so we need
        #  to account for that when level is a sequence of ints
        result = frame
        # _get_level_number() checks level numbers are in range and converts
        # negative numbers to positive
        level = [frame.columns._get_level_number(lev) for lev in level]

        # Can't iterate directly through level as we might need to change
        # values as we go
        for index in range(len(level)):
            lev = level[index]
            result = stack(result, lev, dropna=dropna)
            # Decrement all level numbers greater than current, as these
            # have now shifted down by one
            updated_level = []
            for other in level:
                if other > lev:
                    updated_level.append(other - 1)
                else:
                    updated_level.append(other)
            level = updated_level

    else:
        raise ValueError("level should contain all level names or all level numbers, "
                         "not a mixture of the two.")

    return result

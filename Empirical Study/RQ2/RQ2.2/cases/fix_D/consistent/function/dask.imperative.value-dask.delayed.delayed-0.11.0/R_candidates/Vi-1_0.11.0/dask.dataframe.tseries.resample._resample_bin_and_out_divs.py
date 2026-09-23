def _resample_bin_and_out_divs(divisions, rule, closed='left', label='left'):
    rule = pd.datetools.to_offset(rule)
    g = pd.TimeGrouper(rule, how='count', closed=closed, label=label)

    # Determine bins to apply `how` to. Disregard labeling scheme.
    divs = pd.Series(range(len(divisions)), index=divisions)
    temp = divs.resample(rule, how='count', closed=closed, label='left')
    tempdivs = temp.loc[temp > 0].index

    # Cleanup closed == 'right' and label == 'right'
    res = pd.offsets.Nano() if hasattr(rule, 'delta') else pd.offsets.Day()
    if g.closed == 'right':
        newdivs = tempdivs + res
    else:
        newdivs = tempdivs
    if g.label == 'right':
        outdivs = tempdivs + rule
    else:
        outdivs = tempdivs

    newdivs = newdivs.tolist()
    outdivs = outdivs.tolist()

    # Adjust ends
    if newdivs[0] < divisions[0]:
        newdivs[0] = divisions[0]
    if newdivs[-1] < divisions[-1]:
        if len(newdivs) < len(divs):
            setter = lambda a, val: a.append(val)
        else:
            setter = lambda a, val: a.__setitem__(-1, val)
        setter(newdivs, divisions[-1])
        if outdivs[-1] > divisions[-1]:
            setter(outdivs, outdivs[-1])
        elif outdivs[-1] < divisions[-1]:
            setter(outdivs, temp.index[-1])

    return tuple(map(pd.Timestamp, newdivs)), tuple(map(pd.Timestamp, outdivs))

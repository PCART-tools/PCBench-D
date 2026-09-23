def append_delta(row_list, base, exp):
    percent = 100 * ((exp - base) / base)
    row_list.append(percent)

def normalize_check_ad(check_ad, name):
    # normalized check_ad is 3-element tuple: (bool, List[str], List[str])
    if len(check_ad) == 0:
        check_ad = [False, ['aten::' + name], []]
    elif len(check_ad) == 1:
        check_ad = [check_ad[0], ['aten::' + name], []]
    elif len(check_ad) == 2:
        check_ad = [check_ad[0], check_ad[1], []]
    elif len(check_ad) == 3:
        check_ad = list(check_ad)
    else:
        raise Exception('Invalid check_ad, requires (bool, str|List[str], str|List[str])')

    check_ad = [[t] if isinstance(t, str) else t for t in check_ad]

    return check_ad

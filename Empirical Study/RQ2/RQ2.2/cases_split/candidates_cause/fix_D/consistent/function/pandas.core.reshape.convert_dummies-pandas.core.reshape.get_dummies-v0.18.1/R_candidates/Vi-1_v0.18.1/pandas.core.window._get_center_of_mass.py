def _get_center_of_mass(com, span, halflife, alpha):
    valid_count = len([x for x in [com, span, halflife, alpha]
                      if x is not None])
    if valid_count > 1:
        raise ValueError("com, span, halflife, and alpha "
                         "are mutually exclusive")

    # Convert to center of mass; domain checks ensure 0 < alpha <= 1
    if com is not None:
        if com < 0:
            raise ValueError("com must satisfy: com >= 0")
    elif span is not None:
        if span < 1:
            raise ValueError("span must satisfy: span >= 1")
        com = (span - 1) / 2.
    elif halflife is not None:
        if halflife <= 0:
            raise ValueError("halflife must satisfy: halflife > 0")
        decay = 1 - np.exp(np.log(0.5) / halflife)
        com = 1 / decay - 1
    elif alpha is not None:
        if alpha <= 0 or alpha > 1:
            raise ValueError("alpha must satisfy: 0 < alpha <= 1")
        com = (1.0 - alpha) / alpha
    else:
        raise ValueError("Must pass one of com, span, halflife, or alpha")

    return float(com)

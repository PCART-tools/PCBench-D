def is_re_compilable(obj):
    try:
        re.compile(obj)
    except TypeError:
        return False
    else:
        return True

def ifdynstaticdefault(count1, count2):
    if torch._dynamo.config.assume_static_by_default:
        return count1
    else:
        return count2

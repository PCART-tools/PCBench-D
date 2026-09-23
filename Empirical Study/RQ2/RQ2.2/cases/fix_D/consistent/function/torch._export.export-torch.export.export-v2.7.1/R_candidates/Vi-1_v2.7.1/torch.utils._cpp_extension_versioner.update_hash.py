def update_hash(seed, value):
    # Good old boost::hash_combine
    # https://www.boost.org/doc/libs/1_35_0/doc/html/boost/hash_combine_id241013.html
    return seed ^ (hash(value) + 0x9e3779b9 + (seed << 6) + (seed >> 2))

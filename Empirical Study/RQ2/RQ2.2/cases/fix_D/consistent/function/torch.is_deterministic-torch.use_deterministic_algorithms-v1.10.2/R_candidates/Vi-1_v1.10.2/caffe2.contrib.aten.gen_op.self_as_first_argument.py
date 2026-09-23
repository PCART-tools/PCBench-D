def self_as_first_argument(arguments):
    return ([a for a in arguments if a['name'] == 'self'] +
            [a for a in arguments if a['name'] != 'self'])

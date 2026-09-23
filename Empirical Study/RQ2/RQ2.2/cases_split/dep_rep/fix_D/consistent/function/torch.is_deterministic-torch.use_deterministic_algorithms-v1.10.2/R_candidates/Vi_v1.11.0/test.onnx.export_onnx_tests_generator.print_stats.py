def print_stats(FunctionalModule_nums, nn_module):
    print("{} functional modules detected.".format(FunctionalModule_nums))
    supported = []
    unsupported = []
    not_fully_supported = []
    for key, value in nn_module.items():
        if (value == 1):
            supported.append(key)
        elif (value == 2):
            unsupported.append(key)
        elif (value == 3):
            not_fully_supported.append(key)

    def fun(info, l):
        print(info)
        for v in l:
            print(v)

    # Fully Supported Ops: All related test cases of these ops have been exported
    # Semi-Supported Ops: Part of related test cases of these ops have been exported
    # Unsupported Ops: None of related test cases of these ops have been exported
    for info, l in [["{} Fully Supported Operators:".format(len(supported)),
                     supported],
                    ["{} Semi-Supported Operators:".format(len(not_fully_supported)),
                     not_fully_supported],
                    ["{} Unsupported Operators:".format(len(unsupported)),
                     unsupported]]:
        fun(info, l)

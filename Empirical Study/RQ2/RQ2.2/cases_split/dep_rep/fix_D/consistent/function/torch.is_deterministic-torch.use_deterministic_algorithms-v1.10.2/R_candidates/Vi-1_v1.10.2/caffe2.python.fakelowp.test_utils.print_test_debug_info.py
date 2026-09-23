def print_test_debug_info(testname, items_dict):
    filename = "debug_operator_onnxifi_" + testname + ".txt"
    np.set_printoptions(threshold=sys.maxsize)
    with open(filename, 'w') as f:
        for key, value in items_dict.items():
            print(key, value)
            f.write("{}\n".format(key))
            f.write("{}\n".format(value))

def print_results(result):
    print("===================================")
    for key, value in result.items():
        print("{}, latency per iter (us):{}".format(key, ms_to_us(value)))
    print("===================================")

def report_coverage() -> None:
    start_time = time.time()
    (options, test_list, interested_folders) = initialization()
    # run cpp tests
    get_json_report(test_list, options)
    # collect coverage data from json profiles
    if options.need_summary:
        summarize_jsons(test_list, interested_folders, [""], TestPlatform.OSS)
    # print program running time
    print_time("Program Total Time: ", start_time)

def initialization() -> Tuple[Option, TestList, List[str]]:
    # create folder if not exists
    create_folders()
    # add arguments
    parser = argparse.ArgumentParser()
    parser = add_arguments_utils(parser)
    parser = add_arguments_oss(parser)
    # parse arguments
    (options, args_interested_folder, args_run_only, arg_clean) = parse_arguments(
        parser
    )
    # clean up
    if arg_clean:
        clean_up_gcda()
        clean_up()
    # get test lists
    test_list = get_test_list(args_run_only)
    # get interested folder -- final report will only over these folders
    interested_folders = empty_list_if_none(args_interested_folder)
    # print initialization information
    print_init_info()
    # remove last time's log
    remove_file(os.path.join(LOG_DIR, "log.txt"))
    return (options, test_list, interested_folders)

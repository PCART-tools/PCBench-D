def main() -> None:
    test_file_paths = get_all_test_files()
    pytorch_labels = get_pytorch_labels()

    file_msgs = [validate_file(f, pytorch_labels) for f in test_file_paths]
    err_msg = "\n".join([x for x in file_msgs if x != ""])
    if err_msg != "":
        err_msg = err_msg + "\n\nIf you see files with missing ownership information above, " \
            "please add the following line\n\n# Owner(s): [\"<owner: label>\"]\n\nto the top of each test file. " \
            "The owner should be an existing pytorch/pytorch label."
        print(err_msg)
        sys.exit(1)

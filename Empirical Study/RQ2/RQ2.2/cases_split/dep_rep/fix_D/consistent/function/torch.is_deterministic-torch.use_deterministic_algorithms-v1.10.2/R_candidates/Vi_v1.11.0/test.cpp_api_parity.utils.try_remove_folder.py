def try_remove_folder(folder_path):
    if os.path.exists(folder_path):
        # Don't block the process if this fails, but show the error message as warning.
        try:
            shutil.rmtree(folder_path)
        except Exception as e:
            warnings.warn("Non-blocking folder removal fails with the following error:\n{}".format(str(e)))

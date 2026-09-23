def downloadModel(model, args):
    # Figure out where to store the model
    model_folder = '{folder}'.format(folder=model)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if args.install:
        model_folder = '{dir_path}/{folder}'.format(dir_path=dir_path,
                                                    folder=model)

    # Check if that folder is already there
    if os.path.exists(model_folder) and not os.path.isdir(model_folder):
        if not args.force:
            raise Exception("Cannot create folder for storing the model,\
                            there exists a file of the same name.")
        else:
            print("Overwriting existing file! ({filename})"
                  .format(filename=model_folder))
            os.remove(model_folder)
    if os.path.isdir(model_folder):
        if not args.force:
            response = ""
            query = "Model already exists, continue? [y/N] "
            try:
                response = raw_input(query)
            except NameError:
                response = input(query)
            if response.upper() == 'N' or not response:
                print("Cancelling download...")
                exit(0)
        print("Overwriting existing folder! ({filename})".format(filename=model_folder))
        deleteDirectory(model_folder)

    # Now we can safely create the folder and download the model
    os.makedirs(model_folder)
    for f in ['predict_net.pb', 'init_net.pb']:
        try:
            downloadFromURLToFile(getURLFromName(model, f),
                                  '{folder}/{f}'.format(folder=model_folder,
                                                        f=f))
        except Exception as e:
            print("Abort: {reason}".format(reason=str(e)))
            print("Cleaning up...")
            deleteDirectory(model_folder)
            exit(0)

    if args.install:
        os.symlink("{folder}/__sym_init__.py".format(folder=dir_path),
                   "{folder}/__init__.py".format(folder=model_folder))

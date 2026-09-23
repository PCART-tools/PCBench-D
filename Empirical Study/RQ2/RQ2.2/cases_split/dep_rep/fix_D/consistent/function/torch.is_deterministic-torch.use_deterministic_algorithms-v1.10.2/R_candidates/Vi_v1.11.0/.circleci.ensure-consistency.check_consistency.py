def check_consistency():

    _, temp_filename = tempfile.mkstemp("-generated-config.yml")

    with open(temp_filename, "w") as fh:
        generate_config_yml.stitch_sources(fh)

    try:
        subprocess.check_call(["cmp", temp_filename, CHECKED_IN_FILE])
    except subprocess.CalledProcessError:
        sys.exit(ERROR_MESSAGE_TEMPLATE % (CHECKED_IN_FILE, REGENERATION_SCRIPT, PARENT_DIR, README_PATH))
    finally:
        os.remove(temp_filename)

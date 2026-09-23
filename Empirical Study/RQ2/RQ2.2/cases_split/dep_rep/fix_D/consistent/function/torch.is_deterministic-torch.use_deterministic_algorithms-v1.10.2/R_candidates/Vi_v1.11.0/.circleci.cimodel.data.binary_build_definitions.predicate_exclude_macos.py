def predicate_exclude_macos(config):
    return config.os == "linux" or config.os == "windows"

@partial(normalize_token.register, OpenFileCreator)
def normalize_OpenFileCreator(ofc):
    return ofc.compression, ofc.text, ofc.encoding, ofc.protocol, ofc.storage_options

def getCodeLink(formatter, schema):
    formatter = formatter.clone()
    path = os.path.relpath(schema.file, "caffe2")
    schemaLink = ('https://github.com/pytorch/pytorch/blob/master/{path}'
                  .format(path=path))
    formatter.addLink('{path}'.format(path=path), schemaLink)
    return formatter.dump()

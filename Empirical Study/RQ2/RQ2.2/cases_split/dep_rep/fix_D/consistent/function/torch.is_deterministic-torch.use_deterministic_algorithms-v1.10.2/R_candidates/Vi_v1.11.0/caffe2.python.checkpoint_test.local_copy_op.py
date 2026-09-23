def local_copy_op(src, dest):
    def copy_op(inputs, outputs):
        shutil.copyfile(src, dest)
    return copy_op

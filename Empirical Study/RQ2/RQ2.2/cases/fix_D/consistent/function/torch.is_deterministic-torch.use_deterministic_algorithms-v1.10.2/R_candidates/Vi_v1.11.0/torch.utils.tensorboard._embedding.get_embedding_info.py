def get_embedding_info(metadata, label_img, filesys, subdir, global_step, tag):
    info = EmbeddingInfo()
    info.tensor_name = "{}:{}".format(tag, str(global_step).zfill(5))
    info.tensor_path = filesys.join(subdir, 'tensors.tsv')
    if metadata is not None:
        info.metadata_path = filesys.join(subdir, 'metadata.tsv')
    if label_img is not None:
        info.sprite.image_path = filesys.join(subdir, 'sprite.png')
        info.sprite.single_image_dim.extend([label_img.size(3), label_img.size(2)])
    return info

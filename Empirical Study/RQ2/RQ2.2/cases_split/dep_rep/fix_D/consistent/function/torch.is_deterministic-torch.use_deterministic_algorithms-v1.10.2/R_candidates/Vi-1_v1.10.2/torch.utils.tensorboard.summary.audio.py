def audio(tag, tensor, sample_rate=44100):
    tensor = make_np(tensor)
    tensor = tensor.squeeze()
    if abs(tensor).max() > 1:
        print('warning: audio amplitude out of range, auto clipped.')
        tensor = tensor.clip(-1, 1)
    assert(tensor.ndim == 1), 'input tensor should be 1 dimensional.'
    tensor = (tensor * np.iinfo(np.int16).max).astype('<i2')

    import io
    import wave
    fio = io.BytesIO()
    wave_write = wave.open(fio, 'wb')
    wave_write.setnchannels(1)
    wave_write.setsampwidth(2)
    wave_write.setframerate(sample_rate)
    wave_write.writeframes(tensor.data)
    wave_write.close()
    audio_string = fio.getvalue()
    fio.close()
    audio = Summary.Audio(sample_rate=sample_rate,
                          num_channels=1,
                          length_frames=tensor.shape[-1],
                          encoded_audio_string=audio_string,
                          content_type='audio/wav')
    return Summary(value=[Summary.Value(tag=tag, audio=audio)])

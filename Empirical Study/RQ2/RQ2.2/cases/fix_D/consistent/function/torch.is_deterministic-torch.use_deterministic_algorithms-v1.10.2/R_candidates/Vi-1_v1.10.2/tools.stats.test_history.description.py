def description() -> str:
    return r'''
Display the history of a test.

Each line of (non-error) output starts with the timestamp and SHA1 hash
of the commit it refers to, in this format:

    YYYY-MM-DD hh:mm:ss 0123456789abcdef0123456789abcdef01234567

In multiline mode, each line next includes the name of a CircleCI job,
followed by the time of the specified test in that job at that commit.
Example:

    $ tools/stats/test_history.py --mode=multiline --ref=594a66 --sha-length=8 --test=test_set_dir \
      --job pytorch_linux_xenial_py3_6_gcc5_4_test --job pytorch_linux_xenial_py3_6_gcc7_test
    2021-02-10 11:13:34Z 594a66d7 pytorch_linux_xenial_py3_6_gcc5_4_test 0.36s
    2021-02-10 11:13:34Z 594a66d7 pytorch_linux_xenial_py3_6_gcc7_test 0.573s errored
    2021-02-10 10:13:25Z 9c0caf03 pytorch_linux_xenial_py3_6_gcc5_4_test 0.819s
    2021-02-10 10:13:25Z 9c0caf03 pytorch_linux_xenial_py3_6_gcc7_test 0.449s
    2021-02-10 10:09:14Z 602434bc pytorch_linux_xenial_py3_6_gcc5_4_test 0.361s
    2021-02-10 10:09:14Z 602434bc pytorch_linux_xenial_py3_6_gcc7_test 0.454s
    2021-02-10 10:09:10Z 2e35fe95 (no reports in S3)
    2021-02-10 10:09:07Z ff73be7e (no reports in S3)
    2021-02-10 10:05:39Z 74082f0d (no reports in S3)
    2021-02-10 07:42:29Z 0620c96f pytorch_linux_xenial_py3_6_gcc5_4_test 0.414s
    2021-02-10 07:42:29Z 0620c96f pytorch_linux_xenial_py3_6_gcc5_4_test 0.476s
    2021-02-10 07:42:29Z 0620c96f pytorch_linux_xenial_py3_6_gcc7_test 0.377s
    2021-02-10 07:42:29Z 0620c96f pytorch_linux_xenial_py3_6_gcc7_test 0.326s

Another multiline example, this time with the --all flag:

    $ tools/stats/test_history.py --mode=multiline --all --ref=321b9 --delta=12 --sha-length=8 \
      --test=test_qr_square_many_batched_complex_cuda
    2021-01-07 10:04:56Z 321b9883 pytorch_linux_xenial_cuda10_2_cudnn7_py3_gcc7_test2 424.284s
    2021-01-07 10:04:56Z 321b9883 pytorch_linux_xenial_cuda10_2_cudnn7_py3_slow_test 0.006s skipped
    2021-01-07 10:04:56Z 321b9883 pytorch_linux_xenial_cuda11_1_cudnn8_py3_gcc7_test 402.572s
    2021-01-07 10:04:56Z 321b9883 pytorch_linux_xenial_cuda9_2_cudnn7_py3_gcc7_test 287.164s
    2021-01-06 20:58:28Z fcb69d2e pytorch_linux_xenial_cuda10_2_cudnn7_py3_gcc7_test2 436.732s
    2021-01-06 20:58:28Z fcb69d2e pytorch_linux_xenial_cuda10_2_cudnn7_py3_slow_test 0.006s skipped
    2021-01-06 20:58:28Z fcb69d2e pytorch_linux_xenial_cuda11_1_cudnn8_py3_gcc7_test 407.616s
    2021-01-06 20:58:28Z fcb69d2e pytorch_linux_xenial_cuda9_2_cudnn7_py3_gcc7_test 287.044s

In columns mode, the name of the job isn't printed, but the order of the
columns is guaranteed to match the order of the jobs passed on the
command line. Example:

    $ tools/stats/test_history.py --mode=columns --ref=3cf783 --sha-length=8 --test=test_set_dir \
      --job pytorch_linux_xenial_py3_6_gcc5_4_test --job pytorch_linux_xenial_py3_6_gcc7_test
    2021-02-10 12:18:50Z 3cf78395    0.644s    0.312s
    2021-02-10 11:13:34Z 594a66d7    0.360s  errored
    2021-02-10 10:13:25Z 9c0caf03    0.819s    0.449s
    2021-02-10 10:09:14Z 602434bc    0.361s    0.454s
    2021-02-10 10:09:10Z 2e35fe95
    2021-02-10 10:09:07Z ff73be7e
    2021-02-10 10:05:39Z 74082f0d
    2021-02-10 07:42:29Z 0620c96f    0.414s    0.377s (2 job re-runs omitted)
    2021-02-10 07:27:53Z 33afb5f1    0.381s    0.294s

Minor note: in columns mode, a blank cell means that no report was found
in S3, while the word "absent" means that a report was found but the
indicated test was not found in that report.
'''

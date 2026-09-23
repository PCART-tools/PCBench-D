def generate_doc_test(doc_test):
    def test(self, device):
        self.assertEqual(device, 'cpu')
        runner = doctest.DocTestRunner()
        runner.run(doc_test)

        if runner.failures != 0:
            runner.summarize()
            self.fail('Doctest failed')

    setattr(TestFFTDocExamples, 'test_' + doc_test.name, skipCPUIfNoFFT(test))

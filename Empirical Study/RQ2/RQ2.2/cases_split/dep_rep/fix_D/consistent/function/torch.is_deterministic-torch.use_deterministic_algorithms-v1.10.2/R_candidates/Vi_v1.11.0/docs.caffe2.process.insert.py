def insert(originalfile, first_line, description):
    with open(originalfile, 'r') as f:
        f1 = f.readline()
        if(f1.find(first_line) < 0):
            docs = first_line + description + f1
            with open('newfile.txt', 'w') as f2:
                f2.write(docs)
                f2.write(f.read())
            os.rename('newfile.txt', originalfile)
        else:
            print('already inserted')

def measureAllDistance(dataDis):

    normalizedData = []
    for i, data in enumerate(dataDis):
        tempDataSize = sum(data)
        if tempDataSize == 0:
            print('Error')
            return -1

        normalizedData.append(dit.ScalarDistribution(np.arange(len(data)), [c / float(tempDataSize) for c in data]))

    with open('divergenceInfo', 'w') as fout:
        pass

    divergence = []
    for f, dataA in enumerate(normalizedData):
        tempx = []
        for b in range(f + 1, len(normalizedData)):
            dig = jensen_shannon_divergence([dataA, normalizedData[b]])
            tempx.append(dig)
            divergence.append(dig)

        print('Finished ' + str(f))

        with open('divergenceInfo', 'a') as fout:
           fout.writelines(' '.join(str(x) for x in tempx) + '\n')

    return divergence

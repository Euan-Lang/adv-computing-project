def findMinList(datasetList): #must be numeric
    minValue = min(datasetList)
    minPos = datasetList.index(minValue)
    return minPos
def findMinDict(datasetDict):
    #key of smallest value
    smallestValueKey = min(datasetDict, key = lambda k: datasetDict[k])
    return smallestValueKey
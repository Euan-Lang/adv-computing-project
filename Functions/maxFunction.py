def findMaxList(datasetList): #must be numeric
    maxValue = max(datasetList)
    maxPos = datasetList.index(maxValue)
    return maxPos
def findMaxDict(datasetDict):
    #key of largest value
    largestValueKey = max(datasetDict, key = lambda k: datasetDict[k])
    return largestValueKey
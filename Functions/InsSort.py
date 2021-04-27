def insertionSort(arr):  
    for i in range(1, len(arr)): 
        key = arr[i] 
        j = i-1
        while j >=0 and key < arr[j] : 
                arr[j+1] = arr[j] 
                j -= 1
        arr[j+1] = key 
    return arr
def insertionSortDates(detentions):
    for i in range(1, len(detentions)): # first sort by year 
        key = detentions[i]
        j = i-1
        while j >=0 and int(key.getDetentionDate()[0:4]) < int(detentions[j].getDetentionDate()[0:4]) : 
                detentions[j+1] = detentions[j]        
                j -= 1                               
        detentions[j+1] = key

    for i in range(1, len(detentions)): # then sort by month
        key = detentions[i]
        j = i-1
        while j >=0 and key.getDetentionDate()[0:4] <= detentions[j].getDetentionDate()[0:4] and key.getDetentionDate()[5:7]< detentions[j].getDetentionDate()[5:7]: #key.getDetentionDate()[0:4] <= detentions[j].getDetentionDate()[0:4] this ensures the months are only sorted with their year
                detentions[j+1] = detentions[j]
                j -= 1
        detentions[j+1] = key
    for i in range(1, len(detentions)): # finally sort by day
        key = detentions[i]
        j = i-1
        while j >=0 and key.getDetentionDate()[0:4] <= detentions[j].getDetentionDate()[0:4] and key.getDetentionDate()[5:7]<= detentions[j].getDetentionDate()[5:7] and key.getDetentionDate()[8:10] < detentions[j].getDetentionDate()[8:10]: #key.getDetentionDate()[0:4] <= detentions[j].getDetentionDate()[0:4] and key.getDetentionDate()[5:7]< detentions[j].getDetentionDate()[5:7]  Ensure the days are only sorted within their month and year
                detentions[j+1] = detentions[j]
                j -= 1
        detentions[j+1] = key 
    return detentions

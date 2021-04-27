def binarySearch(array,query):
    found = False
    start =0
    end = len(array)-1
    pos=-1
    comparisons = 0

    while (start <= end) and found == False :
        comparisons += 1
        middle = (start + end) // 2
        if array[middle] == query:
            found = True
            pos = middle
        elif array[middle] < query:
            start = middle + 1
        else:
            end = middle - 1
    print("Comparisons:", comparisons)
    return pos
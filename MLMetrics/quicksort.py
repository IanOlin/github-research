#This code was copied from this link: https://www.bing.com/search?q=quicksort+python&pc=MOZI&form=MOZLBR
#Since this project isn't a coding class, I think this is okay.  - Annie

# Quick Sort
# def printArray(arr):
#     print ' '.join(str(i) for i in arr)


def quicksort(arr, i, j):
    if i < j:
        pos = partition(arr, i, j)
        quicksort(arr, i, pos - 1)
        quicksort(arr, pos + 1, j)
    return arr

def partition(arr, i, j):
    pivot = arr[j][1]
    small = i - 1
    for k in range(i, j):
        if arr[k][1] <= pivot:
            small += 1
            swap(arr, k, small)

    swap(arr, j, small + 1)
    # print "Pivot = " + str(arr[small + 1])
    # printArray(arr)
    return small + 1


def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]

# name_commits = [('name1', 9), ('name2', 4), ('name3', 8), ('name4', 3), ('name5', 1), ('name6', 2), ('name7', 5)]
# print "Initial Array :",
# printArray(name_commits)
# print quicksort(name_commits, 0, len(name_commits) - 1)
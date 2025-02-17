import random


def bubbleSort(arr):
    """
    function for bubble sorting the array (used this since it has easier implementation).
    loop through the array from end to beginning.
    initialize swapped to False at the beginning of each pass.
    inner loop to compare adjacent elements.
    if the current element is greater than the next element, swap them:
        set swapped to True to indicate a swap occurred.
    if no elements were swapped, the array is sorted, and we can exit the loop
    return the sorted array. 
    """
    for n in range(len(arr) - 1, 0, -1):
        swapped = False
        for i in range(n):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        if not swapped:
            break
    return arr


"""
generate list with 100 random numbers raning from 1 to 1000
"""
lst = random.sample(range(1, 1001), 100)


"""
filter lst into two lists, one with odd numbers second with even number.
Filter by if the number is divided by 2 or not.
"""
oddNum = list(filter(lambda x: x % 2 != 0, lst))
evenNum = list(filter(lambda x: x % 2 == 0, lst))

"""
Printing and displaying everything
"""
print("Unsorted List:", lst)
print("Sorted List:", bubbleSort(lst))

print("Avarage of Odd Numbers:", sum(oddNum) / len(oddNum))
print("Avarage of Even Numbers:", sum(evenNum) / len(evenNum))

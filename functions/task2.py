import random
import string 



# Task 1
def generateDicts():
    # initialize random numbers for number of dicts and keys inside
    dictsNum = random.randint(2, 10) 
    ret = []
    keysNum = random.randint(1, 10) 
    for _ in range(dictsNum): 
        # generate a random number of keys between 1 and 10 
        keys = random.sample(string.ascii_lowercase, keysNum)
        # create a dict with random values between 0 and 100
        dct = {key: random.randint(0, 100) for key in keys}
        ret.append(dct)
    return ret



# Task 2
def createCommonDict(dictList):
    commonDict = {}
    # iterate through each dict 
    for i, d in enumerate(dictList, 1):
        # For each key-value pair in  current dict
        for key, value in d.items():
            # If the key already exists in commonDict
            if key in commonDict:
                # If the new value is greater than the stored value
                if value > commonDict[key][1]:
                    # Update value
                    commonDict[key] = (i, value)
            else:
                # If key doesn't exist, add it with the current dict number and value
                commonDict[key] = (i, value)
    ret = {}
    # Iterate over previously created dict
    for key, (dict_num, value) in commonDict.items():
        # Count how many dictionaries contain this key
        key_count = sum(1 for d in dictList if key in d)
        # check if key appears in more than one dict
        if key_count > 1:
            # add the key with different numbering suffic
            ret[f"{key}_{dict_num}"] = value
        else:
            # If the key appears only once, add it as is
            ret[key] = value 
    return ret


# Displaying
temp = generateDicts()
print("Generated Dictionary: ", temp)
print("\n" + "Common Dictionary for Generated: ", createCommonDict(temp))


test = [{'r': 0, 'f': 83}, {'q': 58, 'e': 49}, 
        {'q': 65, 'i': 10}, {'o': 79, 'q': 7},
        {'n': 35, 'i': 56}, {'k': 13, 'h': 3},
        {'e': 80, 'a': 37}, {'i': 83, 'y': 67}]
"""
Expected Output:
{'r': 0, 'f': 83, 'q_3': 65, 'e_7': 80, 'i_8': 83, 'o': 79, 'n': 35, 'k': 13, 'h': 3, 'a': 37, 'y': 67}
"""
print("\n" + "Common Dictionary: ",  createCommonDict(test))
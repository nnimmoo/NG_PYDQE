import re

# given text to variable
text = """  tHis iz your homeWork, copy these Text to variable.

  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

  it iZ misspeLLing here. fix"iZ" with correct "is", but ONLY when it Iz a mistAKE.

  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

# capitalize the first letter of each sentence and turn all others into lowercases
sentences = re.split(r'([.!?]+(?:\s+|\Z))', text.lower())
capitalizedSentences = []
for i, s in enumerate(sentences):
    if i == 0 or (i % 2 == 0 and s.strip()):
        s = s.lstrip()  # remove leading whitespace
        if s:  # check if the string is not empty or not
            s = s[0].upper() + s[1:]
    capitalizedSentences.append(s)

normalized = ''.join(capitalizedSentences)

# create a new sentence with the last words of each existing sentence
sentences = re.split(r'[.!?]+', normalized)
last_words = [sentence.strip().split()[-1] for sentence in sentences if sentence.strip()]
newSentence = " ".join(last_words).capitalize() + "."

# change the occurrences of 'iz' only when it is surrounded by whitespaces and is not part of the word
corrected = re.sub(r'(^|\s)(iz)($|\s)', r'\1is\3', normalized, flags=re.IGNORECASE | re.MULTILINE)

# add the new sentence to the end of the paragraph
ret = corrected + "\n\n" + newSentence

# print the result
print(ret)

# calculate the number of whitespace characters in the original text and print
print(f"\nNumber of whitespace characters: {len(re.findall(r'[\s]', text))}")
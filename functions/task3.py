import re

# given text to variable
text = """  tHis iz your homeWork, copy these Text to variable.

  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

  it iZ misspeLLing here. fix"iZ" with correct "is", but ONLY when it Iz a mistAKE.

  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

# capitalize the first letter of each sentence and turn all others into lowercases
def capitalizeSentences(text):
      # split the text into sentences (regex matches sentence-ending punctuation marks, followed by whitespace)
    sentences = re.split(r'([.!?]+(?:\s+|\Z))', text)
    #capitalize the first letter of each sentence
    capitalizedSentences = []
    for i, s in enumerate(sentences):
        if i == 0 or (i % 2 == 0 and s.strip()):
            s = s.lstrip()  # remove leading whitespace
            if s:  # check if the string is not empty or not
                s = s[0].upper() + s[1:]
        capitalizedSentences.append(s)
    
    return ''.join(capitalizedSentences)


normalized = capitalizeSentences(text.lower())

# create a new sentence with the last words of each existing sentence. first split the sentences
sentences = re.split(r'[.!?]+', normalized)
# then get the last words
last_words = [sentence.strip().split()[-1] for sentence in sentences if sentence.strip()]
newSentence = " ".join(last_words).capitalize() + "."

# change the occurances of 'iz' only when it is surrounded by whitespaces and is not part of the word. (also when part of Fix"iz" since its kinda indicator and not a mistake)
corrected = re.sub(r'(^|\s)(iz)($|\s)', r'\1is\3', normalized, flags=re.IGNORECASE | re.MULTILINE)

# add the new sentence to the end of the paragraph
ret = corrected + "\n\n" + newSentence
# print
print(ret)

# calculate the number of whitespace characters in the original text and print
print(f"\nNumber of whitespace characters: {len(re.findall(r'[\s]', text))}")
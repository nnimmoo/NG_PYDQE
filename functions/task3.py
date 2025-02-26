import re

def capitalizeSentences(text):
    sentences = re.split(r'([.!?]+(?:\s+|\Z))', text)
    capitalizedSentences = []
    for i, s in enumerate(sentences):
        if i == 0 or (i % 2 == 0 and s.strip()):
            s = s.lstrip()
            if s:
                s = s[0].upper() + s[1:]
        capitalizedSentences.append(s)
    return ''.join(capitalizedSentences)

def normalize_text(text):
    return capitalizeSentences(text.lower())

def create_last_words_sentence(text):
    sentences = re.split(r'[.!?]+', text)
    last_words = [sentence.strip().split()[-1] for sentence in sentences if sentence.strip()]
    return " ".join(last_words).capitalize() + "."

def correct_iz(text):
    return re.sub(r'(^|\s)(iz)($|\s)', r'\1is\3', text, flags=re.IGNORECASE | re.MULTILINE)

def combine_text(text, new_sentence):
    return text + "\n\n" + new_sentence

def count_whitespace(text):
    return len(re.findall(r'[\s]', text))

def process_text(text):
    normalized = normalize_text(text)
    new_sentence = create_last_words_sentence(normalized)
    corrected = correct_iz(normalized)
    result = combine_text(corrected, new_sentence)
    whitespace_count = count_whitespace(text)
    return result, whitespace_count

if __name__ == "__main__":
    text = """  tHis iz your homeWork, copy these Text to variable.

    You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

    it iZ misspeLLing here. fix"iZ" with correct "is", but ONLY when it Iz a mistAKE.

    last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""

    result, whitespace_count = process_text(text)
    print(result)
    print(f"\nNumber of whitespace characters: {whitespace_count}")
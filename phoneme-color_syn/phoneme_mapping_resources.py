# https://linguistics.stackexchange.com/questions/29408/given-both-a-word-and-the-corresponding-ipa-how-to-match-map-the-letters-togeth
# ML lib to map the IPA output onto each letter of the input:
# https://github.com/AdolfVonKleist/Phonetisaurus

# lib that includes the semantic meaning of words to phonemize:
from gruut import sentences  

text = 'He wound it around the wound, saying "I read it was $10 to read."'

for sent in sentences(text, lang="en-us"):
    for word in sent:
        if word.phonemes:
            print(word.text, *word.phonemes)

from nltk import word_tokenize
from nltk import ngrams
import pickle

def buildLangModel(file_name):
    # open the file and remove the new lines
    file = open(file_name,"r", encoding='utf-8')
    text = file.read()
    text = text.replace('\n','')

    # tokenize the text and make the unigram and bigram lists
    tokenized_text = word_tokenize(text)
    unigrams = word_tokenize(text)
    bigrams = list(ngrams(tokenized_text,2))

    # make a dictionary for both unigrams and bigrams and their counts
    unigram_dict = {t: unigrams.count(t) for t in set(unigrams)}
    bigram_dict = {b: bigrams.count(b) for b in set(bigrams)}

    # return both dictionaries
    return unigram_dict, bigram_dict

def main():

    # for each language file call the build model function and pickle both returned dictionaries
    nameE = "LangID.train.English"
    uDictE, bDictE = buildLangModel(nameE)
    pickle.dump(uDictE, open('English_Unigram_dict.p', 'wb'))
    pickle.dump(bDictE, open('English_Bigram_dict.p', 'wb'))

    nameF = "LangID.train.French"
    uDictF, bDictF = buildLangModel(nameF)
    pickle.dump(uDictF, open('French_Unigram_dict.p', 'wb'))
    pickle.dump(bDictF, open('French_Bigram_dict.p', 'wb'))

    nameI = "LangID.train.Italian"
    uDictI, bDictI = buildLangModel(nameI)
    pickle.dump(uDictI, open('Italian_Unigram_dict.p', 'wb'))
    pickle.dump(bDictI, open('Italian_Bigram_dict.p', 'wb'))


if __name__ == "__main__":
    main()

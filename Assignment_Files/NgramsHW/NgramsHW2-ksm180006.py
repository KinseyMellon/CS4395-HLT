import pickle
from nltk import word_tokenize, ngrams


def calcAccuracy(test_filename, sol_filename):

    # open the file with the predictions and the right answers
    test_file = open(test_filename, 'r')
    sol_file = open(sol_filename, 'r')

    # get the lines from the files
    test_lines = test_file.readlines()
    sol_lines = sol_file.readlines()

    # initialize the number correct and make a list to hold the wrong line numbers
    num_correct = 0
    list_wrong = []

    # loop through both files comparing the predicted language and correct langauge
    for x in range(len(sol_lines)):
        # if its wrong add the line number to the list
        if test_lines[x] != sol_lines[x]:
            list_wrong.append(x+1)
        else:
            # if its right add one to the number correct
            num_correct += 1

    # calculate and print the percentage correct and print the incorrect line numbers
    print("Percentage correct: ", (num_correct/len(sol_lines))*100,"%")
    print("Incorrectly classified line numbers: ",end="")
    print(*list_wrong, sep=', ')

    # close the files
    test_file.close()
    sol_file.close()

def main():
    # unpickle the 6 dictionaries from the first program
    English_bigram_dict = pickle.load(open('English_Bigram_dict.p', 'rb'))
    English_unigram_dict = pickle.load(open('English_Unigram_dict.p', 'rb'))
    French_bigram_dict = pickle.load(open('French_Bigram_dict.p', 'rb'))
    French_unigram_dict = pickle.load(open('French_Unigram_dict.p', 'rb'))
    Italian_bigram_dict = pickle.load(open('Italian_Bigram_dict.p', 'rb'))
    Italian_unigram_dict = pickle.load(open('Italian_Unigram_dict.p', 'rb'))

    # open the file of lines to test the language models on
    test_file = open("LangID.test", "r", encoding='utf-8')
    lines = test_file.readlines()

    # open a file to write the classified language from the calculated probablities
    file = open('Language_Probablilites.txt','w')

    # find the total amount of tokens
    v = len(English_unigram_dict) + len(French_unigram_dict) + len(Italian_unigram_dict)

    # counter to print the line number
    counter = 1

    # loop through each line in the file
    for line in lines:

        # find the unigrams and bigrams for each line
        unigrams = word_tokenize(line)
        bigrams = list(ngrams(unigrams,2))

        # intialize the probablilites
        EngProb = 1.0
        FreProb = 1.0
        ItProb = 1.0

        # find each language probablity for each bigram
        for b in bigrams:
            bc1 = English_bigram_dict[b] if b in English_bigram_dict else 0
            uc1 = English_unigram_dict[b[0]] if b[0] in English_unigram_dict else 0
            EngProb = EngProb * ((bc1 + 1)/(uc1 + v))

            bc2 = French_bigram_dict[b] if b in French_bigram_dict else 0
            uc2 = French_unigram_dict[b[0]] if b[0] in French_unigram_dict else 0
            FreProb = FreProb * ((bc2 + 1)/(uc2 + v))

            bc3 = Italian_bigram_dict[b] if b in Italian_bigram_dict else 0
            uc3 = Italian_unigram_dict[b[0]] if b[0] in Italian_unigram_dict else 0
            ItProb = ItProb * ((bc3 + 1)/(uc3 + v))

        # write the line number and language with max probability to the output file
        file.write(str(counter))
        if EngProb > FreProb and EngProb > ItProb:
            file.write(' English\n')
        elif FreProb > EngProb and FreProb > ItProb:
            file.write(' French\n')
        else:
            file.write(' Italian\n')
        counter += 1

    # close the file
    file.close()

    # call the function to calculate the accuracy
    sol_filename = "LangId.sol"
    test_filename = "Language_Probablilites.txt"
    calcAccuracy(test_filename,sol_filename)


if __name__ == "__main__":
    main()

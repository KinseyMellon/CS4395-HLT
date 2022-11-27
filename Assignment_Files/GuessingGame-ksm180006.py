import sys
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from random import seed
from random import randint

def lexDiv(text):
    tokens = nltk.word_tokenize(text)
    tokens2 = [t.lower() for t in tokens]
    set1 = set(tokens2)
    print("Number of tokens: ", len(tokens2))
    print("Number of unique tokens: ", len(set1))
    print("Lexical diversity: %.2f" % (len(set1) / len(tokens2)))

def preprocess_text(text):
    # get the tokens and reduce them to only the ones that are alpha, not a stopword and longer than 5
    tokens = nltk.word_tokenize(text)
    tokens2 = [t.lower() for t in tokens]
    tokens3 = [t for t in tokens2 if t.isalpha() and t not in stopwords.words('english') and len(t) > 5]

    # lemmas
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tokens3]
    unique_lemmas = list(set(lemmas))

    # pos tagging on lemmas
    tags = nltk.pos_tag(unique_lemmas)
    print("\nPOS tags for first 20 lemmas: ",tags[:20])

    # make list of nouns
    nouns = []
    for word, tag in tags:
        if tag == "NN" or tag == "NNS" or tag == "NNP" or tag == "NNPS":
            nouns.append(word)

    # print number of tokens and number of nouns
    print("\nNumber of tokens: ", len(tokens3))
    print("Number of nouns: ", len(nouns))

    # return the list of tokens and nouns
    return tokens3, nouns

def GuessingGame(word_list):
    # initialize score to 5
    score = 5

    # create a list to hold the letters guessed to prevent double guessing
    guesses = []

    # loop 50 times, the amount of words the game has
    for i in range(50):
        # randomly choose a word for guessing
        word = word_list[randint(1, 49)]

        # make a list to show the correct guesses
        guess_list = []
        for k in range(len(word)):
            guess_list.append("_")

        # clear the guessed letters before each word
        guesses.clear()

        # have a flag to check that the score is still positive
        flag = True
        while flag:
            # print the word with the blanks left to guess
            print(guess_list)

            # prompt for input
            guess = input("Guess a letter: ")

            # if ! is input quit the game
            if guess == "!":
                return

            # if the letter has already been guessed say that and continue to allow for the next guess
            if guess in guesses:
                print("Letter already guessed, try again")
                continue

            # check if the letter guessed is in the letter
            if guess in word:
                # add to the score and add the letter to the right spot in the word
                score += 1
                print("Correct! Score is ", score)
                for l in range(len(word)):
                    if guess == word[l]:
                        guess_list[l] = guess
                # check if the word is solved with that guess if it is print the word
                if "_" not in guess_list:
                    # set flag too false to get new word
                    flag = False
                    print("You solved it!")
                    print(word)
            else:
                # subtract from the score if wrong
                score -= 1
                print("Incorrect, guess again. Score is ", score)

            # add the letter to the list of guessed letters
            guesses.append(guess)

            # if the score is negative quit the game
            if score < 0:
                print("Game lost :( ")
                return

        print("\nCurrent score: ", score)

def main():

    seed(1234)

    # check if the sysarg has a file path
    if len(sys.argv) > 1:
        # it does so read it
        arg_input = sys.argv[1]

        # open the file
        with open(os.path.join(os.getcwd(), arg_input), 'r') as f:
            raw_text = f.read()

        # get lexical diversity
        lexDiv(raw_text)

        # preprocess the text and get the list of tokens and nouns back from the function
        tokens, nouns = preprocess_text(raw_text)

        # make dictionary of nouns and counts and find 50 most common
        noun_counts = {t: tokens.count(t) for t in nouns}
        ordered_dict = sorted(noun_counts.items(), key=lambda y: y[1], reverse=True)
        noun_list = []
        x = range(50)
        for n in x:
            noun_list.append(ordered_dict[n][0])

        # print 50 most common nouns
        print("\n50 most common nouns: ", ordered_dict[:50])

        # guessing game function
        print("Now playing the word Guessing Game!!")
        GuessingGame(noun_list)
    else:
        # error message if there was no file entered
        print("error, no file path entered")


if __name__ == "__main__":
    main()

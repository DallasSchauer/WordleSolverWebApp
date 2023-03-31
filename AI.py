import random
import quordle

# CLASS: AI
# base class for AI that will try to guess the answer.
# base one just picks a random word from its pool.
# ARGS:
# guessPool - list of answers it can use
# numPools - the number of different word pools it must maintain.
# (1 for wordle, 4 for quordle, etc.)
class AI:
    def __init__(self, guessPool, numPools):
        self.guessPools = []
        self.guessPools.append(guessPool)
        self.poolToChooseFrom = self.guessPools[0]
        # make the desired number of word pools.
        i = 1
        while i < numPools:
            temp = guessPool.copy() # need to make copies or python messes up
            self.guessPools.append(temp)
            i += 1

    # function that will pick word, overridden by each child class.
    def pickWord(self):
        self.pickPool() # function that determines what pool of the AI's we
                        # should pick a word from.
        ret = random.choice(self.poolToChooseFrom)
        self.poolToChooseFrom.remove(ret) # remove choice once done.
        return ret

    # function that picks the pool we should be taking a word from. generally,
    # i think it should be the pool with the largest number of possible words
    # left, because we have the highest potential info gain that way.
    def pickPool(self):
        mostWordsLeft = 0
        i = 0
        for pool in self.guessPools:
            length = len(self.guessPools[i])
            if length == 1: # if only one possible word
                self.poolToChooseFrom = self.guessPools[i]
                break # immediately choose this word, because we need to
                      # eventually and we can get info from it.
            elif length > mostWordsLeft:
                self.poolToChooseFrom = self.guessPools[i] # assigns pool with
                                                           # words left
                mostWordsLeft = length
            i += 1

    # function that uses the hints provided by the game to eliminate
    # words from the pools. all children can use this function because
    # they will all work this way.
    def interpretHint(self, hint, guess, guessPool):
            count = 0;
            for letter in hint:
                if letter == "G":
                    self.greenLetter(guess[count], count, guessPool)
                elif letter == "Y":
                    self.yellowLetter(guess[count], count, guessPool)
                elif letter == "B":
                    self.blackLetter(guess[count], guessPool)
                count += 1

    # function that eliminates words from the pools that do not have
    # the green letter in the same spot.
    def greenLetter(self, letter, spot, guessPool):
        for word in range(len(guessPool) - 1, -1, -1):
            ex = guessPool[word]
            if ex[spot] != letter:
                guessPool.remove(ex)

    # function that eliminates words from the pools that do not abide
    # by the yellow rule (in word but different spot).
    def yellowLetter(self, letter, spot, guessPool):
        for word in range(len(guessPool) - 1, -1, -1):
            ex = guessPool[word]
            if letter not in ex:
                guessPool.remove(ex)
            if ex[spot] == letter:
                guessPool.remove(ex)


    # function that eliminates words from the pools that have an instance
    # of a black letter.
    def blackLetter(self, letter, guessPool):
        for word in range(len(guessPool) - 1, -1, -1):
            ex = guessPool[word]
            if letter in ex:
                guessPool.remove(ex)

    # def priority(self, ele):
    #     return len(list(set(ele)))



# CLASS: UNIQUE WORDS
# subclass of AI that is slightly more advanced and prioritizes words that
# more unique (don't reappear in the word) to reveal more information
class UniqueWords(AI):

    def __init__(self, guessPool, numPools):
        self.guessPools = []
        self.guessPools.append(guessPool)
        self.guessPools[0].sort(key=self.priority, reverse=True)

        i = 1
        while i < numPools:
            temp = self.guessPools[0].copy()
            self.guessPools.append(temp)
            i += 1

    def pickWord(self):
        self.pickPool()

        viableWords = []
        threshHold = self.priority(self.poolToChooseFrom[0])
        for word in self.poolToChooseFrom:
            if self.priority(word) < threshHold:
                break
            viableWords.append(word)
        ret = random.choice(viableWords)
        self.poolToChooseFrom.remove(ret)
        return ret

    def priority(self, ele):
        return len(list(set(ele)))

    def uniqueLetters(self, word):
        unique = []
        for letter in word:
            if letter not in unique:
                unique.append(letter)
        return len(unique)

# CLASS: SCRABBLE
# subclass of AI that prioritizes words with a low scrabble score, as
# they use more common letters.
class Scrabble(AI):
    def __init__(self, guessPool, numPools):
        self.guessPools = []
        self.guessPools.append(guessPool)
        self.guessPools[0].sort(key=self.ScrabbleWord, reverse=True)

        i = 1
        while i < numPools:
            temp = self.guessPools[0].copy()
            self.guessPools.append(temp)
            i += 1

    def pickWord(self):
        self.pickPool()
        ret = self.poolToChooseFrom[0]
        self.poolToChooseFrom.remove(ret)
        return ret

    def ScrabbleWord(self, word):
        count = 0
        for letter in list(set(word[:5])):
            temp = 11 - self.ScrabbleValue[letter]
            count += temp
        return count

    ScrabbleValue = {
                'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1,
                'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8,
                'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1,
                'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1,
                'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z':10
        }

# CLASS : COMMONLETTERS
# subclass of AI that uses actual letter probabilities from the valid
# pool of answers.
class CommonLetters(AI):
    def __init__(self, guessPool, numPools):
        self.guessPools = []
        self.guessPools.append(guessPool)
        self.guessPools[0].sort(key=self.CommonWord, reverse=True)

        i = 1
        while i < numPools:
            temp = self.guessPools[0].copy()
            self.guessPools.append(temp)
            i += 1

    def pickWord(self):
        self.pickPool()
        ret = self.poolToChooseFrom[0]
        self.poolToChooseFrom.remove(ret)
        return ret

    def CommonWord(self, word):
        count = 0
        for letter in list(set(word[:5])):
            count += self.PercentageValue[letter]
        return count

    PercentageValue = {
                'a': .393, 'b': .115, 'c': .194, 'd': .160, 'e': .456,
                'f': .089, 'g': .130, 'h': .164, 'i': .280, 'j': .012,
                'k': .087, 'l': .280, 'm': .129, 'n': .238, 'o': .291,
                'p': .149, 'q': .013, 'r': .362, 's': .267, 't': .288,
                'u': .197, 'v': .064, 'w': .084, 'x': .016, 'y': .180, 'z': .015
        }

# CLASS - COMMONLETTERSPOTS
# subclass of AI that is similar to CommonWords, but more nuanced in that it
# also prioritizes words with letters in common spots.
class CommonLetterSpots(AI):
    def __init__(self, guessPool, numPools):
        self.guessPools = []
        self.guessPools.append(guessPool)
        self.guessPools[0].sort(key=self.CommonLetterSpot, reverse=True)

        i = 1
        while i < numPools:
            temp = self.guessPools[0].copy()
            self.guessPools.append(temp)
            i += 1

    def pickWord(self):
        self.pickPool()
        ret = self.poolToChooseFrom[0]
        self.poolToChooseFrom.remove(ret)
        return ret

    def CommonLetterSpot(self, word):
        count = 0
        multiplier = 2 # weight for the letter spots. can change, but this
                        # best so far.
        count += multiplier * self.FirstLetter[word[0]]
        count += multiplier * self.SecondLetter[word[1]]
        count += multiplier * self.ThirdLetter[word[2]]
        count += multiplier * self.FourthLetter[word[3]]
        count += multiplier * self.FifthLetter[word[4]]
        for letter in list(set(word[:5])):
            count += self.PercentageValue[letter]
        return count

    PercentageValue = {
                'a': .393, 'b': .115, 'c': .194, 'd': .160, 'e': .456,
                'f': .089, 'g': .130, 'h': .164, 'i': .280, 'j': .012,
                'k': .087, 'l': .280, 'm': .129, 'n': .238, 'o': .291,
                'p': .149, 'q': .013, 'r': .362, 's': .267, 't': .288,
                'u': .197, 'v': .064, 'w': .084, 'x': .016, 'y': .180, 'z': .015
        }

    # how common a letter is in the first spot of a word.
    FirstLetter = {
                'a': .061, 'b': .075, 'c': .086, 'd': .048, 'e': .031,
                'f': .059, 'g': .050, 'h': .030, 'i': .015, 'j': .009,
                'k': .009, 'l': .038, 'm': .046, 'n': .016, 'o': .018,
                'p': .061, 'q': .010, 'r': .045, 's': .158, 't': .064,
                'u': .014, 'v': .019, 'w': .036, 'x': 0, 'y': .003, 'z': .001
        }

    # how common a letter is in the second spot of a word.
    SecondLetter = {
                'a': .131, 'b': .007, 'c': .017, 'd': .009, 'e': .105,
                'f': .003, 'g': .005, 'h': .062, 'i': .087, 'j': .001,
                'k': .004, 'l': .087, 'm': .016, 'n': .038, 'o': .121,
                'p': .026, 'q': .002, 'r': .115, 's': .007, 't': .033,
                'u': .080, 'v': .007, 'w': .019, 'x': .006, 'y': .010, 'z': .001
        }

    # how common a letter is in the third spot of a word.
    ThirdLetter = {
                'a': .133, 'b': .025, 'c': .024, 'd': .032, 'e': .077,
                'f': .011, 'g': .029, 'h': .004, 'i': .115, 'j': .001,
                'k': .005, 'l': .048, 'm': .026, 'n': .060, 'o': .105,
                'p': .025, 'q': .001, 'r': .070, 's': .035, 't': .048,
                'u': .071, 'v': .021, 'w': .011, 'x': .005, 'y': .013, 'z': .005
        }

    # how common a letter in the fourth spot of a word.
    FourthLetter = {
                'a': .070, 'b': .010, 'c': .066, 'd': .030, 'e': .137,
                'f': .015, 'g': .033, 'h': .012, 'i': .068, 'j': .001,
                'k': .024, 'l': .070, 'm': .029, 'n': .079, 'o': .057,
                'p': .022, 'q': 0, 'r': .066, 's': .074, 't': .060,
                'u': .035, 'v': .020, 'w': .011, 'x': .001, 'y': .001, 'z': .009
        }

    # how commmon a letter is in the fifth spot of a word.
    FifthLetter = {
                'a': .028, 'b': .005, 'c': .013, 'd': .051, 'e': .183,
                'f': .011, 'g': .018, 'h': .060, 'i': .005, 'j': 0,
                'k': .049, 'l': .067, 'm': .018, 'n': .056, 'o': .025,
                'p': .024, 'q': 0, 'r': .092, 's': .016, 't': .109,
                'u': 0, 'v': 0, 'w': .007, 'x': .003, 'y': .157, 'z': .002
        }

# CLASS::: STATICSTARTERS
# Subclass of AI that starts with the same 2-3 words every game, from a
# suggestion from one of our sources. After the static start, the strategy
# again uses CommonLetterSpots's strategy in order to do the rest.

class StaticStarters(AI) :
    def __init__(self, guessPool, numPools):
        self.guessNum = 0
        self.guessPools = []
        self.guessPools.append(guessPool)
        self.guessPools[0].sort(key=self.CommonLetterSpot, reverse=True)

        i = 1
        while i < numPools:
            temp = self.guessPools[0].copy()
            self.guessPools.append(temp)
            i += 1

    def pickWord(self):
        self.pickPool()
        if self.guessNum < 2:
            if len(self.poolToChooseFrom) != 1:
                self.guessNum += 1
                return self.Starters[self.guessNum-1]
        ret = self.poolToChooseFrom[0]
        self.poolToChooseFrom.remove(ret)
        return ret

    def CommonLetterSpot(self, word):
        count = 0
        multiplier = 2 # weight for the letter spots. can change, but this
                        # best so far.
        count += multiplier * self.FirstLetter[word[0]]
        count += multiplier * self.SecondLetter[word[1]]
        count += multiplier * self.ThirdLetter[word[2]]
        count += multiplier * self.FourthLetter[word[3]]
        count += multiplier * self.FifthLetter[word[4]]
        for letter in list(set(word[:5])):
            count += self.PercentageValue[letter]
        return count

    PercentageValue = {
                'a': .393, 'b': .115, 'c': .194, 'd': .160, 'e': .456,
                'f': .089, 'g': .130, 'h': .164, 'i': .280, 'j': .012,
                'k': .087, 'l': .280, 'm': .129, 'n': .238, 'o': .291,
                'p': .149, 'q': .013, 'r': .362, 's': .267, 't': .288,
                'u': .197, 'v': .064, 'w': .084, 'x': .016, 'y': .180, 'z': .015
        }

    # how common a letter is in the first spot of a word.
    FirstLetter = {
                'a': .061, 'b': .075, 'c': .086, 'd': .048, 'e': .031,
                'f': .059, 'g': .050, 'h': .030, 'i': .015, 'j': .009,
                'k': .009, 'l': .038, 'm': .046, 'n': .016, 'o': .018,
                'p': .061, 'q': .010, 'r': .045, 's': .158, 't': .064,
                'u': .014, 'v': .019, 'w': .036, 'x': 0, 'y': .003, 'z': .001
        }

    # how common a letter is in the second spot of a word.
    SecondLetter = {
                'a': .131, 'b': .007, 'c': .017, 'd': .009, 'e': .105,
                'f': .003, 'g': .005, 'h': .062, 'i': .087, 'j': .001,
                'k': .004, 'l': .087, 'm': .016, 'n': .038, 'o': .121,
                'p': .026, 'q': .002, 'r': .115, 's': .007, 't': .033,
                'u': .080, 'v': .007, 'w': .019, 'x': .006, 'y': .010, 'z': .001
        }

    # how common a letter is in the third spot of a word.
    ThirdLetter = {
                'a': .133, 'b': .025, 'c': .024, 'd': .032, 'e': .077,
                'f': .011, 'g': .029, 'h': .004, 'i': .115, 'j': .001,
                'k': .005, 'l': .048, 'm': .026, 'n': .060, 'o': .105,
                'p': .025, 'q': .001, 'r': .070, 's': .035, 't': .048,
                'u': .071, 'v': .021, 'w': .011, 'x': .005, 'y': .013, 'z': .005
        }

    # how common a letter in the fourth spot of a word.
    FourthLetter = {
                'a': .070, 'b': .010, 'c': .066, 'd': .030, 'e': .137,
                'f': .015, 'g': .033, 'h': .012, 'i': .068, 'j': .001,
                'k': .024, 'l': .070, 'm': .029, 'n': .079, 'o': .057,
                'p': .022, 'q': 0, 'r': .066, 's': .074, 't': .060,
                'u': .035, 'v': .020, 'w': .011, 'x': .001, 'y': .001, 'z': .009
        }

    # how commmon a letter is in the fifth spot of a word.
    FifthLetter = {
                'a': .028, 'b': .005, 'c': .013, 'd': .051, 'e': .183,
                'f': .011, 'g': .018, 'h': .060, 'i': .005, 'j': 0,
                'k': .049, 'l': .067, 'm': .018, 'n': .056, 'o': .025,
                'p': .024, 'q': 0, 'r': .092, 's': .016, 't': .109,
                'u': 0, 'v': 0, 'w': .007, 'x': .003, 'y': .157, 'z': .002
        }

    Starters = {
                0: "raise",
                1: "clout",
                2: "nymph",
    }


# CLASS: ENTROPY
# subclass of AI that starts with the static words but then attempts to
# make guesses based on the entropy of the guesses left, meaning how much
# they reduce the pool.
class Entropy(AI):
    def __init__(self, guessPool, numPools):
        self.guessPools = []
        self.guessPools.append(guessPool)
        self.poolToChooseFrom = self.guessPools[0]
        self.guessNum = 0


        i = 1
        while i < numPools:
            temp = self.guessPools[0].copy()
            self.guessPools.append(temp)
            i += 1

    def pickWord(self):
        self.pickPool()
        if self.guessNum < 3:
            if len(self.poolToChooseFrom) != 1:
                self.guessNum += 1
                return self.Starters[self.guessNum-1]
        if len(self.poolToChooseFrom) == 1:
            ret = self.poolToChooseFrom.pop()
            return ret
        else:
            ret = self.EntropyRating()
            self.poolToChooseFrom.remove(ret)
            return ret

    def EntropyRating(self):
        before = len(self.poolToChooseFrom)
        max = self.poolToChooseFrom[0]
        maxRating = 0

        for testWord in self.poolToChooseFrom:
            total = 0
            after = 0
            for secondWord in self.poolToChooseFrom:
                newAnswers = self.poolToChooseFrom.copy()
                newAI = AI(newAnswers, 1)
                miniGame = quordle.Quordle(newAnswers, 1)
                miniGame.answers[0] = secondWord
                hint = miniGame.evaluateGuess(testWord[:5])
                newAI.interpretHint(hint[0], testWord[:5], newAI.guessPools[0])
                after = len(newAI.guessPools[0])

                total += (before / after)
            if total > maxRating:
                maxRating = total
                max = testWord

        return max


    Starters = {
                0: "raise",
                1: "clout",
                2: "nymph",
    }

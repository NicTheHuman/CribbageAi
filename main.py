#This program will atempt to play the card game "Cribbage" at a high level maximizing points while attempting to minimize points for opponents
#Eventually the goal is for the bot to play differently dependent on the game score (taking more or less risks when needed)
import null as null

FULL_DECK = ['1S', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', '11S', '12S', '13S',
             '1D', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', '11D', '12D', '13D',
             '1C', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', '11C', '12C', '13C',
             '1H', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', '10H', '11H', '12H', '13H']

def inputHand(n):
    hand = []
    print("Eter Cards 1-by-1 in the form 1S ... 13H")
    for i in range(0,n):
        hand.append(input("New Card: "))

    return hand

def getValue(card):
    result = int(card[0:len(card)-1])
    if result < 10:
        return result
    else:
        return 10

def getSuit(card):
    return card[len(card)-1]

def valueList(hand):
    vals = []
    for card in hand:
        vals.append(getValue(card))
    return vals

def factorial(num):
    if num == 0:
        return 1
    else:
        return num*factorial(num-1)

def nChooseK(n, k):
    return factorial(n)/(factorial(k)*factorial(n-k))

def frequencyNotation(hand):
    empty = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for each in hand:
        empty[int(each[0:len(each)-1])-1] += 1

    return empty

def checkPairs(freqList):
    count = 0
    for i in freqList:
        if i > 1:
            count += nChooseK(i, 2)*2
    return count

def checkRuns(freqList):
    count = 0
    indexSinceZero = -1
    for i in range(0,13):
        if freqList[i] == 0:
            if i - indexSinceZero > 3:
                count = i - indexSinceZero - 1
                for j in range(indexSinceZero+1, i):
                    count *= freqList[j]
                break

            else:
                indexSinceZero = i
        if i == 12:
            if i - indexSinceZero + 1 > 3:
                count = i - indexSinceZero
                for j in range(indexSinceZero + 1, i):
                    count *= freqList[j]

    return count

def numTarget(vals, target, index):
    if target == 0:
        return 1
    elif target < 0 or index == len(vals):
        return 0
    else:
        return numTarget(vals, target - vals[index], index+1) + numTarget(vals, target, index+1)

def countFifteens(vals):
    vals_copy = vals[:]
    vals_copy.sort(reverse=True)
    total = sum(vals_copy)
    target = 15
    if total <= 30:
        target = total-15
    return numTarget(vals_copy, target, 0)*2

def checkKnobs(hand):
    for each in hand:
        if getValue(each) == 11 and each != hand[4] and getSuit(each) == getSuit(hand[5]):
            return 1
    return 0

def checkFlush(hand, crib):
    if getSuit(hand[0]) == getSuit(hand[1]) == getSuit(hand[2]) == getSuit(hand[3]):
        if getSuit(hand[3]) == getSuit(hand[4]):
            return 5
        elif not crib:
            return 4
    return 0


def countHand(hand, crib):
    count = 0
    freqs = frequencyNotation(hand)
    count += checkRuns(freqs)
    count += checkPairs(freqs)
    count += checkKnobs(hand)
    count += checkFlush(hand, crib)
    count += countFifteens(valueList(hand))

    return count

def addRandomCard(tempDeck, fakeHand):
    count = 0
    for card in tempDeck:
        fakestHand = fakeHand.copy()
        fakestHand.append(card)
        count += countHand(fakestHand, False)
    count /= len(tempDeck)

    return count

def averageCribScore(cards, tempDeck):
    count = 0
    for i in range(0, 44):
        for j in range(i+1, 45):
            for k in range(j+1, 46):
                fakeHand = cards.copy()
                fakeHand.append(tempDeck[i])
                fakeHand.append(tempDeck[j])
                fakeHand.append(tempDeck[k])

                count += countHand(fakeHand, True)

    return count/15180


def bestAverageThrow(hand, ownCrib):
    tempDeck = FULL_DECK.copy()
    for card in hand:
        print(card)
        tempDeck.remove(card)

    bestThrows = [[' ',' ',-30], [' ',' ',-30], [' ',' ',-30]]

    for i in range(0, 5):
        for j in range(i+1, 5):
            fakeHand = hand.copy()
            fakeHand.remove(hand[j])
            fakeHand.remove(hand[i])

            count = addRandomCard(tempDeck, fakeHand)

            if ownCrib:
                count += averageCribScore([hand[i], hand[j]], tempDeck)
            else:
                count -= averageCribScore([hand[i], hand[j]], tempDeck)

            for k in range(0,3):
                if count > bestThrows[k][2]:
                    del bestThrows[2]
                    bestThrows.insert(k, [hand[i], hand[j], count])
                    break
    print(bestThrows)

def averagePeggingScore(cards, tempDeck):
    pass

def bestThrowFourPlayer(hand):
    pass

def countPegging(played):
    pass

def pegging(cards, cardsPlayed, turn):
    if len(cardsPlayed) == 8:
        p1, p2 = countPegging(cardsPlayed)
    else:
        if turn:
            for card in cards:
                fake = cards.copy()
                fake.remove(card)
                fakePlayed = cardsPlayed.copy()
                fakePlayed.append(card)
                turn = False
                return pegging(fake, fakePlayed, turn)
        else:
            pass

#SAMPLE_HAND = inputHand(5)
SAMPLE_HAND = ['2H', '3D', '5H', '6D', '10C', '13C']

print(SAMPLE_HAND)
print(countHand(['8S', '10D', '6S', '5C'], False))

print(bestAverageThrow(SAMPLE_HAND, True))
''''
testDeck = copyCards(FULL_DECK)
testCards = ['8S', '10D', '6S', '5C']
for i in SAMPLE_HAND:
    testDeck.remove(i)

for card in testDeck:
    fakeTest = copyCards(testCards)
    fakeTest.append(card)
    print(fakeTest)
    print(countHand(fakeTest, False))
'''

import random
import itertools
from icecream import ic


class PokerPlayer:
    def __init__(self, name = "Player X", hand = [], PValue = None, score = 0):
        self.name = name
        self.hand = hand
        self.PValue = PValue

    def setHand(self, list):
        self.hand = list

    def setScore(self, value):
        self.score = value
    def aff(self):
        return [self.name, self.hand]

    def getPValue(self):
        if self.PValue == None:
            self.getCombi()
        return self.PValue

    def getCombi(self):
        global center
        allCards = self.hand + center
        allValue = sorted([i[1] for i in allCards])
        reversedValue = sorted([i[1] for i in allCards], reverse=True)
        allSign = sorted([i[2] for i in allCards])

        suiteList = []
        for nb in range(0, 3):
            if allValue[nb:nb+4] == [i + allValue[nb] for i in range(5)]:
                for card in allCards:
                    if nb <= card[1] <= nb+4:
                        suiteList.append(card)

        flushList = []
        for sign in allSign[0:3]:
            if allSign.count(sign) >= 5:
                for card in allCards:
                    if card[2] == sign:
                        flushList.append(card)

        combination = []
        done = []
        for L in range(3, 6):
            for subset in itertools.permutations(reversedValue, 7 - L):
                if subset.count(subset[0]) == len(subset) and subset not in combination and subset[0] not in done:
                    combination.append(subset)
                    done.append(subset[0])
        if len(combination) <= 1:
            combination.append([])
        ic(combination)

        # interpréter les résultats de la liste combination
        combi = tuple
        for elem in combination:
            if len(combination[0]) == 4:
                count = 5
                for k in combination[0]:
                    if k in reversedValue:
                        reversedValue.remove(k)
                combi = combination[0], reversedValue[0]
            elif len(combination[0]) == 3:
                if len(combination[1]) in [2, 3]:
                    count = 4
                    combi = combination[0], [combination[1][0:2]]
                else:
                    count = 3
                    for k in combination[0]:
                        if k in reversedValue:
                            reversedValue.remove(k)
                    combi = combination[0], reversedValue[0:2]
            elif len(combination[0]) == 2:
                if len(combination[1]) == 2:
                    count = 2
                    for k in combination[0]:
                            if k in reversedValue:
                                reversedValue.remove(k)
                    for k in combination[1]:
                            if k in reversedValue:
                                reversedValue.remove(k)
                    combi = combination[0], combination[1], [reversedValue[0]]
                else:
                    count = 1
                    for k in combination[0]:
                        if k in reversedValue:
                            reversedValue.remove(k)
                    combi = combination[0], reversedValue[0:3]
            else:
                count = 0
                combi = reversedValue[0:5],

        list = []
        for elem in combi:
            for elem2 in elem:
                list.append(elem2)
        combi = list

        if flushList in suiteList or suiteList in flushList:
            self.PValue = 8, ([k for k in flushList if k in suiteList],)
        elif count == 5:
            self.PValue = 7, combi
        elif count == 4:
            self.PValue = 6, combi
        elif flushList != []:
            self.PValue = 5, (flushList[0:5],)
        elif suiteList != []:
            self.PValue = 4, (suiteList[0:5],)
        elif count == 3:
            self.PValue = 3, combi
        elif count == 2:
            self.PValue = 2, combi
        elif count == 1:
            self.PValue = 1, combi
        elif count == 0:
            self.PValue = 0, combi


def getDeck():
    deck = []
    for sign in ['coeur', 'trefle',  'pic', 'carreau']:
        nbValue = 2
        for value in ['deux', 'trois', 'quatre', 'cinq', 'six','sept','huit', 'neuf',  'dix',  'valet',  'dame',  'roi', 'AS']:
            deck.append((f"{value} de {sign}", nbValue, sign))
            nbValue += 1
        random.shuffle(deck)
    return deck

def piocher(deck):
    print(deck[0][0])
    del deck[0]

def afficher(card):
    print(card[0])

def comparer(playerList):
    for player in playerList:
        player.setScore(0)
        for player2 in playerList:
            if player != player2:
                if player.getPValue()[0] == player2.getPValue()[0]:
                    for n in range(5):
                        if player.getPValue()[1][n] > player2.getPValue()[1][n]:
                            player.setScore(player.score + 1)
                            break
                elif player.getPValue()[0] > player2.getPValue()[0]:
                    player.setScore(player.score + 1)
    playerScore = [player.score for player in playerList]
    players = {player.score : player for player in playerList}
    return players[max(playerScore)]

def splitPlayer(deck, nb):
    # Deck is a list defined by the function getDeck
    # nb is the number of deck of cards you want to split on the initial deck
    splittedDeck = []
    nbSplit = len(deck)//nb
    while len(splittedDeck) != nb:
        splittedDeck.append(deck[0:nbSplit])
        del(deck[0:nbSplit])

    return splittedDeck, deck

def splitCards(deck, nbCards, nbDeck = 52):
    # Deck is a list defined by the function getDeck
    # nb is the number of cards you want in each deck
    splittedDeck = []
    while len(deck) >= nbCards or len(splittedDeck) <= nbDeck:
        splittedDeck.append(deck[0:nbCards])
        del(deck[0:nbCards])
    return splittedDeck, deck


def poker(deck, nbPlayer):
    PlayerList = []
    global center

    if len(deck) - 5 < nbPlayer * 2:
        print("Trop de joueurs pour un deck de " + str(len(deck)) + " cartes.")
        return

    for n in range(nbPlayer):
        name = input("Nom du Joueur "+str(n+1))
        hand = deck[0:2]
        del(deck[0:2])
        PlayerList.append(PokerPlayer(name, hand))
    center = deck[0:5]

    ic(comparer(PlayerList).name)

poker(getDeck(), 3)
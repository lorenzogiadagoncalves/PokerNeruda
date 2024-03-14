import random
import itertools
import pygame
import sys
import time
from screeninfo import get_monitors
from icecream import ic


class PokerPlayer:
    def __init__(self, name="Unnammed Player", hand=[], PValue=None, score=0, bet=1000, roundBet=0):
        self.name = name
        self.hand = hand
        self.PValue = PValue
        self.score = score
        self.bet = bet
        self.roundBet = roundBet

    def setHand(self, list):
        self.hand = list

    def setScore(self, value):
        self.score = value

    def aff(self):
        return [self.name, self.hand]

    def getPValue(self, center):
        self.getCombi(center)
        return self.PValue

    def getCombi(self, center):
        allCards = self.hand + center
        allValue = sorted([i[1] for i in allCards])
        reversedValue = sorted([i[1] for i in allCards], reverse=True)
        allSign = sorted([i[2] for i in allCards])

        suiteList = []
        for nb in range(0, 3):
            if allValue[nb:nb + 4] == [i + allValue[nb] for i in range(5)]:
                for card in allCards:
                    if nb <= card[1] <= nb + 4:
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

        # interpréter les résultats de la liste combination
        combi = tuple
        for elem in combination:
            if len(combination[0]) == 4:
                count = 5
                for k in combination[0]:
                    if k in reversedValue:
                        reversedValue.remove(k)
                combi = combination[0], [reversedValue[0]]
            elif len(combination[0]) == 3:
                if len(combination[1]) in [2, 3]:
                    count = 4
                    combi = combination[0], combination[1][0:2]
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
            self.PValue = (8, ([k for k in flushList if k in suiteList],))
        elif count == 5:
            self.PValue = (7, combi)
        elif count == 4:
            self.PValue = (6, combi)
        elif flushList != []:
            self.PValue = (5, (flushList[0:5],))
        elif suiteList != []:
            self.PValue = (4, (suiteList[0:5],))
        elif count == 3:
            self.PValue = (3, combi)
        elif count == 2:
            self.PValue = (2, combi)
        elif count == 1:
            self.PValue = (1, combi)
        elif count == 0:
            self.PValue = (0, combi)

    def paris(self, amount):
        global pot
        if self.bet >= amount:
            self.bet -= amount
            self.roundBet += amount
            pot += amount


def comportementBot(bot):
    random.randint


def getDeck():
    deck = []
    for sign in ['coeur', 'trefle', 'pique', 'carreau']:
        nbValue = 2
        for value in ['02', '03', '04', '05', '06', '07', '08', '09', '10', 'V', 'D', 'R',
                      '01']:
            deck.append((rf"cards\{value}-{sign}\{value}-{sign}-1.png", nbValue, sign))
            nbValue += 1
        random.shuffle(deck)
    return deck


def comparer(playerList, center):
    for player in playerList:
        player.setScore(0)
        for player2 in playerList:
            if player != player2:
                if player.getPValue(center)[0] == player2.getPValue(center)[0]:
                    for n in range(len(player.getPValue(center)[1])):
                        if player.getPValue(center)[1][n] > player2.getPValue(center)[1][n]:
                            player.setScore(player.score + 1)
                            break
                elif player.getPValue(center)[0] > player2.getPValue(center)[0]:
                    player.setScore(player.score + 1)
    playerScore = [player.score for player in playerList]
    players = {player.score: player for player in playerList}
    return players[max(playerScore)]


def splitPlayer(deck, nb):
    # Deck is a list defined by the function getDeck
    # nb is the number of deck of cards you want to split on the initial deck
    splittedDeck = []
    nbSplit = len(deck) // nb
    while len(splittedDeck) != nb:
        splittedDeck.append(deck[0:nbSplit])
        del (deck[0:nbSplit])

    return splittedDeck, deck


def splitCards(deck, nbCards, nbDeck=52):
    # Deck is a list defined by the function getDeck
    # nb is the number of cards you want in each deck
    splittedDeck = []
    while len(deck) >= nbCards or len(splittedDeck) <= nbDeck:
        splittedDeck.append(deck[0:nbCards])
        del (deck[0:nbCards])
    return splittedDeck, deck


def round(playerList):
    global pot, mainPlayer, CardPosList, c, deck, center, button
    deck = getDeck()
    center = deck[0:5]
    del (deck[0:5])
    pot = 0
    c = 3
    for player in playerList:
        ic(player.name, player.bet)
        player.setHand(deck[0:2])
        del (deck[0:2])

    if len(playerList) > 1:
        display()

        button += 1
        petiteBlinde = playerList[(button+1)%len(playerList)]
        grosseBlinde = playerList[(button+2)%len(playerList)]
        petiteBlinde.paris(10)
        grosseBlinde.paris(20)

        loop = True
        while loop:
            ValueList = [k.roundBet for k in playerList]
            while True:
                for player in playerList:
                    while True:
                        if player == mainPlayer:
                            value = int(textBox(
                                f"Combien voulez vous ajouter à votre mise ? ",
                                type="numbers"))
                            if value <= player.bet and player.roundBet >= min(ValueList):
                                player.paris(value)
                                break
                        else:
                            player.paris(max(ValueList)-player.roundBet)
                            break
                ValueList = [k.roundBet for k in playerList]
                if max(ValueList) == min(ValueList):
                    break
            if c == 5:
                loop = False
            else:
                c += 1
            for p in playerList:
                p.roundBet = 0

        roundWinner = comparer(playerList, center)
        roundWinner.bet += pot
        display(winner=roundWinner)
        NewPlayerList = []
        for player in playerList:
            if player.bet != 0:
                NewPlayerList.append(player)
        playerList = NewPlayerList
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        round(playerList)

    else:
        winner = playerList[0]
        print(f"Winner: {winner.name} !")

        poker(6)


def poker(nbPlayer):
    global pot, playerList, mainPlayer, button
    playerList = []
    pot = 0
    button = random.randint(1, 6)


    if 47 < nbPlayer * 2:
        print("Trop de joueurs pour un deck de 52 cartes.")
        return


    mainPlayer = PokerPlayer(NameBox())
    playerList.append(mainPlayer)
    nameList = getBotNames(nbPlayer - 1)
    for n in range(nbPlayer - 1):
        playerList.append(PokerPlayer(nameList[n]))
    round(playerList)

def imageCard(path, co=(0, 0)):
    global CardResize
    image = pygame.image.load(path)
    Simage = pygame.transform.scale(image, (378 / CardResize, 545 / CardResize))
    screen.blit(Simage, co)


def fillScreen(path):
    img = pygame.image.load(path)
    img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(img, (0, 0))


def textBox(text="", type="text"):
    global playerList
    user_text = ""
    a = ""
    while a == "":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    if event.key == pygame.K_RETURN:
                        a = user_text
                    else:
                        if type == "numbers":
                            user_text = user_text + event.unicode if str(event.unicode).isdigit() and len(user_text) <= 8 else user_text
                        else:
                            user_text += event.unicode

        display(False)
        Title_surface = base_font.render(text, True, (255, 255, 255))
        text_rect = Title_surface.get_rect(topright=(SCREEN_WIDTH * 9 / 10, SCREEN_HEIGHT * 9 / 10 + 8))
        screen.blit(Title_surface, text_rect)

        input_rect = pygame.Rect(SCREEN_WIDTH * 9 / 10, SCREEN_HEIGHT * 9 / 10, 140, 32)
        pygame.draw.rect(screen, (0, 0, 0), input_rect)
        text_surface = base_font.render(user_text, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        pygame.display.flip()
        pygame.display.update()
    return a

def display(update = True, winner = None ):
    global mainPlayer, center, c, deck, playerList, betposList, pot, button

    nonPlayerList = [k for k in playerList if k != mainPlayer]

    fillScreen(r"planks.jpg")
    fillScreen(r"pokerTable.png")


    totalRoundBet = sum(k.roundBet for k in playerList)
    pot_surface = base_font.render(str(pot - totalRoundBet), True, (255, 0, 0))
    pot_rect = pot_surface.get_rect(
        center=(SCREEN_WIDTH/2, 5 * SCREEN_HEIGHT/16))
    screen.blit(pot_surface, pot_rect)

    mainName = mainPlayer.name
    mainName_surface = base_font.render(mainName, True, (255, 255, 255))
    mainName_rect = mainName_surface.get_rect(
        center=(betPosList[0][0] * SCREEN_WIDTH, (betPosList[0][1] + 9/100) * SCREEN_HEIGHT))
    screen.blit(mainName_surface, mainName_rect)

    for n in range(2):
        imageCard(mainPlayer.hand[n][0], CardPosList[0][n])

    if winner != None:
        pList = [i for i in playerList if i != mainPlayer]
        for i in range(0, len(playerList) - 1):
            imageCard(pList[i].hand[0][0], co=CardPosList[1::][i][0])
            imageCard(pList[i].hand[1][0], co=CardPosList[1::][i][1])
        pot_surface = base_font.render(f"{winner.name} vient de remporter {pot} jetons", True, (0, 0, 0))
        pot_rect = pot_surface.get_rect(
            center=(SCREEN_WIDTH / 2, 9 * SCREEN_HEIGHT / 16))
        screen.blit(pot_surface, pot_rect)

    else:
        for pos in CardPosList[1:len(playerList)]:
            imageCard(r"dos-bleu.png", co=pos[0])
            imageCard(r"dos-bleu.png", co=pos[1])

    mainPlayerBet = str(mainPlayer.bet)
    mainPlayerBet_surface = base_font.render(mainPlayerBet, True, (255, 255, 0))
    mainPlayerBet_rect = mainPlayerBet_surface.get_rect(
        center=(betPosList[0][0] * SCREEN_WIDTH, betPosList[0][1] * SCREEN_HEIGHT))
    screen.blit(mainPlayerBet_surface, mainPlayerBet_rect)

    mainPlayerRoundBet = str(mainPlayer.roundBet)
    mainPlayerRoundBet_surface = base_font.render(mainPlayerRoundBet, True, (173,216,230))
    mainPlayerRoundBet_rect = mainPlayerRoundBet_surface.get_rect(
        center=(RoundBetPosList[0][0] * SCREEN_WIDTH, RoundBetPosList[0][1] * SCREEN_HEIGHT))
    screen.blit(mainPlayerRoundBet_surface, mainPlayerRoundBet_rect)

    for pos in MidCardPosList:
        imageCard(r"dos-bleu.png", co=pos)
    for i in range(len(center[0:c])):
        imageCard(deck[i][0], co=MidCardPosList[i])
    for i in range(0, 5 - c):
        imageCard(r"dos-bleu.png", MidCardPosList[-1 - i])

    for n in range(len(nonPlayerList)):
        text = str(nonPlayerList[n].bet)
        Title_surface = base_font.render(text, True, (255, 255, 0))
        text_rect = Title_surface.get_rect(center=(betPosList[1::][n][0]*SCREEN_WIDTH, betPosList[1::][n][1]*SCREEN_HEIGHT))
        screen.blit(Title_surface, text_rect)

        playerRoundBet = str(nonPlayerList[n].roundBet)
        playerRoundBet_surface = base_font.render(playerRoundBet, True, (173, 216, 230))
        playerRoundBet_rect = playerRoundBet_surface.get_rect(
            center=(RoundBetPosList[1::][n][0] * SCREEN_WIDTH, RoundBetPosList[1::][n][1] * SCREEN_HEIGHT))
        screen.blit(playerRoundBet_surface, playerRoundBet_rect)

        name = nonPlayerList[n].name
        name_surface = base_font.render(name, True, (255, 255, 255))
        name_rect = name_surface.get_rect(
            center=(betPosList[1::][n][0] * SCREEN_WIDTH, (betPosList[1::][n][1] + 7 / 100) * SCREEN_HEIGHT))
        screen.blit(name_surface, name_rect)

    for n in range(len(playerList)):
        if button == n:
            dealer = pygame.image.load(r"dealer.png")
            Sdealer = pygame.transform.scale(dealer, (50, 50))
            playerNameSurface = base_font.render(playerList[n].name, True, (255, 255, 255))
            screen.blit(Sdealer, (betPosList[n][0]*SCREEN_WIDTH + playerNameSurface.get_width()/2 + 5, betPosList[n][1]*SCREEN_HEIGHT + playerNameSurface.get_width()))

    if update:
        pygame.display.flip()
        pygame.display.update()


def NameBox():
    global playerList
    user_text = ""
    a = ""
    longueur = 400
    largeur = 60
    while a == "":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    a = user_text
                else:
                    if base_font.size(user_text)[0] < longueur - 20:
                        user_text += event.unicode

        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)))
        img = pygame.image.load(r"logo.png")
        screen.blit(img, (SCREEN_WIDTH / 2 - img.get_width() / 2, SCREEN_HEIGHT / 10))
        text = "Quel est votre nom d'utilisateur ?"
        Title_surface = base_font.render(text, True, (0, 0, 0))
        text_rect = Title_surface.get_rect(center=(SCREEN_WIDTH / 2, 2 * SCREEN_HEIGHT / 3 - largeur))
        screen.blit(Title_surface, text_rect)

        input_rect = pygame.Rect(SCREEN_WIDTH / 2 - longueur / 2, 2 * SCREEN_HEIGHT / 3 - largeur / 2, longueur,
                                 largeur)
        pygame.draw.rect(screen, (0, 0, 0), input_rect, 5)
        text_surface = base_font.render(user_text, True, (0, 0, 0))
        screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))
        pygame.display.flip()
        pygame.display.update()
    return a

def getBotNames(n):
    nameList = list("Marie Jeanne Françoise Catherine Monique Isabelle Jacqueline Sylvie Anne Martine Madeline Nicole Suzanne Hélène Christine Louise Margueritte Denise Christiane Jean Pierre Michel André Philippe Louis Réné Alain Jaques Bernard Marcel Daniel Roger Paul Robert Claude Henri Christian Nicolas Georges".split(" "))
    random.shuffle(nameList)
    return nameList[0:n]
pygame.init()

screen = get_monitors()[0]
SCREEN_WIDTH = screen.width
SCREEN_HEIGHT = screen.height

TEXTBOX_WIDTH = 200
TEXTBOX_HEIGHT = 50

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
base_font = pygame.font.Font(None, 32)

CardResize = 3
CardPosList = (((SCREEN_WIDTH / 2 - 378 / CardResize, 3 * SCREEN_HEIGHT / 4 - 545 / CardResize),
                (SCREEN_WIDTH / 2, 3 * SCREEN_HEIGHT / 4 - 545 / CardResize)),
               ((SCREEN_WIDTH / 2 - 378 / CardResize, 18*SCREEN_HEIGHT / 64 - 545 / CardResize),
                (SCREEN_WIDTH / 2, 18*SCREEN_HEIGHT / 64 - 545 / CardResize)),
               ((SCREEN_WIDTH / 6 - 378 / CardResize, 2 * SCREEN_HEIGHT / 3 - 545 / CardResize),
                (SCREEN_WIDTH / 6 - 378 / 1.5 / CardResize, 2 * SCREEN_HEIGHT / 3 - 545 / CardResize - 20)),
               ((SCREEN_WIDTH / 6 - 378 / CardResize, 4 * SCREEN_HEIGHT / 9 - 545 / CardResize),
                (SCREEN_WIDTH / 6 - 378 / 1.5 / CardResize, 4 * SCREEN_HEIGHT / 9 - 545 / CardResize + 20)),
               ((4 * SCREEN_WIDTH / 5 + 378 / CardResize, 2 * SCREEN_HEIGHT / 3 - 545 / CardResize),
                (4 * SCREEN_WIDTH / 5 + 378 / 1.5 / CardResize, 2 * SCREEN_HEIGHT / 3 - 545 / CardResize - 20)),
               ((4 * SCREEN_WIDTH / 5 + 378 / CardResize, 4 * SCREEN_HEIGHT / 9 - 545 / CardResize),
                (4 * SCREEN_WIDTH / 5 + 378 / 1.5 / CardResize, 4 * SCREEN_HEIGHT / 9 - 545 / CardResize + 20)))

betPosList = [(49/100, 81/100), (7/100, 73/100), (11/100, 9/100), (49/100, 3/100), (87/100, 9/100), (93/100, 73/100)]

MidCardPosList = (
    (SCREEN_WIDTH / 2 - 378 / (2 * CardResize) - 2 * 378 / CardResize, SCREEN_HEIGHT / 3),
    (SCREEN_WIDTH / 2 - 378 / (2 * CardResize) - 378 / CardResize, SCREEN_HEIGHT / 3),
    (SCREEN_WIDTH / 2 - 378 / (2 * CardResize), SCREEN_HEIGHT / 3),
    (SCREEN_WIDTH / 2 - 378 / (2 * CardResize) + 378 / CardResize, SCREEN_HEIGHT / 3),
    (SCREEN_WIDTH / 2 - 378 / (2 * CardResize) + 2 * 378 / CardResize, SCREEN_HEIGHT / 3)
)

RoundBetPosList = ((59 / 100, 68 / 100), (21 / 100, 55 / 100), (21 / 100, 33 / 100), (40 / 100, 22 / 100), (80 / 100, 33 / 100), (80 / 100, 55 / 100))


run = True

poker(6)
pygame.quit()

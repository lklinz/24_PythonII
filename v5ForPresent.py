import random
import subprocess
import sys
from colorama import Fore
turns = 0
move = 0
deck = [ "AS","AD","AC","AH","2D","3D","4D","5D","6D","7D","8D","9D","10D","JD","QD","KD","2S","3S","4S","5S","6S","7S","8S","9S","10S","JS","QS","KS","2C","3C","4C","5C","6C","7C","8C","9C","10C","JC","QC","KC","2H","3H","4H","5H","6H","7H","8H","9H","10H","JH","QH","KH"]
def DealingCards():
    random.shuffle(deck)
    player1 = []
    player2 = []
    attackingCards = []
    defendingCards = []
    tableCards=[]
    for i in range(8):
        player1.append(deck.pop())
        player2.append(deck.pop())
    trumpSuit = deck.pop()
    deck.append(trumpSuit)
    suits = {
        'S': 'Spade',
        'C': 'Club',
        'D': 'Diamond',
        'H': 'Heart'
    }
    theValue={
        '1':10,
        '2':2,
        '3':3,
        '4':4,
        '5':5,
        '6':6,
        '7':7,
        '8':8,
        '9':9,
        'J': 11,
        'Q': 12,
        'K': 13,
        'A': 14
    }
    return player1, player2, deck, trumpSuit,theValue,suits,attackingCards,defendingCards,tableCards

#v5
def visualForCards():
    with open('cards.txt') as textFile:
        visualOfCards = textFile.read().splitlines()
    visual = {}
    place = 0
    for card in deck:
        aCard = []
        for line in range(place,place+6):
            aCard.append(visualOfCards[line])
        place += 6
        visual[card] = aCard
    for key in visual.keys():
        if 'H' in key:
            for i in range(6):
                visual[key][i]=Fore.RED+visual[key][i]+Fore.RESET
        if 'D' in key:
            for i in range(6):
                visual[key][i]=Fore.RED+visual[key][i]+Fore.RESET
    return visual
visual = visualForCards()

def printhand():
    for j in range(6):
        handvisual = ""
        if move%2==0:
            for card in player1:
                if card in visual.keys():
                    handvisual+=visual[card][j]
        elif move%2==1:
            for card in player2:
                if card in visual.keys():
                    handvisual+=visual[card][j]
        print(handvisual)
    return ""

# v0
def printBoardTable(defendingCards,attackingCards,suits,trumpSuit, move,player1,player2):
    subprocess.run('cls', shell=True)
    print('|                                                                                   |')
    print(f'|The trump suit is {suits[trumpSuit[-1]]}                                                         |')                                                                            
    print('|                                                                                   |')
    print(f'|Attacking Cards: {attackingCards}|')
    print(f'|Defending Cards: {defendingCards}|')
    print('|                                                                                   |')
    print('|                                                                                   |')
    if move % 2 == 0:
        print(f"|{player1}{printhand()}                              |")
    elif move%2==1:
        print(f"|{player2}{printhand()}")    

#v3
def Draw():
    if len(deck) > 0:
        for card in deck:
            if len(player1) <8:
                player1.append(card)
                deck.remove(card)
        for card in deck:    
            if len(player2)<8:
                player2.append(card)
                deck.remove(card)


# v2:
def isValidAttackCard(attackCard):
    isValid = False
    if len(attackingCards) == 0:
        isValid = True
    elif len(attackingCards)>0:
        for card in attackingCards:
            if attackCard[0] == card[0]:
                isValid = True
        for card in defendingCards:
            if attackCard[0] == card[0]:
                isValid = True
    return isValid

def ScanAttack(player,turns):
    attackCard = ''
    while attackCard != 'q' and (attackCard not in player or not isValidAttackCard(attackCard)):
        attackCard = input('Play a card to attack: ')
    if attackCard == 'q':
        turns += 1
        del attackingCards[0:len(attackingCards)+1]
        del defendingCards[0:len(defendingCards)+1]
        Draw()
        print('Next attacking turn:')
    else:
        player.remove(attackCard)
        attackingCards.append(attackCard)
    return attackCard,turns

def DeterMineAttacker(turns,move):
    attackerChoice = ''
    while attackerChoice != 'q' and attackerChoice != 'a':
        attackerChoice = input('Enter (a)ttack or (q)uit: ')
    if attackerChoice == 'q':
        turns += 1
        del attackingCards[0:len(attackingCards)+1]
        del defendingCards[0:len(defendingCards)+1]
        attackCard = ''
        Draw()
        print('Next attacking turn:')
    elif attackerChoice == 'a':
        if turns %2 == 0:
            attackCard,turns= ScanAttack(player1,turns)
        elif turns %2 ==1:
            attackCard,turns = ScanAttack(player2,turns)
    move += 1
    return attackCard,turns,move,attackerChoice 

def isValidDefendCard(attackCard,defendCard):
    defendSuit = defendCard[-1]
    attackSuit = attackCard[-1]
    if theValue[defendCard[0]]>theValue[attackCard[0]] and defendSuit == attackSuit:
        isValid = True
    elif defendSuit == trumpSuit[-1] and attackSuit != trumpSuit[-1]:
        isValid = True
    else:
        isValid = False
    return isValid
        
def ScanDefenderCard(player,turns):
    defendCard = ''
    while defendCard != 'q' and (defendCard not in player or not isValidDefendCard(attackCard,defendCard)): 
        defendCard = input('Play a card to defend: ')
    if defendCard == 'q':
        turns += 2
        nextAttackingTurn()
        print('Next attacking turn:')
    else:
        defendingCards.append(defendCard)
        player.remove(defendCard)
    return defendCard,turns

#v3
def nextAttackingTurn():
    tableCards.extend(attackingCards)
    tableCards.extend(defendingCards)
    if turns % 2 == 0:
        player2.extend(tableCards)
    elif turns % 2 == 1:
        player1.extend(tableCards)
    del attackingCards[0:len(attackingCards)+1]
    del defendingCards[0:len(defendingCards)+1]
    del tableCards[0:len(tableCards)+1]
    Draw()          
#v2
def deterMineDefender(turns,move):
    defenderChoice = ''
    while defenderChoice != 'q' and defenderChoice != 'd':
        defenderChoice = input('Enter (d)efending or (q)uit: ')
    if defenderChoice == 'q':
        turns += 2
        nextAttackingTurn()
        print('Next attacking turn:')
    elif defenderChoice == 'd':
        if turns % 2 == 0:
            ScanDefenderCard(player2,turns)
        elif turns % 2 == 1:
            ScanDefenderCard(player1,turns)
    move +=1
    return turns,move,defenderChoice

#v4
def determineWinner():
    if len(deck)==0:
        if turns%2==0 and len(player2)==0:
            print("The winner is Player 2!") #player2 is defender, deck is empty
            return False
        elif turns%2==1 and len(player1)==0:
            print("The winner is Player 1!") #player1 is defender, deck is empty
            return False
    if turns%2==0:
        if len(player1)==0:
            print("The winner is Player 1!") #player 1 is attacker and runs out of cards and wins
            return False
        elif len(player2)==0 and attackerChoice=='q':
            print("The winner is Player 2!") #player2 is defender, player2 wins if attacker quits and their hand is empty
            return False
    elif turns%2==1:
        if len(player2)==0:
            print("The winner is Player 2!") #player2 is attacker and wins when hand is empty
            return False
        elif len(player1)==0 and attackerChoice == 'q':
            print("The winner is Player 1!") #player1 is defender and wins if their hand is empty and if attacker quits
            return False
   


#v5
userChoice = ''
while userChoice != 'q':
    userChoice = input('(q)uit or (p)lay: ' )
    if userChoice == 'q':
        sys.exit()
    player1, player2, deck, trumpSuit,theValue,suits,attackingCards,defendingCards,tableCards = DealingCards()
    printBoardTable(defendingCards,attackingCards,suits, trumpSuit,move,player1,player2)
    while determineWinner()!=False:
        attackCard,turns,move,attackerChoice = DeterMineAttacker(turns,move)
        if determineWinner() == False:
            break      
        if attackerChoice == 'q':
            printBoardTable(defendingCards,attackingCards,suits, trumpSuit,move,player1,player2)
            continue
        if attackCard == 'q':
            printBoardTable(defendingCards,attackingCards,suits, trumpSuit,move,player1,player2)
            continue
        printBoardTable(defendingCards,attackingCards,suits, trumpSuit,move,player1,player2)
        turns,move,defenderChoice = deterMineDefender(turns,move)
        if determineWinner() == False:
            break
        printBoardTable(defendingCards,attackingCards,suits, trumpSuit,move,player1,player2)    
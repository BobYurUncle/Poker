"""
Classes:
  - river (deck, cards)
      what cards are in the river
      get cards from deck
  - deck (cards)
      what cards are in the deck (and which ones are given out)
      giving out cards
  - dealer (driver class): (Everything)
      pot
      check who's winner at end
  - players: (deck, cards)
      actions:
        - call
        - raise
        - fold
      hand
      money
  - specific cards: (Nothing)
      suite
      number
      in the case of no one having a viable hand, take into account which hands are more valuable (number first suite next) (spade (4) > hearts (3) > diamonds (2) > clubs (1))


Working Order:
Cards/
Deck/
River/
players/
Dealer/
"""
#suites go from 1-4
#numbers go from 2-14

import random
import pdb

class SpecificCards:
  def __init__(self, cardNumber, suiteValue):
    self.cardNum = cardNumber
    self.suites = suiteValue
    
  def PrintCards(self):
    if self.cardNum == 11:
      cardNumberPrint = "Jack"
    elif self.cardNum == 12:
      cardNumberPrint = "Queen"
    elif self.cardNum == 13:
      cardNumberPrint = "King"
    elif self.cardNum == 14:
      cardNumberPrint = "Ace"
    else:
      cardNumberPrint = str(self.cardNum)
    if self.suites == 1:
      suiteValuePrint = "Clubs"
    elif self.suites == 2:
      suiteValuePrint = "Diamonds"
    elif self.suites == 3:
      suiteValuePrint = "Hearts"
    elif self.suites == 4:
      suiteValuePrint = "Spades"
    print(cardNumberPrint + " of " + suiteValuePrint)

  def __gt__(self, other):
    if self.cardNum > other.cardNum:
      return True
    elif self.cardNum < other.cardNum:
      return False
    else:
      if self.suites > other.suites:
        return True
      elif self.suites < other.suites:
        return False

  def __lt__(self, other):
    if self.cardNum < other.cardNum:
      return True
    elif self.cardNum > other.cardNum:
      return False
    else:
      if self.suites < other.suites:
        return True
      elif self.suites > other.suites:
        return False 

  def GetCardInfo(self):
    return self.cardNum, self.suites


class Deck:
  def __init__(self):
    self.cardsGivenOut = []

  def GetRandomCard(self):
    rs, rn = self.RandomlyCreateCardInfo()
    self.cardsGivenOut.append(str(rs) + str(rn))
    return SpecificCards(rn, rs)

  def RandomlyCreateCardInfo(self):
    alreadyGiven = False
    randomSuite = random.randint(1,4)
    randomNumber = random.randint(2,14)
    for x in self.cardsGivenOut:
      if x == str(randomSuite) + str(randomNumber):
        alreadyGiven = True
    if alreadyGiven == True:
      randomSuite, randomNumber = self.RandomlyCreateCardInfo()
      return randomSuite, randomNumber
    else:
      return randomSuite, randomNumber

  def Clear(self):
    self.cardsGivenOut = []


class River:
  def __init__(self):
    self.riverCards = []
  """
  Inputs: A card object
  Outputs: None
  Description: Adds a card to the river
  """
  def RiverAdd(self, card):
    self.riverCards.append(card)

  def RiverPrint(self):
    print("\nRiver:")
    for x in self.riverCards:
      x.PrintCards()

  def RiverClear(self):
    self.riverCards = []

  
class Player:
  def __init__(self):
    self.money = 10
    self.hand = []
    self.score = 1

  def Raise(self, highestBet):
    properlyRaised = False 
    while properlyRaised == False:
      raiseAmount = int(input("How much money would you like to put in? "))
      if self.money < raiseAmount:
        print("You don't have that amount of money!")
      else:
        if raiseAmount >= highestBet:
          self.money -= raiseAmount
          properlyRaised = True
        else:
          print("You must meet the current highest bet of " + str(highestBet))
    return raiseAmount

  def SetHand(self, card, card2):
    self.hand.append(card2)
    self.hand.append(card)

  def AddMoney(self,amount):
    self.money += amount

  def ClearMoney(self):
    self.money = 0

  def ClearForNewGame(self):
    self.hand = []
    self.score = 1

  def PrintHand(self):
    print("You have " + str(self.money) + " dollars")
    for x in self.hand:
      x.PrintCards()

  def GetHand(self):
    return self.hand


class Dealer():
  def __init__(self):
    self.pot = 0
    self.playerList = []
    self.river = River()
    self.deck = Deck()
    self.skipIndices = set()

  def StartGame(self):
    amountPlayers = 0
    while not (amountPlayers > 1 and amountPlayers < 4):
      amountPlayers = int(input("How many players want to play? "))
    #how many players are allowed to play?
      if not (amountPlayers > 1 and amountPlayers < 4):
        print("That is not a viable number.")
    for x in range(amountPlayers):
      self.playerList.append(Player())
    self.PlayGame()

  def PlayGame(self):
    print("\n-Poker-")
    minimumBet = 1
    #gives each player a random starting hand (2 cards to start off with)
    for x in self.playerList:
      x.SetHand(self.deck.GetRandomCard(), self.deck.GetRandomCard())
    #betting happens
    self.PlayerBetting(minimumBet, False, -1)
    #add more cards to river (3 cards)
    for x in range(3):
      self.river.RiverAdd(self.deck.GetRandomCard())
    self.river.RiverPrint()
    #more betting
    self.PlayerBetting(0, True, -1)
    #add more cards to river (2 cards)
    for x in range(2):
      self.river.RiverAdd(self.deck.GetRandomCard())
    #more betting
    self.PlayerBetting(0, True, -1)
    #if everyone folded, otherwise someone wins
    if self.AllFold():
      print("\nEveryone folded, no one wins.")
    else:
      #win
      winIndex = self.WinnerCheck()
      self.playerList[winIndex].money += self.pot
      self.pot = 0
      print("\nPlayer " + str(winIndex + 1) + " wins!")
    #play again
    keepPlaying = 1
    while keepPlaying != "Yes" and keepPlaying != "No":
      keepPlaying = input("Would you like to play again? Please answer with either yes or no. ")
      if keepPlaying == "yes":
        for x in self.playerList:
          x.ClearForNewGame()
        self.river.RiverClear()
        self.deck.Clear()
        self.skipIndices = set()
        self.PlayGame()
      elif keepPlaying == "no":
        print("Ok.")
        return
      else:
        print("That is not a viable response.")

  def PlayerBetting(self, initialBidLimit, raisable, skipIndex):
    skipCount = -1
    for x in self.playerList:
      skipCount += 1
      correctAction = False
      #repeatedly asks each person until their answer (and any subsequent answers created by their answer) are correctly answered
      while correctAction == False and skipCount != skipIndex and not skipCount in self.skipIndices and not self.AllFold():
        if raisable == False:
          print("\nPlayer " + str(skipCount + 1))
          x.PrintHand()
          action = input("Would you like to check or fold? ")
        else:
          #only one person can raise per round
          skipIndex = skipCount
          print("\nPlayer " + str(skipCount + 1))
          x.PrintHand()
          action = input("Would you like to check, raise, or fold? ")
          if action == "raise":
            playerBet = x.Raise(initialBidLimit)
            self.pot += playerBet
            print("You have raised.")
            self.PlayerBetting(playerBet, False, skipIndex)
            return
        if action == "check":
          x.AddMoney(initialBidLimit * -1)
          self.pot += initialBidLimit
          print("You have checked")
          correctAction = True
        elif action == "fold":
          print("You have folded.")
          #once someone folds
          if self.AllFold():
            return
          correctAction = True
          self.skipIndices.add(skipCount)
        else:
          print("That's not a viable action.") 

  def AllFold(self):
    #if the amount of players is the same with the amount of people that folded, then everyone should've folded and no one wins
    return len(self.playerList) == len(self.skipIndices)
      
  def WinnerCheck(self):
    #does the various checks on each player, whilst also comparing them to the tracked player with the "best hand"
    winningPlayerIndex = 0
    winningPlayerScore = 0
    index = 0
    for x in self.playerList:
      combinedDeck = x.GetHand() + self.river.riverCards
      inOrder, firstInSequence, firstInSameSuite, sameSuite, numberTrips, numberPairs, fourKind = self.Check(combinedDeck)
      if self.RoyalFlush(firstInSequence, inOrder, firstInSameSuite, sameSuite):
        x.score = 9
      elif self.StraightFlush(inOrder, sameSuite, firstInSameSuite, firstInSequence):
        x.score = 8
      elif self.FourKind(fourKind):
        x.score = 7
      elif self.FullHouse(numberPairs, numberTrips):
        x.score = 6
      elif self.Flush(sameSuite):
        x.score = 5
      elif self.ThreeKind(numberTrips):
        x.score = 4
      elif self.TwoPair(numberPairs):
        x.score = 3
      elif self.OnePair(numberPairs):
        x.score = 2
      if x.score > winningPlayerScore or (x.score == winningPlayerScore and sorted(x.GetHand())[-1] > sorted(self.playerList[index].GetHand()[-1])) and not (index in self.skipIndices):
        winningPlayerScore = x.score
        winningPlayerIndex = index
      index += 1
    return winningPlayerIndex

  def Check(self, cardsChecking):
    #sorts the cards 
    cardsChecking.sort()
    #numbersRepeated is a dictionary that creates entries for numbers that are repeated (what the number is and how many times it shows)
    #suitesRepeated is a dictionary that creates entries for suties that are repeated (what that suite is and how many times it shows)
    numbersRepeated = {}
    suitesRepeated = {}
    #sameSuite and sequencialOrder are booleans that check 
    sameSuite = False
    sequencialOrder = False
    firstInSequence = 0
    currentIndex = 0
    sequentialCounter = 0
    numberPairs = 0
    numberTrips = 0
    fourOfKind = False
    firstInSameSuite = cardsChecking[currentIndex]
    firstInSequence = cardsChecking[currentIndex]
    suiteSkipBool = False
    #creates entries for dictionaries for repeated num and same suites
    for y in cardsChecking:
      cardNum, suite = y.GetCardInfo()
      if cardNum in numbersRepeated:
        numbersRepeated[cardNum] += 1
      else:
        numbersRepeated[cardNum] = 1
      if suite in suitesRepeated:
        suitesRepeated[suite] +=1
      else:
        suitesRepeated[suite] = 1
    #checks if there is a sequential order and where it starts (for there to be a royal flush, it must start at an index of 10) 
      if not currentIndex + 1 >= len(cardsChecking):
        if (cardsChecking[currentIndex + 1].cardNum - y.cardNum != 1) and (cardsChecking[currentIndex + 1].cardNum - y.cardNum != 0):
          sequentialCounter = 0 
          if sequencialOrder != True:
            firstInSequence = cardsChecking[currentIndex + 1]
        elif cardsChecking[currentIndex + 1].cardNum - y.cardNum == 1:
          sequentialCounter += 1
          if sequentialCounter == 4:
            sequencialOrder = True
        #checks if cards in order are in same suite
        if (y.cardNum == cardsChecking[currentIndex + 1].cardNum) and (y.suites == firstInSameSuite.suites):
          suiteSkipBool = True
        elif ((y.suites != firstInSameSuite.suites) and not (cardsChecking[currentIndex + 1].cardNum == y.cardNum) and not (suiteSkipBool == True)) or (cardsChecking[currentIndex + 1].cardNum - y.cardNum > 1):
          firstInSameSuite = cardsChecking[currentIndex + 1]
        else:
          suiteSkipBool = False
        #pdb.set_trace()
      currentIndex += 1
      #looks through the dictionaries
    for amount in numbersRepeated.values():
      if amount == 3:
        numberTrips +=1
      elif amount == 2:
        numberPairs += 1
      elif amount == 4:
        fourOfKind = True
    for amount in suitesRepeated.values():
      if amount >= 5:
        sameSuite = True
    return sequencialOrder, firstInSequence.cardNum, firstInSameSuite, sameSuite, numberTrips, numberPairs, fourOfKind

  #various hand checkers
  def RoyalFlush(self, firstInSequence, inOrder, firstInSameSuite, sameSuite):
    if firstInSequence == 10 and inOrder == True and firstInSameSuite == 10 and sameSuite == True:
      return True
    else:
      return False
  def StraightFlush(self, inOrder, sameSuite, firstInSameSuite, firstInSequence):
    if inOrder == True and sameSuite == True and firstInSameSuite == firstInSequence:
      return True
    else:
      return False
  def FourKind(self, fourOfKind):
    return fourOfKind
  def FullHouse(self, numberPairs, numberTrips):
    if (numberPairs >= 1 and numberTrips == 1) or (numberTrips == 2):
      return True
    else:
      return False
  def Flush(self, sameSuite):
    return sameSuite
  def ThreeKind(self, numberTrips):
    if numberTrips ==1:
      return True
    else:
      return False
  def TwoPair(self, numberPairs):
    if numberPairs >= 2:
      return True
    else:
      return False
  def OnePair(self, numberPairs):
    if numberPairs == 1:
      return True
    else:
      return False


#test functions
def CheckTestSuite():
  listt = []
  dealer = Dealer()
  
  #royale flush, duplicates
  card1 = SpecificCards(14, 4)
  card2 = SpecificCards(13, 4)
  card3 = SpecificCards(12, 4)
  card4 = SpecificCards(11, 4)
  card5 = SpecificCards(10, 4)
  card6 = SpecificCards(14, 3)
  card7 = SpecificCards(14, 2)
  listt = [card1, card2, card3, card4, card5, card6, card7]
  inOrder, firstInSequence, firstInSameSuite, sameSuite, numberTrips, numberPairs, fourKind = dealer.Check(listt)
  assert inOrder == True and firstInSequence == 10 and firstInSameSuite.cardNum == 10 and sameSuite == True and numberTrips == 1 and numberPairs == 0 and fourKind == False
  #royale flush
  card1 = SpecificCards(14, 4)
  card2 = SpecificCards(13, 4)
  card3 = SpecificCards(12, 4)
  card4 = SpecificCards(11, 4)
  card5 = SpecificCards(10, 4)
  card6 = SpecificCards(6, 4)
  card7 = SpecificCards(3,4)
  listt = [card1, card2, card3, card4, card5, card6, card7]
  inOrder, firstInSequence, firstInSameSuite, sameSuite, numberTrips, numberPairs, fourKind = dealer.Check(listt)
  assert inOrder == True 
  assert firstInSequence == 10 
  assert firstInSameSuite.cardNum == 10 
  assert sameSuite == True 
  assert numberTrips == 0 
  assert numberPairs == 0 
  assert fourKind == False
  #royale flush duplicates
  card7 = SpecificCards(13,3)
  listt = [card1, card2, card3, card4, card5, card6, card7]
  inOrder, firstInSequence, firstInSameSuite, sameSuite, numberTrips, numberPairs, fourKind = dealer.Check(listt)
  assert inOrder == True 
  assert firstInSequence == 10 
  assert firstInSameSuite.cardNum == 10 
  assert sameSuite == True 
  assert numberTrips == 0 
  assert numberPairs == 1 
  assert fourKind == False
  #straight flush
  card1 = SpecificCards(13, 4)
  card2 = SpecificCards(12, 4)
  card3 = SpecificCards(11, 4)
  card4 = SpecificCards(10, 4)
  card5 = SpecificCards(9, 4)
  card6 = SpecificCards(6, 4)
  card7 = SpecificCards(3,4)
  listt = [card1, card2, card3, card4, card5, card6, card7]
  inOrder, firstInSequence, firstInSameSuite, sameSuite, numberTrips, numberPairs, fourKind = dealer.Check(listt)
  assert inOrder == True and firstInSequence == 9 and firstInSameSuite.cardNum == 9 and sameSuite == True and numberTrips == 0 and numberPairs == 0 and fourKind == False
  #four of a kind
  card1 = SpecificCards(13, 1)
  card2 = SpecificCards(13, 2)
  card3 = SpecificCards(13, 3)
  card4 = SpecificCards(13, 4)
  card5 = SpecificCards(9, 1)
  card6 = SpecificCards(6, 1)
  card7 = SpecificCards(3,1)
  listt = [card1, card2, card3, card4, card5, card6, card7]
  inOrder, firstInSequence, firstInSameSuite, sameSuite, numberTrips, numberPairs, fourKind = dealer.Check(listt)
  assert inOrder == False and sameSuite == False and numberTrips == 0 and numberPairs == 0 and fourKind == True
  #full house
  card1 = SpecificCards(13, 1)
  card2 = SpecificCards(13, 2)
  card3 = SpecificCards(13, 3)
  card4 = SpecificCards(9, 4)
  card5 = SpecificCards(9, 1)
  card6 = SpecificCards(6, 1)
  card7 = SpecificCards(3,1)
  listt = [card1, card2, card3, card4, card5, card6, card7]
  inOrder, firstInSequence, firstInSameSuite, sameSuite, numberTrips, numberPairs, fourKind = dealer.Check(listt)
  assert inOrder == False and sameSuite == False and numberTrips == 1 and numberPairs == 1 and fourKind == False
  #flush
  card1 = SpecificCards(11, 4)
  card2 = SpecificCards(1, 4)
  card3 = SpecificCards(5, 4)
  card4 = SpecificCards(7, 4)
  card5 = SpecificCards(10, 4)
  card6 = SpecificCards(6, 4)
  card7 = SpecificCards(3,4)
  listt = [card1, card2, card3, card4, card5, card6, card7]
  inOrder, firstInSequence, firstInSameSuite, sameSuite, numberTrips, numberPairs, fourKind = dealer.Check(listt)
  assert inOrder == False 
  assert sameSuite == True 
  assert numberTrips == 0 
  assert numberPairs == 0 
  assert fourKind == False
  #straight
  card1 = SpecificCards(14, 1)
  card2 = SpecificCards(13, 2)
  card3 = SpecificCards(12, 3)
  card4 = SpecificCards(11, 4)
  card5 = SpecificCards(10, 1)
  card6 = SpecificCards(6, 2)
  card7 = SpecificCards(3,3)
  listt = [card1, card2, card3, card4, card5, card6, card7]
  inOrder, firstInSequence, firstInSameSuite, sameSuite, numberTrips, numberPairs, fourKind = dealer.Check(listt)
  assert inOrder == True and firstInSequence == 10 and firstInSameSuite.cardNum == 14 and sameSuite == False and numberTrips == 0 and numberPairs == 0 and fourKind == False

def DeckTestSuite():
  listt = []
  newDeck = Deck()
  for x in range(13):
    listt.append(newDeck.GetRandomCard())
  assert len(listt) - len(set(listt)) == 0
  newDeck.Clear()
  assert not newDeck.cardsGivenOut

def SpecificCardTestSuite():
  SpecificCard = SpecificCards(4, 3)
  SpecificCard2 = SpecificCards(4,1)
  assert SpecificCard.cardNum == 4 and SpecificCard.suites == 3
  SpecificCard.PrintCards()
  SpecificCard2.PrintCards()
  SpecificCard3 = SpecificCards(11, 1)
  SpecificCard4 = SpecificCards(12, 2)
  SpecificCard3.PrintCards()
  SpecificCard4.PrintCards()
  assert SpecificCard > SpecificCard2
  assert SpecificCard3 > SpecificCard4

def RiverTestSuite():
  SpecificCard = SpecificCards(4,3)
  myRiver = River()
  myRiver.RiverAdd(SpecificCard)
  myRiver.RiverPrint()
  myRiver.RiverClear()
  myRiver.RiverPrint()
  SpecificCard = SpecificCards(4,1)
  myRiver.RiverAdd(SpecificCard)
  myRiver.RiverPrint()

def PlayerTestSuite():
  SpecificCard = SpecificCards(4,3)
  SpecificCard4 = SpecificCards(12, 2)
  player1 = Player()
  assert player1.money == 10
  player1.ClearMoney()
  assert player1.money == 0
  player1.AddMoney(5)
  assert player1.money == 5
  player1.SetHand(SpecificCard, SpecificCard4)
  player1.PrintHand()
  player1.Raise(5)
  assert player1.money == 0

#test suites
"""
CheckTestSuite()
DeckTestSuite()
RiverTestSuite()
PlayerTestSuite()
"""
jamesHolzhauer = Dealer()
jamesHolzhauer.StartGame()
#folded player won't be considered, print cards in river 
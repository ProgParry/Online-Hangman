#!/usr/bin/python3

import os
import socket
import re
import json
import random

f = open('hangman-assets/words_dictionary.json')
wordsTable = json.load(f)
playing = True
wins = 0
losses = 0
cheating = False
unlimited = False
thewords = []

os.system('clear')
print("Welcome to Parry's Hangman Game!")
name = input('What is your name?\n')
print(f"\nWelcome {name}!")
os.system('sleep 3')

def pickWord(string):
    exists = False
    for key in list(wordsTable.keys()):
        if string == key:
            exists = True
            break
    return exists

def top():
    print(f"Username: {name}")
    if wins != 0:
        print(f"Words guessed correctly: {wins}")
    if losses != 0:
        print(f"Failed guesses: {losses}")
    if cheating or unlimited:
        print(f"Cheats: enabled")

def printHangman(num):
    if num == 0:
        os.system('cat hangman-assets/hangman-1')
    elif num == 1:
        os.system('cat hangman-assets/hangman-2')
    elif num == 2:
        os.system('cat hangman-assets/hangman-3')
    elif num == 3:
        os.system('cat hangman-assets/hangman-4')
    elif num == 4:
        os.system('cat hangman-assets/hangman-5')
    elif num == 5:
        os.system('cat hangman-assets/hangman-6')
    elif num == 6:
        os.system('cat hangman-assets/hangman-7')
    elif num == 7:
        os.system('cat hangman-assets/hangman-dead')
    else:
        print(f"ERROR: invalid number [NUM]:{num}")

def game():
    global wins, losses, solved
    inGame = True
    status = 0
    gameWord = random.choice(list(wordsTable.keys()))
    thewords.append(gameWord)
    blanksArray = []
    answerArray = []
    guessesArray = []
    incorrectArray = []
    for i in range(len(gameWord)):
        blanksArray.append("_ ")
        answerArray.append("")
    while inGame:
        if not unlimited:
            attempts = 7 - status
        else:
            attempts = 9999
        os.system('clear')
        top()
        printHangman(status)
        print(f"\nIncorrect guesses left: {attempts}\n")
        if attempts == 0:
            print("No more attempts left! You lose!")
            inGame = False
            losses += 1
            print(f"\nThe word was {gameWord}")
            input("\nPress enter to continue...")
            break
        else:
            if cheating:
                print(f"Word: {gameWord}\n")
            print("".join(map(str, blanksArray)))
            if incorrectArray:
                display = " ".join(map(str, incorrectArray))
                print(f"\nIncorrect letters guessed: {display}")
            print("\nType 'exit' to exit")
            print("\nType 'guess' to guess")
            gameInput = input("\nPlease guess a letter 'a-z': ")
            if gameInput in guessesArray:
                print(f"\nYou already guessed '{gameInput}'!")
            elif gameInput in gameWord and re.fullmatch("[a-z]{1}", gameInput):
                charCount = 0
                for char in range(len(gameWord)):
                    if gameInput == gameWord[char]:
                        blanksArray[char] = gameInput + " "
                        answerArray[char] = gameInput
                        charCount += 1
                print(f"\nGood job! '{gameInput}' was found {charCount} times!")
                answer = "".join(answerArray)
                if answer == gameWord:
                    print(f"\nYou won! The word was {gameWord}")
                    inGame = False
                    wins += 1
                    input("\nPress enter to continue...")
                guessesArray.append(gameInput)
            elif gameInput not in gameWord and re.fullmatch("[a-z]{1}", gameInput):
                print(f"\nSorry! '{gameInput}' is not in the word")
                status += 1
                guessesArray.append(gameInput)
                incorrectArray.append(gameInput)
            elif gameInput == "exit":
                inGame = False
                print("\nReturning to main menu...")
            elif gameInput == "guess":
                print("\nType the word you'd like to guess: ")
                guess = input()
                if guess == gameWord:
                    print(f"\nYou guessed the word! It was {gameWord}!")
                    inGame = False
                    wins += 1
                    input("Press enter to continue...")
                else: 
                    print(f"\n{guess} is not the word :(")
                    status += 1
            else:
                print(f"\n{gameInput} is not a valid option!")
        os.system('sleep 3')

def options():
    global name, cheating, unlimited
    inOptions = True
    while inOptions:
        os.system('clear')
        top()
        print("\nType '[n]ame' to change username")
        print("\nType '[c]heats' to turn on cheats")
        print("\nType '[w]ords' to see the words you've seen so far")
        print("\nType '[s]earch' to search for words in the dictionary")
        print("\nType '[e]xit' to return to the main menu\n")
        option = input()
        if re.fullmatch('[nN](ame)?', option):
            while True:
                name = input("\nPlease enter your name: ")
                print(f"\nIs '{name}' correct? [Y/n]\n")
                yesno = input()
                if re.fullmatch('[yY](es)?', yesno) or not yesno:
                    break
                elif re.fullmatch('[nN](o)?', yesno):
                    pass
                else:
                    print(f"\n'{yesno}' is not a valid option")
                    os.system('sleep 3')
        elif re.fullmatch('[cC](heats)?', option):
            onoff = "on"
            if unlimited:
                onoff = "off"
            print(f"\nPress '1' to turn unlimited attempts {onoff}")
            onoff = "on"
            if cheating:
                onoff = "off"
            print(f"\nPress '2' to turn seeing the word {onoff}")
            print("\nPress any other key to not be a stinky little cheater >:(\n")
            cheat = input()
            if cheat == "2":
                cheating = not cheating
            elif cheat == "1":
                unlimited = not unlimited
        elif re.fullmatch('[wW](ords)?', option):
            if thewords:
                print("\nHere are the words you've seen so far: \n")
                for words in thewords:
                    print(words)
            else:
                print("\nYou have not played any games yet :(")
            input("\nPress [enter] to continue...")
        elif re.fullmatch('[sS](earch)?', option):
            while True:
                os.system('clear')
                print("\nType '1' to return to the options menu")    
                search = input("\nWord search: ")
                if search == "1":
                    break
                else:
                    x = 0
                    for word in list(wordsTable.keys()):
                        if search in word:
                            print(f"'{search}' found in {word}")
                            x += 1
                    if x == 0:
                        print(f"\nNo words with '{search}' in them were found")
                    else:
                        print(f"\n{x} words exist with '{search}' in them")
                    input("\nPress [enter] to continue...")
        elif re.fullmatch('[eE](xit)?', option):
            print("\nReturning to main menu...")
            inOptions = False
            os.system('sleep 3')
            break
        else:
            print(f"\n'{option}' is not a valid option, please try again")
            os.system('sleep 3')

def multiplayerHost():
    HOST = ""
    PORT = 6969
    os.system('clear')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("\nWaiting on connection...")
        conn, addr = s.accept()
        with conn:
            print(f"Connection established with {addr}")
            CONNECTED = True
            opponentName = conn.recv(1024).decode('utf-8')
            conn.sendall(bytes(name, 'utf-8'))
            os.system('sleep 3')
            while CONNECTED:
                os.system('clear')
                print("You are picking the word!")
                picking = True
                while picking:
                    print("Type '0' to exit")
                    hostWord = input("Please enter word: ")
                    if pickWord(hostWord):
                        picking = False
                        conn.sendall(bytes(hostWord, 'utf-8'))
                    elif hostWord == '0':
                        CONNECTED = False
                        picking = False
                        print("Goodbye!")
                        conn.sendall(b"DISCONNECT")
                        os.system('sleep 3')
                        break
                    else:
                        print(f"'{hostWord}' is not a word, please try again")
                        os.system('sleep 3')
                if CONNECTED:
                    hooah = True
                else:
                    break
                hostCount = 0
                hostBlanksArray = []
                hostIncorrectArray = []
                for i in range(len(hostWord)):
                    hostBlanksArray.append("_")
                while hooah:
                    os.system('clear')
                    print(f"Username: {name}")
                    print(f"Opponent: {opponentName}")
                    printHangman(hostCount)
                    print(f"Your word: {hostWord}\n")
                    print(f"Opponent attempts left: {7 - hostCount}\n")
                    print(" ".join(map(str, hostBlanksArray)) + "\n")
                    if hostIncorrectArray:
                        display = " ".join(map(str, hostIncorrectArray))
                        print(f"{opponentName} wrong guesses: {display}\n")
                    while True:
                        opponentGuess = conn.recv(1024).decode('utf-8')
                        if opponentGuess:
                            break
                    if opponentGuess == "DISCONNECT":
                        print(f"\n{opponentName} disconnected")
                        hooah = False
                        CONNECTED = False
                        os.system('sleep 3')
                        break
                    if opponentGuess in hostWord:
                        num = 0
                        for char in range(len(hostWord)):
                            if opponentGuess == hostWord[char]:
                                hostBlanksArray[char] = opponentGuess
                                num += 1
                        print(f"{opponentName} guessed '{opponentGuess}'")
                        print(f"\n'{opponentGuess}' is in {hostWord} {num} times!")
                        if "".join(hostBlanksArray) == hostWord:
                            print(f"Oh no! {opponentName} got the word!")
                            print("You lose!")
                            hooah = False
                    elif re.fullmatch("[a-z]{1}", opponentGuess):
                        print(f"{opponentName} guessed '{opponentGuess}' incorrectly")
                        hostCount += 1
                        hostIncorrectArray.append(opponentGuess)
                        if hostCount == 7:
                            print(f"\n{opponentName} is out of attempts! You win!")
                            hooah = False
                            input("Press [enter] to continue...")
                            break
                    else: 
                        print(f"Unexpected {opponentGuess} from {opponentName}")
                        input("\nPress enter to continue...")
                    os.system('sleep 3')

def multiplayerJoin():
    os.system('clear')
    print("Please enter the host IP: ")
    IP = input()
    if re.fullmatch("([0-9]{1,3}\.){3}[0-9]{1,3}", IP):
        print(f"\nAttempting to establish connection to {IP} ...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
            c.connect((IP, 6969))
            CONNECTED = True
            c.sendall(bytes(name, 'utf-8'))
            opponentName = c.recv(1024).decode('utf-8')
            while CONNECTED:
                os.system('clear')
                print("\nYou are guessing!")
                os.system('sleep 3')
                print("\nWaiting on host to pick word")
                waiting = True
                while waiting:
                    word = c.recv(1024).decode('utf-8')
                    if word: 
                        waiting = False
                if word == "DISCONNECT":
                    print(f"{opponentName} disconnected")
                    os.system('sleep 3')
                    CONNECTED = False
                    break
                uhoh = True
                clientAttempts = 0
                clientBlanks = []
                clientGuesses = []
                clientIncorrect = []
                for i in range(len(word)):
                    clientBlanks.append("_")
                while uhoh:
                    os.system('clear')
                    print(f"Username: {name}")
                    print(f"Opponent: {opponentName}")
                    printHangman(clientAttempts)
                    print(f"Incorrect guesses left: {7 - clientAttempts}\n")
                    print(" ".join(clientBlanks))
                    if clientIncorrect:
                        temp = " ".join(clientIncorrect)
                        print(f"\nIncorrect guesses: {temp}")
                    print("\nType 'exit' to exit")
                    clientLetter = input("\nGuess a letter 'a-z': ")
                    if clientLetter in clientGuesses:
                        print("\nYou already guessed that letter!") 
                    elif clientLetter in word and re.fullmatch("[a-z]{1}", clientLetter):
                        c.sendall(bytes(clientLetter, 'utf-8'))
                        count = 0
                        for char in range(len(word)):
                            if clientLetter == word[char]:
                                count += 1
                                clientBlanks[char] = clientLetter
                        print(f"\nNice! '{clientLetter}' was found {count} times!")
                        if "".join(clientBlanks) == word:
                            print(f"\nYou won! The word was {word}")
                            uhoh = False
                    elif clientLetter not in word and re.fullmatch("[a-z]{1}", clientLetter):
                            c.sendall(bytes(clientLetter, 'utf-8'))
                            print(f"\nSorry, '{clientLetter}' is not in the word")
                            clientAttempts += 1
                            if clientAttempts == 7:
                                print("\nThat's too many wrong guesses! You lose!")
                                print(f"\nThe word was {word}")
                                uhoh = False
                            clientGuesses.append(clientLetter)
                            clientIncorrect.append(clientLetter)
                    elif clientLetter == "exit":
                        print("goodbye!")
                        c.sendall(b"DISCONNECT")
                        CONNECTED = False
                        uhoh = False
                    else:
                        print(f"{clientLetter} is not a valid option, please try again")
                    os.system('sleep 3')
    else:
        print(f"\n{IP} does not seem  to be a valid IP")
        os.system('sleep 3')

def multiplayerMenu():
    inMultiplayerMenu = True
    while inMultiplayerMenu:
        os.system('clear')
        top()
        print("\nType '[h]ost' to start a multiplayer session")
        print("\nType '[j]oin' to join another session")
        print("\ntype '[e]xit' to return to the main menu\n")
        multMenuInput = input()
        if re.fullmatch("[eE](xit)?", multMenuInput):
            print("\nReturning to main menu...")
            inMultiplayerMenu = False
            os.system("sleep 3")
        elif re.fullmatch("[jJ](oin)?", multMenuInput):
            multiplayerJoin()
        elif re.fullmatch("[hH](ost)?", multMenuInput):
            multiplayerHost()
        else:
            print(f"\n{multMenuInput} is not a valid option, please try again")
            os.system("sleep 3")

while playing:
    os.system('clear')
    top()
    print("\nType '1' to play single player")
    print("\nType '2' to play online multiplayer")
    print("\nType '3' to see the options menu")
    print("\nType '[e]xit' to exit\n")
    menuInput = input()
    if menuInput == "1":
        game()   
    elif menuInput == "2":
        multiplayerMenu()
    elif menuInput == "3":
        options()
    elif re.fullmatch("[eE](xit)?", menuInput):
        print("Goodbye!")
        os.system('sleep 3')
        playing = False
        break
    else:
        print(f"{menuInput} is an invalid input, please try again")
        os.system('sleep 3')

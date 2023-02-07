import random
import colorama
from colorama import Fore, Style
colorama.init(autoreset=True)

# Lobby
def mainmenu():
    enter = 0
    while enter != "X":
        print(Fore.WHITE + Style.BRIGHT + "Select a venture from the below list -")
        print()
        print(Fore.LIGHTMAGENTA_EX + "1. Play Game")
        print(Fore.LIGHTMAGENTA_EX + "2. Create Account")
        print(Fore.LIGHTMAGENTA_EX + "3. Leagues & Rankings")
        print(Fore.LIGHTMAGENTA_EX + "4. Rules and Instructions")
        print(Fore.LIGHTMAGENTA_EX + "5. Player Information")
        print()
        enter = input("Enter a numeral to proceed or press X to Exit the game: ")
        if enter == "1":
            playgame()
        elif enter == "2":
            print()
            accountcreator()
        elif enter == "3":
            print()
            lrt()
        elif enter == "4":
            print()
            ri()
        elif enter == "5":
            playerboard()
        elif enter == "X":
            return
        else:
            print(Fore.RED + Style.BRIGHT + "Please enter a valid input only.")
        print()

# Game mechanics
def playgame():
    global database
    global namelist
    namelist = []
    global playerlist
    playerlist = []
    global scorelist
    scorelist = []
    print()
    print(Fore.BLUE + Style.BRIGHT + "Fill in the required credentials to proceed.")
    username = unlogin()
    if username == -1:
        return
    password = pwlogin(username)
    if password == -1:
        return
    print()
    print("Welcome,",Fore.YELLOW + Style.BRIGHT + database[username]["name"])
    print(Fore.BLUE + Style.BRIGHT + "Select the Match you want to play: ")
    print()
    print("Players| Cost | Rewards")
    print("---------------------------")
    print("   2   |  25  |   30")
    print("   3   |  21  |   40")
    print("   4   |  18  |   50")
    print("   5   |  15  |   60")
    print()
    players = int(input(Fore.BLACK + Style.BRIGHT + "Enter Number of Players: " + Fore.RESET + Style.NORMAL))
    while (players < 2 or players > 5):
        print(Fore.RED + Style.BRIGHT + "Players should be between 2 and 5!")
        print()
        players = int(input(Fore.BLACK + Style.BRIGHT + "Enter Number of Players: " + Fore.RESET + Style.NORMAL))

    if players == 2:
        mc = 25
    elif players == 3:
        mc = 21
    elif players == 4:
        mc = 18
    elif players == 5:
        mc = 15
    else:
        mc = 0
    playerlist.append(username)
    scorelist.append(0)
    namelist.append(database[username]["name"])
    database[username]["coins"] = database[username]["coins"]-mc
    for i in range(1, players):
        username = unlogin()
        if username == -1:
            return
        playerlist.append(username)
        scorelist.append(0)
        namelist.append(database[playerlist[i]]["name"])
        database[playerlist[i]]["coins"] = database[playerlist[i]]["coins"]-mc
        if database[playerlist[i]]["coins"] < 0:
            database[playerlist[i]]["coins"] = 0
            print(namelist[i], "didn't had the Coins required as Match Cost.")
            enter = input("Press ENTER to watch an AD to get required coins.")
            print()
            print('''ANACONDA DISTRIBUTION
The world's most popular open-source Python distribution platform
Try it now at www.anaconda.com''')
            print()
            enter = input("Press ENTER to continue.")
    print()
    playboard(scorelist, i+1)

    while max(scorelist) != 100:
        for i in range(players):
            s = 0
            if input('{}, press ENTER for your turn '.format(namelist[i])) == "":
                Dice = random.randint(1, 6)
                print()
                print(Fore.MAGENTA + Style.BRIGHT + 'The dice outcome is: ', Dice)
            scorelist[i] = scorelist[i] + Dice
            if scorelist[i] > 100:
                scorelist[i] = scorelist[i]-Dice
                playboard(scorelist, i)
                print(namelist[i], ", you need", (100-scorelist[i]), "to win.")
                print()
            if scorelist[i] == 89 or scorelist[i] == 78 or scorelist[i] == 67 or scorelist[i] == 56 or scorelist[i] == 45 or scorelist[i] == 34 or scorelist[i] == 23 or scorelist[i] == 12:
                scorelist[i] = scorelist[i]-10
                s = 1
                playboard(scorelist, i, s)
            elif scorelist[i] == 19 or scorelist[i] == 28 or scorelist[i] == 37 or scorelist[i] == 46 or scorelist[i] == 55 or scorelist[i] == 64 or scorelist[i] == 73 or scorelist[i] == 82:
                scorelist[i] = scorelist[i]+10
                s = 2
                playboard(scorelist, i, s)
            else:
                playboard(scorelist, i)

            if scorelist[i] == 100:
                winner = i
                break
    print(Fore.CYAN + Style.BRIGHT + "Congratulations, Winner of the game is {}".format(namelist[winner]))
    database[playerlist[winner]
             ]["trophies"] = database[playerlist[winner]]["trophies"]+125
    for i in range(players):
        database[playerlist[i]]["trophies"] = database[playerlist[i]]["trophies"]-25
        if database[playerlist[i]]["trophies"] < 0:
            database[playerlist[i]]["trophies"] = 0
    enter = input("Press ENTER to get redirected to the Main Menu.")

# Playboard
def playboard(scorelist, i, s=0):
    global database
    global playerlist
    global namelist
    n = 100
    for k in range(10):
        for l in range(10):
            if n in scorelist:
                index = scorelist.index(n)
                print(Fore.YELLOW + Style.BRIGHT + database[playerlist[index]]["symbol"], end="   ")
            elif n < 10:
                print(n, end="   ")
            elif n % 10 == 0 and n < 100:
                print(n, end="   ")
            elif n == 89 or n == 78 or n == 67 or n == 56 or n == 45 or n == 34 or n == 23 or n == 12:
                print(Fore.LIGHTRED_EX + "S", end="   ")
            elif n == 19 or n == 28 or n == 37 or n == 46 or n == 55 or n == 64 or n == 73 or n == 82:
                print(Fore.LIGHTGREEN_EX + "L", end="   ")
            else:
                print(n, end="  ")
            n = n-1
        print()
    if s == 1:
        print()
        print(namelist[i],Fore.RED + 'got bit by snake.')

    elif s == 2:
        print()
        print(namelist[i],Fore.GREEN + 'climbed a ladder.')
    print()
    return n

# Username login
def unlogin():
    global database
    username = input(Fore.BLACK + Style.BRIGHT + "Username: " + Fore.RESET + Style.NORMAL)
    if username not in database:
        print(Fore.RED + Style.BRIGHT + "This Username doesn't exist.")
        username = input(Fore.BLACK + Style.BRIGHT + "Username: " + Fore.RESET + Style.NORMAL)
    else:
        return username

# Password login 
def pwlogin(username):
    global database
    password = input(Fore.BLACK + Style.BRIGHT + "Enter Your Password: " + Fore.RESET + Style.NORMAL)
    if password != database[username]["password"]:
        print(Fore.RED + Style.BRIGHT + "Wrong Password")
        pwlogin(username)
    else:
        return password

#Sign in
def accountcreator():
    global database
    print(Fore.BLUE + Style.BRIGHT + "Welcome to the Account Creation Menu.")
    print(Style.BRIGHT + "Fill up the following fields to create your Account.")
    print()
    name = input(Fore.BLACK + Style.BRIGHT + "Enter your Name: " + Fore.RESET + Style.NORMAL)
    mail = mailchecker()
    symbol = symbolchecker()
    username = usernamecreator()
    password = passwordcreator(username)
    coins = 10000
    trophies = 0

    database[username] = {"name": name, "mail": mail, "symbol": symbol, "password": password,
                          "coins": coins, "trophies": trophies}
    print()
    print(Fore.GREEN + Style.BRIGHT + "Congratulations, Your Account Has Been Created.")
    print(Style.BRIGHT + "10,000 Coins have been alloted to you.")
    print(Style.BRIGHT + "Good luck for your journey to the topmost leagues.")
    print()
    enter = input("Press ENTER to go back to the Main Menu.")
    return

# New username
def usernamecreator():
    global database
    username = input(Fore.BLACK + Style.BRIGHT + "Create a Unique Username: " + Fore.RESET + Style.NORMAL)
    if username in database:
        print(Fore.RED + Style.BRIGHT + "This Username is Already in Existence.")
        print()
        username = usernamecreator()
        return username
    else:
        return username

# New account password
def passwordcreator(username):
    global database
    password = input(Fore.BLACK + Style.BRIGHT + "Create a password: " + Fore.RESET + Style.NORMAL)
    reconfirm = input(Fore.BLACK + Style.BRIGHT +"Reconfirm the password: " + Fore.RESET + Style.NORMAL)
    if password == reconfirm:
        return password
    else:
        print(Fore.RED + Style.BRIGHT + "Passwords didn't match.")
        print()
        password = passwordcreator(username)
        return password

def passwordchanger(username):
    global database
    password = input(Fore.BLACK + Style.BRIGHT + "Create a password: " + Fore.RESET + Style.NORMAL)
    if password==database[username]["password"]:
        print(Fore.RED + Style.BRIGHT + "Password already exists.")
        password = passwordchanger(username)
        reconfirm = input(Fore.BLACK + Style.BRIGHT +"Reconfirm the password: " + Fore.RESET + Style.NORMAL)
        if password == reconfirm:
            return password
    else:
        reconfirm = input(Fore.BLACK + Style.BRIGHT +"Reconfirm the password: ")
        if password == reconfirm:
            return password

# Mail Checker
def mailchecker():
    mail = input(Fore.BLACK + Style.BRIGHT + "Enter Your Mail ID: " + Fore.RESET + Style.NORMAL)
    if ("@" not in mail) or ("." not in mail):
        print(Fore.RED + Style.BRIGHT + "INVALID MAIL ID")
        mailchecker()
    else:
        return mail

#Symbol checker
def symbolchecker():
    symbol = input(Fore.BLACK + Style.BRIGHT + "Select a single character symbol for your Pawn: " + Fore.RESET + Style.NORMAL)
    if len(symbol) != 1:
        print(Fore.RED + Style.BRIGHT + "INVALID SYMBOL")
        enter = input()
        symbolchecker()
    else:
        return symbol

#Ranking 
def lrt():
    print(Fore.BLUE + Style.BRIGHT + "Leagues & Trophies")
    print()
    print("S.No |  League  | Trophies")
    print("---------------------------")
    print(" 1.  |   Iron   | 0-100 ")
    print(" 2.  |  Bronze  | 101-500")
    print(" 3.  |  Silver  | 501-1000")
    print(" 4.  |   Gold   | 1001-1500")
    print(" 5.  |  Emerald | 1501-2000")
    print(" 6.  |  Crystal | 2001-2500")
    print(" 7.  |  Diamond | 2500+")
    print()
    enter = input("Press Enter to go back to the Main Menu.")
    return

#Instructions
def ri():
    print(Fore.BLUE + Style.BRIGHT + "Rules and Instructions")
    print(Fore.LIGHTBLACK_EX + "1.) The First player to reach 100 wins.")
    print(Fore.LIGHTBLACK_EX + "2.) L represents Ladder, reaching onto it will reward a bonus of 10 points.")
    print(Fore.LIGHTBLACK_EX + "3.) S represents Snake, reaching onto it will cause a penalty of 10 points.")
    print(Fore.LIGHTBLACK_EX + "4.) Winning a non-pratice match awards 100 trophies.")
    print(Fore.LIGHTBLACK_EX + "5.) Losing a non-practice match deducts 25 trophies.")
    print()
    print(Style.BRIGHT + "Let's Enjoy the Game.")
    print()
    enter = input("Press Enter to go back to the Main Menu.")
    return

# Player Inforamtion
def playerboard():
    global database
    global extra
    print()
    print(Fore.BLUE + Style.BRIGHT + "You can change your credentials here")
    username = unlogin()
    if username == -1:
        return
    password = pwlogin(username)
    if password == -1:
        return
    if database[username]["trophies"] < 201:
        print()
        print("Welcome,",Fore.MAGENTA + Style.BRIGHT + database[username]["name"])
        print(Fore.YELLOW + "LEAGUE", "->" + Fore.CYAN + Style.BRIGHT + "Unranked")

    elif database[username]["trophies"] < 501:
        print()
        print("Welcome,",Fore.MAGENTA + Style.BRIGHT + database[username]["name"], "(1 STAR)")
        print(Fore.YELLOW + "LEAGUE", "->" + Fore.CYAN+ Style.BRIGHT + "Iron")

    elif database[username]["trophies"] < 1001:
        print()
        print("Welcome,",Fore.MAGENTA + Style.BRIGHT + database[username]["name"], "(2 STAR)")
        print(Fore.YELLOW + "LEAGUE", "->" + Fore.CYAN+ Style.BRIGHT + "Bronze")

    elif database[username]["trophies"] < 1501:
        print()
        print("Welcome,",Fore.MAGENTA + Style.BRIGHT + database[username]["name"], "(3 STAR)")
        print(Fore.YELLOW + "LEAGUE", "->" + Fore.CYAN + Style.BRIGHT + "Silver")

    elif database[username]["trophies"] < 2001:
        print()
        print("Welcome,",Fore.MAGENTA + Style.BRIGHT + database[username]["name"], "(4 STAR)")
        print(Fore.YELLOW + "LEAGUE", "->" + Fore.CYAN + Style.BRIGHT + " Gold")

    elif database[username]["trophies"] < 2501:
        print()
        print("Welcome,",Fore.MAGENTA + Style.BRIGHT + database[username]["name"], "(5 STAR)")
        print(Fore.YELLOW + "LEAGUE", "->" + Fore.CYAN+ Style.BRIGHT + " Platinum")

    elif database[username]["trophies"] > 2500:
        print()
        print("Welcome,",Fore.MAGENTA + Style.BRIGHT + database[username]["name"], "(6 STAR)")
        print(Fore.YELLOW + "LEAGUE", "->" + Fore.CYAN + Style.BRIGHT + " Diamond")

    print(Fore.YELLOW + "TROPHIES", "->", database[username]["trophies"])
    print(Fore.YELLOW + "COINS", "->", database[username]["coins"])
    print(Fore.YELLOW + "SYMBOL", "->", database[username]["symbol"])
    print(Fore.YELLOW + "MAIL ID", "->", database[username]["mail"])
    print()
    print("Press U to update your username")
    print("Press P to update your password")
    print("Press ENTER to return to the Main Menu.")
    enter = input()
    extra=username
    if enter == "U":
        newusername = usernamecreator()
        database[newusername] = database[username]
        print(Fore.GREEN + Style.BRIGHT + "Username changed successfully.")
        del database[username]
        return
    elif enter == "P":
        database[username]["password"] = passwordchanger(username)
        print(Fore.GREEN + Style.BRIGHT + "Password changed successfully.")
        return
    else:
        return 

database = {'h': {'name': 'h', 'mail': 'h', 'symbol': 'h', 'password': 'h', 'coins': 10000, 'trophies': 3000,},
'd': {
    'name': 'd', 'mail': 'd', 'symbol': 'd', 'password': 'd', 'coins': 10000, 'trophies': 0}}

print()
print(Fore.GREEN + Style.BRIGHT + "Welcome to the game 'Snakes & Ladders'")
mainmenu()
print(database)
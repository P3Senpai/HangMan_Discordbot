import os
import discord
from discord.ext import commands

client = commands.Bot(command_prefix='!')
TOKEN = "NTU0NjY1MjkwMTI2ODUyMTE2.D2qAJA.lZShQC3O7z2luBho9C3-NySPEL8"
man_lives = 5  # arbitrary number
guessed = []
word_chosen = "{{{empty}}}"
correct_guess = []
heart_emojii = ":heart:"
lose_emojii = ":disappointed_relieved:"
running_game = False
restart_agree = False

def check(word, *args):
    guess = "".join(*args)
    if word == guess:
        return True
    else:
        return False


def insert_under(string):
    for j in range(0, len(string)):
        global correct_guess
        correct_guess.append("_")
        print(correct_guess) # TEST


def char_lower_eng(letter):
    if len(letter) != 1 or ord(letter) < 97 or ord(letter) > 122:
        return False
    return True


def lower_eng(word):
    for i in range(0, len(word)):
        if ord(word[i]) < 97 or ord(word[i]) > 122:
            return False
    return True
    #  TESTS BELOW
    # wrong_char = ", ".join(guessed)
    # await client.say(f"{hang_stages[man_lives-1]}")
    # await client.say(" ".join(correct_guess))
    # await client.say(f"Wrong letters guessed: {wrong_char}")
def hud():
    word_correct = " ".join(correct_guess)
    all_guessed = ", ".join(guessed)
    hud_str = f"{hang_stages[man_lives-1]}\nLives left: {heart_emojii*man_lives}\nLetters Guessed: {all_guessed}\nWord: {word_correct}"
    return hud_str

def restart_game():
    global word_chosen
    global running_game
    global man_lives
    global correct_guess
    global restart_agree
    man_lives = 5  # arbitrary number
    guessed = []
    word_chosen = "{{{empty}}}"
    correct_guess = []
    running_game = False
    restart_agree = False

hang_stages = [
"""
      _______
     |/      |
     |      (_)
     |      \|/
     |       |
     |      | |
     |
    _|___""",
"""
      _______
     |/      |
     |      (_)
     |      \|/
     |       |
     |
     |
    _|___""",
               """
      _______
     |/      |
     |      (_)
     |      \|/
     |
     |
     |
    _|___""",
               """
      _______
     |/      |
     |      (_)
     |
     |
     |
     |
    _|___""",
               """
      _______
     |/      |
     |
     |
     |
     |
     |
    _|___"""
               ]


@client.event
async def on_ready():
    print("I'm in")
    print(client.user)


@client.command(pass_context=True)
async def start(ctx, message=""):
    global running_game
    channel = str(ctx.message.channel)
    if running_game:
        await client.say("Game is in progress.\nTo start a new game use the !restart command")
    elif channel != "general":
        await client.say("You must choose your word in the general channel")
    elif not lower_eng(message) and len(message) > 0:
        await client.say("Error. Word must only contain lower cased english letters \n" + "Please try again")
    else:
        global word_chosen
        global correct_guess
        running_game = True
        word_chosen = message
        await client.say("Word Chosen")
        await client.say(message)
        await client.say(f"word-chosen {word_chosen}")
        insert_under(word_chosen)
        ey = " ".join(correct_guess)
        await client.say(ey)
        print(ey)


@client.command()
async def show():
    await client.say(word_chosen)
    await client.say(" ".join(correct_guess))
    await client.say(str(running_game))

@client.command(pass_context=True)
async def guess(ctx,message=""):
    channel = str(ctx.message.channel)
    empty= message.strip()
    if channel != "general":
        await client.say("Or not in general channel")
    elif empty == "":
        await client.say("Guess empty")
    elif not running_game:
        await client.say("Or game not in progress")
    else:
        char = message.lower()
        if not char_lower_eng(char) or char == "":
            error = "Your guess must only contain 1 character in the English alphabet"
            await client.say(error)
        elif (char in correct_guess or char in guessed):
            error = f"You have already guesssed \"{char}\""
            await client.say(error)
        else:
            if char in word_chosen:
                for i in range(0, len(word_chosen)):  # check if it runs to end of word
                    if char == word_chosen[i]:
                        # await client.say(type(correct_guess))
                        # await client.say(correct_guess)
                        correct_guess[i] = char
                        # await client.say(f"2nd:    {type(correct_guess)}")
                        # correct_guess.pop(i)
                        # correct_guess.insert(i, char)
                        # await client.say(correct_guess)
                        # await client.say("guessed correctly")
            else:
                global man_lives
                man_lives -= 1
                guessed.append(char)
                # await client.say("guessed incorrectly")
            # win condition below
            if check(word_chosen, correct_guess):  # move if statement if you want win to display before other things
                ans = "".join(correct_guess)
                await client.say(f"You win! The word is ***{ans}*** and you had {heart_emojii*man_lives} lives left")
                restart_game()
                # end game
            if man_lives == 0:
                await client.say(f"You lost {lose_emojii}.  The word is **{ans}**. Better luck next time")
                restart_game()
                # end game
            # iterating print of status
        if running_game == True:
            await client.say(hud()) # todo: figure out position of hud in game


@client.command()
async def hud_command():
    word_correct = " ".join(correct_guess)
    all_guessed = ", ".join(guessed)
    hud_str = f"{hang_stages[man_lives-2]}\nLives left: {heart_emojii*man_lives}\nLetters Guessed: {all_guessed}\nWord: {word_correct}"
    await client.say(hud_str)

@client.command()
async def restart():
    global restart_agree
    print (restart_agree)
    if not running_game or restart_agree:
        restart_game()
        await client.say("Game successfully restarted")
    else:
        restart_agree = True
        print (restart_agree)
        # await client.say("Game is currently in progress\nTo restart the game just type the command again")

@client.command()
async def sellout():
    pass  # link to ashot's nuse website

# @client.command()
# async def help():
#     await client.say("***")
#     all = ["!start","!show","!guess","!restart"]
#     for i in all:
#         await client.say(i)
#     await client.say("***")

client.run(TOKEN)

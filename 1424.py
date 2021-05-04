import random

# roll dice
# decide what to keep
DEBUG=False

def roll_dice(num):
        temp = []
        for i in range(num):
                temp.append(random.randint(1,6))
        return temp

def is_qualified(dice):
        return 4 in dice and 1 in dice

def total_points(dice):
        if not is_qualified(dice):
                return 0
        temp = dice.copy()
        return sum(temp ) - 5

def log(string):
        if DEBUG:
                print(string)

def play_a_game(gamble, reallygamble, keepfive, keepfour):
        kept_dice = []
        rolled_dice = []
        num_dice = 6


        while len(kept_dice) < 6:
            rolled_dice = roll_dice(6-len(kept_dice))
            log("ROLL")
            log(rolled_dice)
            kept = 0
            # Qualify if you can
            if not is_qualified(kept_dice):
                    if 1 in rolled_dice and 1 not in kept_dice:
                            kept_dice.append(1)
                            rolled_dice.remove(1)
                            kept += 1
                    if 4 in rolled_dice and 4 not in kept_dice:
                            kept_dice.append(4)
                            rolled_dice.remove(4)
                            kept += 1
            rolled_dice.sort(reverse=True)
            for i in rolled_dice:
                if is_qualified(kept_dice) and i == 6:
                        kept_dice.append(6)
                        kept += 1
                        log("KEPT 6")
                elif gamble and i == 6 and len(kept_dice) < 3:
                        kept_dice.append(6)
                        kept += 1
                        log("KEPT 6... gambling")
                elif reallygamble and i == 6 and len(kept_dice) <= 4:
                        kept_dice.append(6)
                        kept += 1
                        log("KEPT 6... gambling")
                elif kept == 0:
                        kept_dice.append(i)
                        kept+= 1
                        log("KEPT {}".format(i))
                elif keepfour and is_qualified(kept_dice) and len(kept_dice) >= 4 and i >= 4:
                        kept_dice.append(i)
                        kept+=1
                        log("KEPT the last {}".format(i))
                elif keepfive and is_qualified(kept_dice) and len(kept_dice) >= 5 and i >= 4:
                        kept_dice.append(i)
                        kept+=1
                        log("KEPT the last {}".format(i))

            log("KEPT {}".format(kept_dice))
        return (total_points(kept_dice))

def count_games(gamelist):
        temp = {}
        for i in range(25):
            temp[i] = sum([1 for b in gamelist if b == i])
        return temp

vanilla_games = []
gamble_games = []
reallygamble_games = []
keep_five_games = []
keep_four_games = []
for i in range(100000):
    vanilla_games.append(play_a_game(False,False, False, False))
    gamble_games.append(play_a_game(True,False, False, False))
    reallygamble_games.append(play_a_game(True, True, False, False))
    keep_five_games.append(play_a_game(False, False, True, False))
    keep_four_games.append(play_a_game(False, False, True, False))

print("---- averages ----")
print("vanilla: {}".format(sum(vanilla_games) / len(vanilla_games)))
print("gamble: {}".format(sum(gamble_games) / len(gamble_games)))
print("reallygamble: {}".format(sum(reallygamble_games) / len(reallygamble_games)))
print("keep_five: {}".format(sum(keep_five_games) / len(keep_five_games)))
print("keep_four: {}".format(sum(keep_four_games) / len(keep_four_games)))
print ("\n---- perfects ----")

print("vannila perfects: {}".format(sum([1 for game in vanilla_games if game == 24])))
print("gamble perfects: {}".format(sum([1 for game in gamble_games if game == 24])))
print("reallygamble perfects: {}".format(sum([1 for game in reallygamble_games if game == 24])))
print("five perfects: {}".format(sum([1 for game in keep_five_games if game == 24])))
print("four perfects: {}".format(sum([1 for game in keep_four_games if game == 24])))

print("\n---- nonQualifiers ----")
print("vannila nonqual: {}".format(sum([1 for game in vanilla_games if game == 0])))
print("gamble nonqual: {}".format(sum([1 for game in gamble_games if game == 0])))
print("reallygamble nonqual: {}".format(sum([1 for game in reallygamble_games if game == 0])))
print("five nonqual: {}".format(sum([1 for game in keep_five_games if game == 0])))
print("four nonqual: {}".format(sum([1 for game in keep_four_games if game == 0])))

print("\n---- Count ----")
print (count_games(vanilla_games))
print (count_games(keep_four_games))
print (count_games(keep_five_games))
print (count_games(gamble_games))
print (count_games(reallygamble_games))

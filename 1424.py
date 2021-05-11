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
        return sum(temp) - 5

def log(string):
        if DEBUG:
                print(string)

def computer_play_a_game(gamble, reallygamble, keepfive, keepfour):
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
                elif keepfive and is_qualified(kept_dice) and len(kept_dice) >= 4 and i >= 5:
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

def output(status):
        if status['qualified']:
                print("QUALIFIED")
        else:
                print("NOT QUALIFIED")
        print("KEPT DICE: {}".format(",".join(str(k) for k in status['kept'])))
        print("ROLL: {}".format(",".join(str(k) for k in status['roll'])))
        print("LOG:")
        print("\n".join(status['messages']))
        print("=====================")

def human_play_a_game():
        kept_dice = []
        rolled_dice = []
        num_dice = 6
        status = {}

        while len(kept_dice) < 6:
            rolled_dice = roll_dice(6-len(kept_dice))
            messages = []
            kept = 0
            status['qualified'] = is_qualified(kept_dice)
            status['kept'] = kept_dice
            if not is_qualified(kept_dice):
                    if 1 in rolled_dice and 1 not in kept_dice:
                            kept_dice.append(1)
                            rolled_dice.remove(1)
                            kept += 1
                            messages.append('Kept 1 for qualification')    
                    if 4 in rolled_dice and 4 not in kept_dice:
                            kept_dice.append(4)
                            rolled_dice.remove(4)
                            kept += 1
                            messages.append('Kept 4 for qualification')
            
            status['roll'] = rolled_dice
            status['messages'] = messages
            rolled_dice.sort(reverse=True)
            finished = False
            for die in rolled_dice:
                    if kept == 0:
                            kept_dice.append(die)
                            messages.append('Have to keep {}'.format(die))
                            kept += 1
                            continue
                    status['messages'].append('Do you want to keep {}'.format(die))
                    output(status)
                    decision = input("(k)eep or (r)oll")
                    if decision.lower() == 'k':
                           kept_dice.append(die)
                    if decision.lower() == 'r':
                            break
            output(status)
        _ = input("Total {}\n ---- press key to continue ----".format(total_points(kept_dice)))
        return total_points(kept_dice)

computer_players = {
                'gambler': [False, True, False, False],
                'real_gambler': [True, True, False, False],
                'normal': [False, False, False, False],
                'press_five': [False, False, False, True],
                'press_four': [False, False, True, False]
                }


def play_a_round():
        players = ['human','press_five', 'normal', 'gambler', 'real_gambler', 'press_four']
        money = [15 for p in players]
        turn = 0
        pot = 0
        while turn < len(players):
            number = -1
            tie = False
            top_player = -1
            for player in [i%len(players) for i in range(turn,turn+len(players))]:
                    print("=======================")
                    print("Player:{} money:${}".format(player, money[player]))
                    print("-----------------------")
                    pot += 1
                    money[player] -= 1
                    if players[player] == 'human':
                        total = human_play_a_game()
                    else:
                        total = computer_play_a_game(*computer_players[players[player]])
                    print("Total was {} old number was {}".format(total, number))
                    if total == number:
                            print("TIE!")
                            tie = True
                    elif total > number:
                            print("New Number {}".format(total))
                            tie = False
                            number = total
                            top_player=player
                    elif total == 0:
                            print("Didn't qualify")
                            money[player] -= 1
                            pot += 1
            if tie:
                    a = 1
                    print(">>>>>>>>>>>>>TIE! we do it again<<<<<<<<<<<<<<<<<")
            else:
                    print("<<<<<<<<<<<<<{} wins {}>>>>>>>>>>>>>".format(top_player, pot))
                    money[top_player] += pot
                    pot = 0
                    turn += 1
        print(money)

def play_a_bunch():
        vanilla_games = []
        gamble_games = []
        reallygamble_games = []
        keep_five_games = []
        keep_four_games = []
        for i in range(10000):
            vanilla_games.append(computer_play_a_game(False,False, False, False))
            gamble_games.append(computer_play_a_game(True,False, False, False))
            reallygamble_games.append(computer_play_a_game(True, True, False, False))
            keep_five_games.append(computer_play_a_game(False, False, True, False))
            keep_four_games.append(computer_play_a_game(False, False, True, False))

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

print(play_a_round())

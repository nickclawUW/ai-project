'''
Nicholas Clawson and Daniel Nakamura CSE 415, Spring 2015, University of Washington
Assignment 5
Our working K in a row player
'''

import random
from Player import Player
import lang

'''
Global Variables
'''

GOOD = [
    "You don't stand a chance against me, {0}!",
    "You're going down!",
    "Did you see that one coming {0}?",
    "You are doing really bad {0}.",
    "Do you now understand the rules?",
    "You are really bad at this game",
    "I think I'm going to win this one!",
    "Only a few moves until victory!"
]
BAD = [
    "How do you play this game? I apparently forgot..",
    "How did this get so bad??",
    "Good move {0}",
    "Your skills are really good {0}",
    "How did you get so good {0}",
    "Do you play this game all the time?"
]
MEH = [
    "Do you think you're going to win {0}?",
    "I don't really know where to put this piece so whatever..",
    "I guess this move'll do..",
    "Do you think this will end up in a tie {0}?",
    "This game is pretty boring.",
    "Do you think this game is boring",
    "We're so evenly matched!"
]
GOOD_TWIST = [
    "Did you expect that sort of comeback?!",
    "Booyah!",
    "It's comeback time baby!",
    "Now it's a real game!",
    "Why did you stop trying?"
]
BAD_TWIST = [
    "Where did that come from?",
    "I did not see that coming {0}..",
    "How did you do that {0}?",
    "That move doesn't even seem legal..",
    "That wasn't nice {0}!",
    "Seriously?!",
    "Why did you start playing all of a sudden?"
]
REASON = [
    "reasons!",
    "it seems like the game was going that way",
    "mind your own beeswax!",
    "it's really the only thing I can say.",
    "the gods made it so!",
    "that is what I choose to believe."
]
EXPLANATION = [
    "cheating..",
    "being the better person {0}.",
    "putting myself in fates hands.."
]

class WeightedPlayer(Player):

    def __init__(self, name):
        Player.__init__(self, name)
        self.previous_score = 0

    def move(self, board, turn, remarks):
        best_score = None
        best_move = None

         # for each coordinate that is empty
        for y in range(0, self.h):
            for x in range(0, self.w):
                if board[y][x] != " ": continue

                # evaluate the score _if_ we moved there
                new_state = deep_copy(board)
                new_state[y][x] = self.symbol
                score = self.eval(new_state)

                # if this is the first run
                # _or_ this position is better than our current best
                # save the new move information
                if best_score == None:
                    best_score = score
                    best_move = (y, x)
                elif score > best_score:
                    best_score = score
                    best_move = (y, x)

        # fallback response
        response = "Good move."

        return best_move, self.make_remark(board, best_move, turn, remarks)

    '''
    Evaluate the current state
    Positive return is good for player
    Negative return is bad for player
    '''
    def eval(self, state):
        myScore = 0
        theirScore = 0

        for (player, symbol) in self.players:
            for streak in self.build_list(state, symbol):
                count = streak_score(streak, state, symbol)
                if count == self.k:
                    myScore += self.k ** (count + 1)
                elif count > 0 and symbol == self.symbol:
                    myScore += self.k ** (count - 1)
                elif count > 0 and symbol != self.symbol:
                    theirScore += self.k ** (count)

        return myScore - theirScore / (len(self.players) - 1)

    def build_list(self, state, side):
        h = self.h
        w = self.w
        K = self.k
        STREAKS = []

        # for each coordinate on the board
        for y in range(0, h):
            for x in range(0, w):

                # try a streak going 'up and right'
                streak = []
                for z in range(0, K):
                    if x + z >= w: break
                    if y - z < 0: break
                    if state[y -z][x + z] != " " and state[y - z][x + z] != side: break
                    streak.append((x + z, y - z))
                if len(streak) == K: STREAKS.append(streak)

                # try the streak going 'right'
                streak = []
                for z in range(0, K):
                    if x + z >= w: break
                    if state[y][x + z] != " " and state[y][x + z] != side: break
                    streak.append((x + z, y))
                if len(streak) == K: STREAKS.append(streak)

                # try the streak going 'down right'
                streak = []
                for z in range(0, K):
                    if x + z >= w: break
                    if y + z >= h: break
                    if state[y + z][x + z] != " " and state[y + z][x + z] != side: break
                    streak.append((x + z, y + z))
                if len(streak) == K: STREAKS.append(streak)

                # try the streak going 'down'
                streak = []
                for z in range(0, K):
                    if y + z >= h: break
                    if state[y + z][x] != " " and state[y + z][x] != side: break
                    streak.append((x, y + z))
                if len(streak) == K: STREAKS.append(streak)
        return STREAKS

    def make_remark(self, state, move, turn, _remarks):

        # get useful variables
        remark = "Nice move." # default
        index = turn % len(self.players)
        new_state = deep_copy(state)
        (y, x) = move
        new_state[y][x] = self.symbol
        score = self.eval(new_state)
        old_score = self.previous_score
        self.previous_score = score
        diff = score - old_score
        limit = self.k  * 2

        # build other players remarks in reverse order
        remarks = []
        for i in range(1, len(self.players)):
            j = (turn - i) % len(self.players)
            remarks.append((self.players[j], _remarks[j]))


        for ((player, symbol), remark) in remarks:
            if turn == 0: break
            wordlist = lang.to_wordlist(remark)
            inverse = lang.invert(wordlist)

            if self.name().lower() not in wordlist:
                if random.randint(0, 10) <= 2: break
                if random.randint(0, 10) <= 2: continue

            #
            # see if there is a question
            #

            if wordlist[0:3] == ["how", "are", "you"]:
                if score > self.k:
                    return "Awesome!"
                elif score < self.k:
                    return "Not so great."
                else:
                    return "I'm doing fine."

            if wordlist[0:1] == ["how"]:
                if wordlist[1] in ["do", "did"]: inverse = inverse[1:]
                inverse = filter(lambda w: w != "me" and w != self.symbol.lower(), inverse[1:])
                return ("I " + " ".join(inverse) + " by " + EXPLANATION[random.randint(0, len(EXPLANATION) - 1)]).format(player.name())

            if wordlist[0:1] == ["why"]:
                inverse = filter(lambda w: w != "me" and w != self.symbol.lower(), inverse[1:])
                return ("I " + " ".join(inverse) + " because " + REASON[random.randint(0, len(REASON) - 1)]).format(player.name())

            if wordlist[0:1] == ["did"]:
                if score > self.k:
                    return ("I did, because " + REASON[random.randint(0, len(REASON) - 1)]).format(player.name())
                elif score < -self.k:
                    return ("I didn't, because " + REASON[random.randint(0, len(REASON) - 1)]).format(player.name())

            if wordlist[0:1] == ["do"]:
                if score > self.k:
                    return ("I do, because " + REASON[random.randint(0, len(REASON) - 1)]).format(player.name())
                elif score < -self.k:
                    return ("I don't, because " + REASON[random.randint(0, len(REASON) - 1)]).format(player.name())

            if len(wordlist) == 0:
                return "Why so silent {0}?".format(player.name())

            if "good" in wordlist or "bad" in wordlist:
                return "I know {0}!".format(player.name())

        if diff > limit:
            return GOOD_TWIST[random.randint(0, len(GOOD_TWIST) - 1)].format(player.name())

        if diff < -limit:
            return BAD_TWIST[random.randint(0, len(BAD_TWIST) - 1)].format(player.name())

        if score > self.k:
            return GOOD[random.randint(0, len(GOOD) - 1)].format(player.name())

        if score > -self.k:
            return BAD[random.randint(0, len(BAD) - 1)].format(player.name())

        return MEH[random.randint(0, len(MEH) - 1)].format(player.name())


'''
Deep copy the two dimensional board state
'''
def deep_copy(state):
    return [s[:] for s in state]


'''
Count how many pieces of a side are in a streak
Assumed that the streak is valid (e.g. only " " or side pieces)
'''
def streak_score(streak, state, side):
    count = 0
    for x,y in streak:
        if state[y][x] == side: count += 1
        elif state[y][x] == " ": continue
    return count
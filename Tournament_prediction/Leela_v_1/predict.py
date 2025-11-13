# import sklearn
import pandas as pd
import numpy as np
import random
import itertools as it

# v1 - predict only by elo
player_elos  = pd.read_csv("Data/Elo/cur_elo.csv")

with open("Leela_v_1/tournament_names.txt", 'r') as f:
    tournament = [int(x.strip()) for x in f.readlines()]
    
# def play_game(a,b):
#     """Plays the game and prints the outcome -> 1 = a won."""
#     w = 1/(1+np.pow(10,(b-a)/400))
#     if(random.uniform(0,1)<w):
#         return 1
#     return 0

def single_elim(players, player_elos): #Not shuffled
    # n = len(players)
    outcome = []
    player_in_tournament = players.copy()
    player_elos_in_tournament = player_elos.copy()
    # print(player_in_tournament)
    # print(player_elos_in_tournament)
    d = {idx: value for idx, value in enumerate(player_in_tournament)}
    while len(player_in_tournament)>1:
        n = len(player_in_tournament)
        ind = []
        for i in range(0,n,2):
            if(random.uniform(0,1)< (1/(1+np.pow(10,(player_elos_in_tournament[i+1]-player_elos_in_tournament[i])/400)))):
                ind.append(i+1)
                # outcome.append(player_in_tournament[i+1])
            else:
                ind.append(i)
                # outcome.append(player_in_tournament[i])
        ind = sorted(ind, reverse=True)
        for u in ind:
            # return
            outcome.append(player_in_tournament.pop(u))
            player_elos_in_tournament.pop(u)
    # print(player_in_tournament[0] , "Has won the tournament")
    
    outcome.append(player_in_tournament[0])
    # print("Outcome", outcome)
    return outcome[::-1]


def simulate_tournament():
    players = player_elos[player_elos["Player"].isin(tournament)]
    # print(len(players))
    # players_elos = player_elos[player_elos["Player"]==tournament[0]]["Elo"]
    d = {player_id: i for i,player_id in enumerate(players["Player"])}
    print("Player elos: ",players["Elo"].tolist())
    print("Player id: ",players["Player"].tolist())
    player_pos = np.zeros((len(players),len(players)))
    # print(player_pos, d)
    # print("Outcome", random_elim(tournament,players["Elo"].tolist(), [], 1))
    # print("Outcome", single_elim(tournament,players["Elo"].tolist()))
    
    # print(results)
    
    for i in range(100000):
        # print(tournament, players["Elo"].tolist())
        # print(len(players))
        
        indices = list(range(len(players)))
        random.shuffle(indices)
        results = single_elim([tournament[v] for v in indices],[players["Elo"].tolist()[v] for v in indices])
        # print(results)
        # print(results)
        # print(random.uniform(0,1))
        for j,res in enumerate(results):
            # print(j, d[res])
            player_pos[d[res]][j] +=1
    print(player_pos)
    # print(players)
    
        
simulate_tournament()
        
        
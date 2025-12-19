# import sklearn
import pandas as pd
import numpy as np
import random
import itertools as it

# v1 - predict only by elo
player_elos  = pd.read_csv("Data/Elo/cur_elo.csv")

with open("Leela_v_1/tournament_names.txt", 'r') as f:
    tournament = [int(x.strip()) for x in f.readlines()]

def single_elim(players, player_elos, player_prob): #Not shuffled
    outcome = []
    player_in_tournament = players.copy()
    player_elos_in_tournament = player_elos.copy()
    d = {idx: value for idx, value in enumerate(player_in_tournament)}
    while len(player_in_tournament)>1:
        n = len(player_in_tournament)
        ind = []
        for i in range(0,n,2):
            #can precompute this matrix of mutual matches
            # print(player_elos)
            val = player_prob[i][i+1]#(1/(1+np.pow(10,(player_elos_in_tournament[i+1]-player_elos_in_tournament[i])/400)))
            print("Playing: ", player_elos[i+1], player_elos[i], val, i)
            if(random.uniform(0,1)< val):
                ind.append(i+1)
            else:
                ind.append(i)
        ind = sorted(ind, reverse=True)
        for u in ind:
            outcome.append(player_in_tournament.pop(u))
            player_elos_in_tournament.pop(u)
    # print(player_in_tournament[0] , "Has won the tournament")
    
    outcome.append(player_in_tournament[0])
    # print("Outcome", outcome)
    return outcome[::-1]


def simulate_tournament(N):
    """Plays a whole tournament."""
    
    players = player_elos[player_elos["Player"].isin(tournament)]
    player_in_tour_elos = players["Elo"].tolist()
    d = {player_id: i for i,player_id in enumerate(players["Player"])}
    print("Player elos: ",players["Elo"].tolist())
    print("Player id: ",players["Player"].tolist())
    player_pos = np.zeros((len(players),len(players)))
    
    n = len(players)
    player_prob = np.zeros((n,n))
    for i in range(n):
        for j in range(i):
            val = 1/(1+np.pow(10,(player_in_tour_elos[j]-player_in_tour_elos[i])/400))
            player_prob[i][j] = val
            player_prob[j][i] = 1-val
    # player_prob
    # print(player_prob)
    # print(player_in_tour_elos)
            
    # return 
    print(player_prob)
    for i in range(N):
        indices = list(range(len(players)))
        random.shuffle(indices)
        results = single_elim([tournament[v] for v in indices],[player_in_tour_elos[v] for v in indices], player_prob)
        for j,res in enumerate(results):
            # print(j, d[res])
            player_pos[d[res]][j] +=1
    return player_pos
    # print(players)
    
        

        
def compute_probability_tournament(player_pos):
    #very basic, using marginal probs.
    #Assuming independence across positions
    player_pos_matrix = np.matrix(player_pos)
    n = np.sum(player_pos_matrix) // len(player_pos_matrix)
    player_pos_matrix /=n
    prob = 1
    player_assigned = []
    ind = 0
    for i in range(len(player_pos_matrix)): #Iterating over positions
        ind = np.argmax(player_pos_matrix[:,i])
        prob*=player_pos_matrix[ind, i]
        player_assigned.append(ind)
        player_pos_matrix[ind,:] =0
    
    print("The most likely probability is : ", prob, player_assigned)
    
player_pos = simulate_tournament(1)
compute_probability_tournament(player_pos)

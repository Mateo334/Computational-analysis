import os
import pandas as pd
import hashlib
import ast

start_elo = 1000
def hash_id(x):
    return int(hashlib.sha256(x.encode()).hexdigest(), 16) % (10**12)

def initialize_elo():
    """Reads all the results and gathers all players_elo ever on tour - init to start_elo""" 
    players_elo = []
    for tour in os.listdir("Data/Results"):
        if(tour.endswith(".csv")):
            tournament = pd.read_csv(f"Data/Results/{tour}")
            if(players_elo):
                players_elo = pd.unique(pd.concat([players_elo, tournament["White"], tournament["Black"]]))
            else:
                players_elo = pd.unique(pd.concat([tournament["White"], tournament["Black"]]))
    players_elo = pd.DataFrame(players_elo)
    players_elo["Elo"] = 1000.0
    players_elo.columns=["Player", "Elo"] 
    players_elo["Player Name"] = players_elo["Player"]
    players_elo["Player"] = players_elo["Player"].apply(hash_id)#Need to also make a dictionary for this to be invertible...
    players_elo.to_csv("Data/Elo/cur_elo.csv") 
    return players_elo



players_elo = pd.read_csv(f"Data/Elo/cur_elo.csv", index_col = 0) #Elos are initialized
# players_elo = initialize_elo() #Need to initialize first

if os.path.getsize("Data/Elo/player_head.csv") > 0:
    player_head = pd.read_csv("Data/Elo/player_head.csv", index_col=0)
    player_head["Opponent"] = player_head["Opponent"].apply(ast.literal_eval)
    player_head["Variation"] = player_head["Variation"].apply(ast.literal_eval)
else:
    player_head = pd.DataFrame(columns=["Player", "Variation", "Opponent"])#w/l/r
    player_head["Player"] = players_elo["Player"]
    player_head["Opponent"] = [[[ ] for _ in range(3)] for _ in range(len(player_head))]
    player_head["Variation"] = [[[ ] for _ in range(3)] for _ in range(len(player_head))]

import numpy as np
def compute_data_from_tournament(tour):
    global players_elo, player_head
    
    #OR can just find all unique matches for each player and update both players_elo that played this 
    # """First we put our elo in place of the tour and then update them."""
    """For each match in tour we look up the player elos and depending 
    on the outcome, we update them."""
    w_out_dict = {"1-0":1, "0-1": 0, "1/2-1/2": 0.5}
    b_out_dict = {"0-1":0, "1-0": 1, "1/2-1/2": 2}
    
    n_player_id = players_elo["Player"].to_numpy()
    n_player_elo = players_elo["Elo"].to_numpy(dtype=float)
    
    id_in_index = {pid: i for i, pid in enumerate(n_player_id)}
    
    w_index = [id_in_index[x] for x in tour["White"]]
    b_index = [id_in_index[x] for x in tour["Black"]]
    
    outcomes = np.array([w_out_dict[x] for x in tour["Result"]])
    
    w_elo = n_player_elo[w_index]
    b_elo = n_player_elo[b_index]
    
    k = 32
    w_exp  = 1/(1+np.pow(10,(b_elo-w_elo)/400))
    b_exp = 1-w_exp
    
    w_chg = k*(outcomes-w_exp)
    b_chg = k*(1-outcomes-b_exp)
    np.add.at(n_player_elo,w_index, w_chg)
    np.add.at(n_player_elo,b_index, b_chg)
    
    
    players_elo["Elo"] = n_player_elo

    w_out_map = {"1-0": 0, "0-1": 1, "1/2-1/2": 2}
    b_out_map = {"1-0": 1, "0-1": 0, "1/2-1/2": 2}
    opp_dict = {}
    for player_id in n_player_id.tolist():
        opp_dict[player_id] = [[],[],[]]
        
    for _, row in tour.iterrows():
        w_out = row["Result"]
        
        w_id = row["White"]
        b_id = row["Black"]
        opp_dict[w_id][w_out_map[w_out]].append(row["Black"])
        opp_dict[b_id][b_out_map[w_out]].append(row["White"])
    # 
    for player_id in n_player_id.tolist():
        for i in range(3):
            player_head.at[id_in_index[player_id],"Opponent"][i].extend(opp_dict[player_id][i])
        
    

def iterate_tour():
    """Iterates through all .csv files"""
    for index, tour in enumerate(os.listdir("Data/Results")):
        
        if(tour.endswith(".csv")):
            tournament = pd.read_csv(f"Data/Results/{tour}")
            tournament["Black"] = tournament["Black"].apply(hash_id)
            tournament["White"] = tournament["White"].apply(hash_id)
            compute_data_from_tournament(tournament)
        print("Progress: ", index, len(os.listdir("Data/Results")))
            
iterate_tour()
players_elo = players_elo.sort_values(by="Elo", ascending=False)
players_elo.to_csv("Data/Elo/cur_elo.csv")
player_head.to_csv("Data/Elo/player_head.csv")
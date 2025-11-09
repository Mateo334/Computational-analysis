import os
import pandas as pd
import math
import hashlib
#Need to hash the matches already calculated to fin_matches.txt and then check if cur is in there. 
#If yes, can skip the file whole, move to next in folder
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


import ast
# players_elo = pd.read_csv(f"Data/Elo/cur_elo.csv") #Elos are initialized
players_elo = initialize_elo() #Need to initialize first

if os.path.getsize("Data/Elo/player_head.csv") > 0:
    player_head = pd.read_csv("Data/Elo/player_head.csv", index_col=0)
    player_head["Opponent"] = player_head["Opponent"].apply(ast.literal_eval)
    player_head["Variation"] = player_head["Variation"].apply(ast.literal_eval)
else:
    player_head = pd.DataFrame(columns=["Player", "Variation", "Opponent"])#w/l/r
    player_head["Player"] = players_elo["Player"]
    player_head["Opponent"] = [[[ ] for _ in range(3)] for _ in range(len(player_head))]
    player_head["Variation"] = [[[ ] for _ in range(3)] for _ in range(len(player_head))]


    



def elo_func(white_elo,black_elo,out):
    """Calculates the elo change after a match."""
    expect_white = 1/(1+math.pow(10,(black_elo-white_elo)/400))
    expect_black = 1/(1+math.pow(10,(-black_elo+white_elo)/400))
    k = 32 #will not be a constant later on... based on the number of matches played
    
    if("2" in out):
        actual_white = 0.5
        actual_black = 0.5
        # return 
    elif(out[0]==1):
        actual_white = 1
        actual_black = 0
    else:
        actual_white = 1
        actual_black = 0
        
    return k*(actual_white-expect_white), k*(actual_black - expect_black)

            
def compute_data_from_tournament(tour):
    global players_elo, player_head
    out_dict = {"1-0":0, "0-1": 1, "1/2-1/2": 2}
    #OR can just find all unique matches for each player and update both players_elo that played this 
    # """First we put our elo in place of the tour and then update them."""
    """For each match in tour we look up the player elos and depending 
    on the outcome, we update them."""
    for _, row in tour.iterrows():
        # print(players_elo["Player"],row["White"])
        white = players_elo["Player"] == row["White"]
        black = players_elo["Player"] == row["Black"]
        
        white_elo = players_elo[white]["Elo"]
        black_elo = players_elo[black]["Elo"]
        
        white_id = players_elo[white]["Player"].iloc[0]
        black_id = players_elo[black]["Player"].iloc[0]

        out = row["Result"]
        # print(out, out_dict[out])
        res = elo_func(white_elo.iat[0], black_elo.iat[0], str(out))
        players_elo.loc[white, "Elo"]  += float(res[0])
        players_elo.loc[black, "Elo"]  += float(res[1])
        
        ind_w = out_dict[out]
        ind_b = 2 if ind_w==2 else 1-ind_w
        
        index_w = player_head.index[player_head["Player"] == white_id][0]
        player_head.at[index_w, "Opponent"][ind_w].append(row["Black"])
        index_b = player_head.index[player_head["Player"] == black_id][0]
        player_head.at[index_b, "Opponent"][ind_b].append(row["White"])

        
        
        
        
        # if(row["White"] in players_elo["Player"].values and row["Black"] in players_elo["Player"].values):
        #     white_prob = 1/(1+math.pow(10,(black_elo.iat[0]-white_elo.iat[0])/400))
            # return white_prob, 1-white_prob
        

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
players_elo.to_csv("Data/Elo/cur_elo.csv")
player_head.to_csv("Data/Elo/player_head.csv")
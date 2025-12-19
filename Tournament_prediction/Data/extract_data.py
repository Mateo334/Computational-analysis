import chess.pgn
import pandas as pd
import os

games = []
# path = "twic1617"
# with open(f"Data/{path}g/{path}.pgn", encoding="utf-8") as pgn:
#     while True:
#         game = chess.pgn.read_game(pgn)
#         if game is None:
#             break
#         headers = game.headers
#         games.append({
#             "Date": headers.get("Date"),
#             "White": headers.get("White"),
#             "Black": headers.get("Black"),
#             "Result": headers.get("Result"),
#             "WhiteElo": headers.get("WhiteElo"),
#             "BlackElo": headers.get("BlackElo")
#         })

# pd.DataFrame(games).to_csv("Data/Results/{path}.csv", index=False)
path = "twic1617"
with open(f"Data/{path}g/{path}.pgn", encoding="utf-8") as pgn:
    while True:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break
        headers = game.headers
        games.append({
            "Date": headers.get("Date"),
            "White": headers.get("White"),
            "Black": headers.get("Black"),
            "Result": headers.get("Result"),
            "WhiteElo": headers.get("WhiteElo"),
            "BlackElo": headers.get("BlackElo"),
            "Variation": headers.get("Variation")
            # "Game": headers.get("") #Missing the played position
        })

pd.DataFrame(games).to_csv(f"Data/Games/{path}.csv", index=False)

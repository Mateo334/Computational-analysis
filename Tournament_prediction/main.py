import os


with open("Data/matches.txt") as file:
    matches = [line.strip() for line in file.readlines()]
print(matches)


# Run this to extract the pgn 
# pgn-extract --filter --output results.txt --nosetup --nomovenumbers --noresults \
#   --format "%d,%w,%b,%r,%we,%be\n" lichess_2025-10.pgn


# Take some previous data, extract them, compute elo and head to head
# then take the newer data and try to either train an ML model, or just predict each match
# Finally plot the results for various types of models
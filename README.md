# LittleBattle
Intro:
A turn based board game for two players based on python.

Structure:
config.txt - A txt file that defines initial resources for each player and also contains the initial resource cords on the gameboard.
file_loading_test.py - a testing .py file which reads all the invalid config.txt files from the folder "invalid files", and pass them into
                        little_battle.py to test the result of initial configuration loading.  
little_battle.py - the main file that execute the game.

How to run Little_battle.py:
by using commandline argument, open terminal and input the following: python little_battle.py config.txt"

Rules:
1. The game is initialized with a map with resources and two players
2. The winning condition is to capture the other player’s home base by an army.
3. There are two stages including “Recruit Armies” and “Move Armies” in a player’s turn
4. In stage “Recruit Armies”, each player can recruit armies and only place the newly recruited armies
next to their home base (4 positions surrounding the home base)
5. Recruiting armies costs resources
6. There are three types of resources on the map: wood (W), food(F), gold(G)
7. Each player initially has 2W, 2F and 2G
8. There are four types of soldiers: Spearman (S) costs 1W, 1F; Archer (A) costs 1W, 1G; Knight (K) 
costs 1F, 1G, Scout (T) costs 1W, 1F, 1G
9.Spearman (S) counters Knight (K); Knight (K) counters Archer (A); Archer (A) counters Spearman 
(S); All other types of armies counter Scout (T); The table below shows the outcome of a fight:
10.  In stage “Move Armies”, each Spearman (S), Archer (A), and Knight (K) can move one step in 
each turn while Scout (T) can move up to two steps (one step or two steps in the same direction)
but move only once
11.  Each player can command an army to collect resources

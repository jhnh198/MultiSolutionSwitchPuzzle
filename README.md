# MultiSolutionSwitchPuzzle
Pygame project, switch and puzzle sequence changes at set intervals

A Switch Puzzle
10/16/2022
by jhnh198, https://github.com/jhnh198
Uses references from Tech With Tim, techwithtim.net pygame tutorials.
Image and audio assets are from Kenney Free Assets:  Kenney.nl.assets

This is a proof of concept for a puzzle that could be implemented in a game, such as a dungeon crawler.

The object of the game is to hit the switches in the right order to solve the puzzle
The switches have two properties; a number and a color
When the player hits the switch, either the correct number in the sequence or the correct color is valid, but not both
Each switch can solve 1 part of the puzzle sequence.

Easier puzzles have less random probablity and change slower.
Harder puzzles can be made by increasing the frequency of randomness for switches and puzzle

WASD to move
Space to use a switch when the player is touching the switch
Esc or closing the window exits the game



Things that could be added:
-  adjust probability with randrange for numbers and symbols. then you can shorten the cycle / cooldown time
    numbers should change less often as symbols are easier to deal with and 
    players will more than likely use symbols instead because it's easier.
- Add a single timer for the puzzle and switch cooldowns. remove the timer from each piece. 
- make a temporary set that the random changes pull from for unique set of changes, rather than having duplicate values
- possible to create a 'puzzle' class that has both the puzzle and switches in there, but it may complicate things.
- potentially can make it so left and right changes the properties so the player has some ability to manipulate them
reset field: switches only reset random counter if the player is in that field. forcing the player to move away from
    switches instead of camping them

- would be interesting to add mazes and enemies
-can add levels and maps later 



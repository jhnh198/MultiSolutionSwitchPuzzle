# MultiSolutionSwitchPuzzle
Pygame project, switch and puzzle sequence changes at set intervals

A Switch Puzzle

by jhnh198, https://github.com/jhnh198

Uses references from Tech With Tim, techwithtim.net pygame tutorials.
Image and audio assets are from Kenney Free Assets:  Kenney.nl.assets

This is a proof of concept for a puzzle that could be implemented in a game, such as a dungeon crawler.
There may be some similarity to a sliding puzzle, but the randomness can be sneaky if you do not tell the player.
The properties will change without any indication, so by the time the player reaches their goal, the value that is needed has changed.
This could be very difficult and frustrating as the player may have to go from place to place only to find the piece they needed is no longer there.

The idea for it was meant to be to simulate dream experiences where details change on their own, so this sort of idea could be implemented in that kind of game 
where things about the world are uncertain. 

The object of the game is to hit the switches in the right order to solve the puzzle
The switches have two properties; a number and a color
When the player hits the switch, either the correct number in the sequence or the correct color is valid, but not both
Each switch can solve 1 part of the puzzle sequence.

Easier puzzles have less random probablity and change slower.
Harder puzzles can be made by increasing the frequency of randomness for switches and puzzle

WASD to move
Space to use a switch when the player is touching the switch
Esc or closing the window exits the game


Things that could be added/tweaked:
-  adjust probability with randrange for numbers and symbols. then you can shorten the cycle / cooldown time
    numbers should change less often as symbols are easier to deal with and 
    players will more than likely use symbols instead because it's easier.
- Add a single timer for the puzzle and switch cooldowns. remove the timer from each piece. 
- make a temporary set that the random changes pull from for unique set of changes, rather than having duplicate values
- create a 'puzzle' class that has both the puzzle and switches and all the initial values in there
- potentially can make it so left and right changes the properties so the player has some limited ability to manipulate them
-  Add a reset field: switches only reset random counter if the player is in that field. forcing the player to move away from
    switches instead of camping them

- Add mazes, obstacles and enemies
- New maps
- Add progression, easy to difficult/ randomness on switches that may change at random frame intervals, some less than frame perfect and would change before the player reaches them 



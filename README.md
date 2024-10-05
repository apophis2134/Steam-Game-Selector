<a name="top"></a>
# 🚀 About
* Do you play games with friends on Steam?
* Are you and your friends **_clueless_** on what the heck you want to play [sometimes]?
* **Well, do I have the solution for _YOU_!**

THIS python script (with C integration) will allow for YOU to pick a game randomly from your Steam Library!!
Worried it'll pick something you have but your friends dont? WELL GUESS WHAT?! 

 ### **This script will only select from a pool of games that are the same between you and your friends!**

That's right, no more spending forever waiting for someone to make a decision, all you need to do is:
* Plug you and your friends' Steam ID's into the .env file
* Swap the Steam API key placeholder in the .env file with your own
* Ensure the GameSelector.py, wheel.so, and .env files are all in the same directory
*  **Run the script!**

My future planning for this includes adding:
* User-provided Steam usernames (via prompt/input of some sort) to eliminate need to plug in Steam IDs manually.
* Make the wheel nicer looking.
* Name abbreviation on the wheel
* Pop-up to display the game that won!

Features that haven't been thought through yet:
Filtering - There are many ways this can go, from genre to average time played among all users.
StartFromApp - Option to locate and start the selected game on user confirmation
History - Option to only allow a game to be selected once, if user spins again the game is removed from pool (or something similar)

[Back to top](#top)

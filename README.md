## DiscordGuess Remastered
 Meet, DiscordGuess Remastered!

⚠️ Highly recommended to start guess from the second account (twink) ⚠️

This tool allows you to guess the Discriminator of Discord accounts (the numbers at the end) based on their Username. It uses the "Add Friend" feature to test for valid Discord Tags.

Then... what updated in DiscordGuess (Remastered)?
1. Prevent ban (adding success list log in format USERNAME.txt) because two friend request sent = ban.
2. Added number to start without waiting for number when already checked.
3. Changed recommend delay from 10 second to 15 second.
4. Added log file. (Helps if your PC is running 24/7 to guess)
5. And small fixes.

## Usage
- pip install -r requirements.txt
- python3 discordguess.py

## Notes
* You will need your Token to be able to send valid requests.
* Discord has a 10 requests/minute rate limit on the Add Friend function. Rate limiting delays are implemented, but use a 15 second delay to avoid suspicion.

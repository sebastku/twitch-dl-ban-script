# twitch-dl-ban-script
This is a script that may help you moderating a Twitch chat if the chat gets flooded with dozens of unwanted messages.
For all incoming messages it determines how similar they are to phrases of your blacklist and bans them automatically using the [Damerau–Levenshtein distance](https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance).

## Getting started
This script is written in [Python](https://www.python.org/). If not already done, please install Python 3.6 or higher in order to run the script.

Additionally you need to install the IRC library as well as jellyfish through pip:

```sh
$ pip install -r requirements.txt
```

Copy the file `config.py.example` to `config.py` and adjust it accordingly. You will need an OAuth access token in order to connect to the chat which can be generated by the [Twitch Chat OAuth Password Generator](https://twitchapps.com/tmi/).

Every channel you want to use this on needs a directory with the name of the channel in all lowercase characters. Within this directory you need a user whitelist `whitelist.txt` and a blacklist for usernames `blacklist-users.txt` and at least one blacklist for unwanted phrases `blacklist-phrase-1.txt` you want to compare to.

You can also create additional blacklists for phrases `blacklist-phrase-<no.>.txt` in order to group similar ones to keep better track of them.

## Usage
After everything is set up just run
```sh
$ python banscript.py <channel>
```
Where `<channel>` is to be replaced with the channel you want to moderate with this script.

# BakaBT Description Generator
This tool is intended for automated, fast, and most importantly, accurate generation of torrent descriptions for BakaBT tracker.

For now, it's still in very early alpha, but i intend to work on it until it becomes so easy to use that it'll be a nobrainer to go for it instead of manually typing HTML code.

### Usage
##### Cloning the repo and installing dependencies: 

    git clone https://github.com/w1kl4s/DescriptionGenerator && cd DescriptionGenerator
    pip3 install -r requirements.txt
You will need AniDB account. If you don't have one, create it. After that you need to provide your login and password in `src/settings.py` file.
You can encrypt your connection using AniDB API Client page. If you wish to do so, generate client key and put it in `src/settings.py` as well.

That should be it. You can start using the tool!
#### Usage, for real this time
    python3 src/main.py /path/to/directory
This will create data.txt file in your current directory. Progress of hashing and file query is displayed.
Speed of hashing depends heavily on read speed of directory (For example, i can hash with about 300 MB/s when directory is on my SSD, but if i try it with location over network, it can be as low as single megabytes per second.)

New fancy colored logs and stuff! Preview of what it looks like right now.

Current version already runs well! It takes file in templates folder, and puts parsed data in new HTML file in Generated Descriptions folder.

Mind that i put black background in HTML file for sake of visibility after generation. After you put proper background image, it will go away.
![Example output:](https://i.imgur.com/1cUl74F.png)

### Current State and TODO

- [x] Using collections instead of filthy dictionaries

- [x] Implement logging

- [x] Implement proper exception classes

- [x] Verification of each file with release information

- [x] Fetching of most basic data from AniDB

- [x] Writing obtained data to HTML template

- [x] Acquiring missing data from mediainfo (Framerate, aspect ratio, audio sample rate, channels, subtitle format)

- [x] Parsing every file data to get average values for whole release (video bitrate, audio bitrate)

- [x] Generating links for other sites (Anime News Network, AnimePlanet, MAL) (Partially done i guess, MAL and AnimePlanet need search instead of just pasting ID from AniDB)

- [x] Fetching pages of director and studio

- [ ] Fetching description either from ANN, AP, or MAL (for user to choose)

- [ ] Implementing multithreading for faster hashing and querying rate
### Limitations
Main limitation right now is AniDB API which does not contain all information that is needed. Also, it doesn't allow fast querying (Wiki says that it allows one request per 4 seconds, which is a lot). I'm using Yumemi Client for easier management of this ([Source Code](https://github.com/fpob/yumemi)).

Right now, it doesn't check for extra files as well (Openings, Endings, etc), since AniDB API doesn't include those in episode number. Hashes of those files are still calculated and they will be fetched just like normal episodes, so having them in checked directory won't interfere with data parsing for main release itself.

## Help!

I am by no means a proper developer. I work as a sysadmin, so i have a lot of experience with Python, but not when it comes to writing a proper project from scratch. It would be great if someone who actually knows how to do that stuff properly came here and complained about it. I am open to suggestions how to improve it and make it a proper pythonic application.


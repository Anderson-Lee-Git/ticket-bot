# ticket-bot
## Installation
1. Clone this repository
```
git clone https://github.com/Anderson-Lee-Git/ticket-bot.git
```
2. Install Chrome driver
```
brew install --cask chromedriver
```
## Run
1. Start Chrome with remote debugging enabled. On the terminal, run this command
```
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_debug_profile"
```
2. Open a new terminal window and enter the repository directory
```
cd [path to directory]
```
* Note: You could drag and drop the directory on Finder or Desktop to the terminal after typing `cd `.
* Note: Replace the `[]` as well
3. In the repository directory, on the terminal with a different window from 1., run this command
```
python3 bot.py --url [concert page URL]
```
* Note: If you'd like to run 2. again, just keep the terminal window on 1. open. You don't have to run 1. again.
* Note: Replace the bracket as well

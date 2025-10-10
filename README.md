# SingingIron
SingingIron is a bot that implements various funny and helpful features. Including playing music, taking bot-therapy and helping you make intelligent decisions in gaming, coding and more.  
Please don't take this bot seriously as it is also still in very early developement. 
Working features right now include:
- Playing music from Youtube

# Planned features
- Music Queue
- Spotify integration
- Soundboard functionality

# Run Bot
- install dependencies (below)
- Setup dev environment (below)
- run venv
- in venv: `python startBot.py`
- enter api key if not created .env

# Dependencies
- ffmpeg -> converting audio


# Dev Setup
- Clone project
- Create new python venv: `python -m venv /path/to/new/virtual/environment` or `python3 -m venv /path/to/new/virtual/environment`
- Start venv: Linux: `source path/to/venv/bin/activate`
- In venv: Install requirements from requirements.txt: `pip install -r /path/to/requirements.txt`
- If you want to you can create an .env file with your discord api token (`DISCORD_API_TOKEN=YourApiToken`). It will be found and inserted at runtime automatically

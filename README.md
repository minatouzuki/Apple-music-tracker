# Apple Music Tracker — for Windows

See what's playing on your PC and control it from a terminal.
Works with Apple Music, Spotify, YouTube in a browser — anything that
shows up in Windows' media controls (the little popup when you press
a media key).

## Setup (one time)

1. Install Python from https://www.python.org/downloads/
   (on the first installer screen, tick **"Add python.exe to PATH"**)
2. Open PowerShell or Terminal and run:
   ```
   pip install winsdk
   ```
3. Put `nowplaying.py` anywhere you like (Desktop is fine).

## Usage

Open PowerShell/Terminal in the folder with the script, then:

```
python nowplaying.py status     what's playing right now
python nowplaying.py toggle     play / pause
python nowplaying.py next       next track
python nowplaying.py prev       previous track
python nowplaying.py play       play
python nowplaying.py pause      pause
python nowplaying.py watch      live feed — prints every song change
```

Press Ctrl+C to stop `watch` mode.

## Notes

- Needs Windows 10 or 11.
- If it says "Nothing playing", start your music first, then run it again.
- Some apps take a second to register — `watch` mode is the most reliable
  way to see everything.

#!/usr/bin/env python3
"""
Now Playing for Windows
-----------------------
See what's currently playing on your PC and control it from a terminal.

Works with anything that plugs into Windows' media controls:
Apple Music, Spotify, YouTube in a browser, and more.

Setup:
    pip install winsdk

Usage:
    python nowplaying.py status     show the current track
    python nowplaying.py play       play
    python nowplaying.py pause      pause
    python nowplaying.py toggle     play / pause toggle
    python nowplaying.py next       next track
    python nowplaying.py prev       previous track
    python nowplaying.py watch      live feed of track changes (Ctrl+C to stop)
"""

import argparse
import asyncio
import sys

try:
    from winsdk.windows.media.control import (
        GlobalSystemMediaTransportControlsSessionManager as MediaManager,
    )
except ImportError:
    print("This script needs the 'winsdk' package.")
    print("Install it with:  pip install winsdk")
    sys.exit(1)


async def get_session():
    sessions = await MediaManager.request_async()
    return sessions.get_current_session()


async def current_info():
    """Return a dict with the current track info, or None if nothing found."""
    session = await get_session()
    if session is None:
        return None
    try:
        props = await session.try_get_media_properties_async()
    except Exception:
        return None
    info = session.get_playback_info()
    status = (
        info.playback_status.name.lower()
        if info is not None and info.playback_status is not None
        else "unknown"
    )
    return {
        "title": props.title or "",
        "artist": props.artist or "",
        "album": props.album_title or "",
        "status": status,
        "source": getattr(session, "source_app_user_model_id", "") or "",
    }


def show(info):
    if not info or not info["title"]:
        print("Nothing playing right now.")
        return
    symbol = {"playing": chr(9654), "paused": chr(10074)}.get(info["status"], chr(9834))
    line = "%s %s" % (symbol, info["title"])
    if info["artist"]:
        line += " - %s" % info["artist"]
    if info["album"]:
        line += "  (%s)" % info["album"]
    print(line)


async def cmd_status(_args):
    show(await current_info())


async def cmd_control(action):
    session = await get_session()
    if session is None:
        print("Nothing to control - no media session found.")
        return
    actions = {
        "play": session.try_play_async,
        "pause": session.try_pause_async,
        "toggle": session.try_toggle_play_pause_async,
        "next": session.try_next_async,
        "prev": session.try_previous_async,
    }
    try:
        ok = await actions[action]()
    except Exception as exc:
        print("Couldn't send '%s': %s" % (action, exc))
        return
    if ok:
        await asyncio.sleep(0.6)
        show(await current_info())
    else:
        print("The app didn't accept '%s'." % action)


async def cmd_watch(_args):
    print("Watching for track changes - press Ctrl+C to stop.\n")
    last = None
    try:
        while True:
            info = await current_info()
            key = (info["title"], info["artist"], info["status"]) if info else None
            if key != last:
                last = key
                show(info)
            await asyncio.sleep(1.5)
    except KeyboardInterrupt:
        print("\nStopped.")


def main():
    parser = argparse.ArgumentParser(description="See and control what's playing on Windows.")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Show the current track.")
    for name in ("play", "pause", "toggle", "next", "prev"):
        sub.add_parser(name, help="Control playback: %s." % name)
    sub.add_parser("watch", help="Live feed of track changes.")

    args = parser.parse_args()
    if args.command == "status":
        asyncio.run(cmd_status(args))
    elif args.command == "watch":
        asyncio.run(cmd_watch(args))
    else:
        asyncio.run(cmd_control(args.command))


if __name__ == "__main__":
    main()

# Ping Distance

A World of Tanks mod that keeps the distance visible on position pings, the markers placed with the contextual command key (T by default). In the base game the distance only shows while your crosshair is on the marker.

The game already draws that distance itself, but only while a marker is "sticky", which is what it does to the marker in your sights. This mod makes every position ping sticky as soon as it appears and keeps it that way, so the engine keeps drawing a live distance. Off-screen pings stick to the screen edge with an arrow, as the hovered one does in the base game.

It only changes how your team's own pings are drawn. It reads no enemy information.

## Install

Copy `maksforge.ping_distance_<version>.wotmod` into `World_of_Tanks/mods/<game version>/`. No other mods are needed.

## Build

```sh
./build.sh                       # needs Python 2.7, e.g. pyenv install 2.7.18
python2.7 tests/test_patch.py
```

## Support

Questions and bug reports: open an issue in this repository or write to wotmods.support@maksforge.com.

This is a free fan-made mod by MaksForge. It is not affiliated with or endorsed by Wargaming.

# Video Cut Generator

## Requirements

`opencv-python` is used in `generate_cuts` to display movies.

Make sure that `files.py` is in the same folder when scripts are ran, since it is referenced by the other modules.

## generate_cuts

`generate_cuts` displays movies that are referenced in `clips.csv`, starting play at the expected location of the start of the cut and playing the movie again at the expected location of the end of the cut. Use the movie controls to pinpoint the precise location of the cuts, which will then be saved into `cuts.csv`.

Note that the movie will be played 2 seconds prior to the cut to allow for precisely finding the cut location.

### Movie controls

```
Key   | Purpose
----------------------------------------------------------------
Space | Toggle play/pause
    F | Double playback speed
    S | Halve playback speed

    M | Mark movie cut at playback point
    R | Redo cut (starts over at -2 second position)

    Q | Quit application, saving current progress into clips.csv
    K | Skip current cut location (i.e. for nonsensical times)
```

### Usage examples (Windows)

Run commands in a PowerShell window (Shift + right click in folder containing the Python scripts, then click "Open PowerShell Window")

To run generate_cuts in the current folder:

`py generate_cuts.py .`

In another folder:

`py generate_cuts.py /path/to/folder/`
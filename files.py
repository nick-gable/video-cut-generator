"""files: file saving / loading methods"""

import os
import csv


def get_movies(dir: str):
    """Returns a dictionary mapped to the available movies provided from the movies.csv file in specified directory"""
    path = os.path.join(dir, "movies.csv")
    result = {}
    with open(path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            result[row["movie_id"]] = row["video_name"]
    return result


def get_clips(dir: str):
    """Returns list of dictionaries containing information about the clips that need to be generated"""
    path = os.path.join(dir, "clips.csv")
    result = []
    with open(path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            result.append(row)
    return result


def write_cuts(dir: str, cuts):
    """Writes out cuts.csv into provided directory

    Parameter cuts: list of dictionaries"""
    path = os.path.join(dir, "cuts.csv")
    with open(path, 'w') as file:
        writer = csv.DictWriter(
            file, fieldnames=["clip_id", "movie_id", "start_sec", "end_sec"])
        writer.writeheader()
        writer.writerows(cuts)

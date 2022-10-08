import pprint
from copy import deepcopy
import requests
import os

from custom_exception import EmptyMapDownloadError
import osuparser


def get_dataset_info(id):

    path = f"maps/{id}.osu"

    if not os.path.exists("maps"):
        os.makedirs("maps")

    if not os.path.exists(path):
        url = "https://osu.ppy.sh/osu/" + str(id)
        r = requests.get(url, allow_redirects=True)
        if r.text == "":
            raise EmptyMapDownloadError("Unvalid beatmap id")
        open(path, "wb").write(r.content)

    # parser doesn't reset when you call parse and build
    # so you need to instantiate new one every loop
    parser = osuparser.beatmapparser.BeatmapParser()
    parser.parseFile(path)
    parser.build_beatmap()

    data = []
    timing_index = 0
    break_index = 0

    first_skipped = False

    for (index, hit_object) in enumerate(parser.beatmap["hitObjects"]):

        # dataset columns:
        ## posx, posy, dt, bpm, type, duration, length
        # Add dt calculations in the future maybe? I don't think dt timings will impact the results too hard. but we'll see
        # maybe i will do dt exclusive dataset in the future just to try

        # posx, posy
        line = deepcopy(hit_object["position"])

        # bpm
        while timing_index < len(parser.beatmap["timingPoints"]) - 1 and hit_object["startTime"] > parser.beatmap["timingPoints"][timing_index]["offset"]:
            timing_index += 1
        try:
            bpm = parser.beatmap["timingPoints"][timing_index]["bpm"]
        except:
            print("negative first timing point, skipping a step")
            first_skipped = True
            continue

        # dt
        if index == 0 or first_skipped:
            dt = 0
        elif break_index < len(parser.beatmap["breakTimes"]) - 1 and parser.beatmap["breakTimes"][break_index]["startTime"] > hit_object["startTime"]:
            break_index += 1
            dt = last_dt
        else:
            dt = hit_object["startTime"] - last_start_time  # dt
        dt = dt / bpm  # to standartize the dt for maps. bpm data also will be fed to model to account for bpm changes
        line += [dt, bpm]
        last_dt = dt

        if hit_object["object_name"] == "circle":
            line += [0]  # type
            line += [0]  # duration
            line += [0]  # length
            last_start_time = hit_object["startTime"]

        elif hit_object["object_name"] == "slider":
            line += [1]  # type
            line += [hit_object["duration"]]
            line += [hit_object["pixelLength"]]
            last_start_time = hit_object["end_time"]

        elif hit_object["object_name"] == "spinner":
            line += [2]  # type
            line += [0]  # duration
            line += [0]  # length
            last_start_time = hit_object["end_time"]

        data.append(line)

    return data


if __name__ == "__main__":

    dataset = get_dataset_info(10801)
    # pprint.pprint(dataset)

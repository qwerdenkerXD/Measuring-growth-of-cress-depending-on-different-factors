INIT_DATE = 30, 1, 2023, 10, 27
CSV_DELIM = ";"


def main():
    data = getMeasurements()

    assert len(data["H2O"][0]) % 20 == 0,  "Missing measurement in H2O"
    assert len(data["pH"][0]) % 20 == 0,   "Missing measurement in pH"
    assert len(data["NaCl"][0]) % 20 == 0, "Missing measurement in NaCl"

    M_COUNT = len(data["H2O"][0]) // 20  # count of measurements


def getMeasurements() -> dict:
    data = {"H2O": [[], []],  # [x-values, y-values]
            "pH": [[], []],
            "NaCl": [[], []]
            }
    with open("Wuchshohen.csv") as f:
        f.readline()  # skip first line
        for line in f:
            medium, dateTime, height, _ = line.split(CSV_DELIM)
            data[medium][0] += [relTime(dateTime)]
            data[medium][1] += [int(height)]

    return data


def relTime(dateTime: "dd.mm.yyyy, hh:mm") -> "int of minutes":  # for correct positioning on x-axis
    date, time = dateTime.split(", ")
    day, month, _ = date.split(".")
    hours, minutes = time.split(":")
    initDay, initMonth, _, initHours, initMinutes = INIT_DATE

    if int(month) == initMonth:
        day = int(day) - initDay
    else:
        day = int(day) + 31 - initDay

    hours = int(hours) + 24 * day - initHours
    minutes = int(minutes) + 60 * hours - initMinutes

    return minutes


if __name__ == '__main__':
    main()

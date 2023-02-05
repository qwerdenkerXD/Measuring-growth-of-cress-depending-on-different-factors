from matplotlib import pyplot as plot

INIT_DATE = 30, 1, 2023, 10, 27
CSV_DELIM = ";"


def main():
    data = getMeasurements()

    assert len(data["H2O"][0]) % 20 == 0,  "Missing measurement in H2O"
    assert len(data["pH"][0]) % 20 == 0,   "Missing measurement in pH"
    assert len(data["NaCl"][0]) % 20 == 0, "Missing measurement in NaCl"

    plotScattered(data, "ScatterPlot")


def plotScattered(data: dict, outFileName: str) -> "saves plot as png":
    plot.clf()  # clear plot

    M_COUNT = len(data["H2O"][0]) // 20  # count of measurements
    arithMean, median = {}, {}
    for medium in data:  # calculate medians and arith. means of data
        yArith, yMedian, xValues = [], [], []

        for i in range(M_COUNT):
            xValues += [data[medium][0][i * 20]]
            yData = sorted(data[medium][1][i * 20: i * 20 + 20])
            yArith += [sum(yData) / 20]
            yMedian += [(yData[9] + yData[10]) / 2]

        arithMean[medium] = [xValues, yArith]
        median[medium] = [xValues, yMedian]

    MAX_X = data["H2O"][0][-1]
    MAX_Y = max(data["H2O"][1])

    for i in range(2):
        subP = plot.subplot(121 + i)
        subP.title.set_text(["median", "arithmetic mean"][i])
        plot.xlabel("Zeitpunkt in Tagen")
        plot.ylabel("Wachstumshöhe in mm")
        subP.set_xticks([i for i in range(0, MAX_X, 60 * 24)])
        subP.set_xticklabels([i // (60 * 24) for i in range(0, MAX_X, 60 * 24)])
        subP.set_xlim(0, MAX_X)
        subP.set_ylim(0, MAX_Y)
        addWatering(subP)

        for medium in data:
            x_values, y_values = [median, arithMean][i][medium]
            subP.plot(x_values, y_values, marker="o", linestyle="-", label=medium)
            plot.legend(loc="upper left")

    plot.savefig("%s.png" % outFileName)


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


def addWatering(plot) -> None:
    with open("Watering.csv") as f:
        f.readline()
        label = "Watering"
        for line in f:
            dateTime, _ = line.split(CSV_DELIM)
            plot.axvline(relTime(dateTime), label=label)
            label = None


if __name__ == '__main__':
    main()

from matplotlib import pyplot as plot

INIT_DATE = 30, 1, 2023, 10, 27
CSV_DELIM = ";"


def main():
    data = getMeasurements()

    assert len(data["H2O"][0]) % 20 == 0,  "Missing measurement in H2O"
    assert len(data["pH"][0]) % 20 == 0,   "Missing measurement in pH"
    assert len(data["NaCl"][0]) % 20 == 0, "Missing measurement in NaCl"

    plotBoxed(data, "BoxPlot")
    plotScattered(data, "ScatterPlot")
    makeRcompatible(data)  # writes a file for a script from the course


def plotBoxed(data: dict, outFileName: str) -> "saves plot as png":
    plot.clf()

    def splitData(data: dict) -> dict:
        res = {i: [] for i in data}
        for medium in data:
            x, y = data[medium]
            M_COUNT = len(x) // 20  # count of measurements
            for i in range(M_COUNT):
                res[medium] += [[]]
                for j in range(20):
                    res[medium][-1] += [y[i*20 + j]]
        return res

    def findMax(data: dict) -> int:
        maxV = -1
        for medium in data:
            maxInMedium = max(data[medium][1])
            if maxV < maxInMedium:
                maxV = maxInMedium
        return maxV

    MAX_V = findMax(data)
    M_COUNT = len(data["H2O"][0]) // 20  # count of measurements
    pos = [data["H2O"][0][i * 20] for i in range(M_COUNT)]
    data = splitData(data)
    fig, plots = plot.subplots(1, len(data))
    fig.set_size_inches(30,15)
    for medium, subP in zip(data, plots):
        addWatering(subP)
        subP.set_title(medium, fontdict={"fontsize": 25})
        boxP = subP.boxplot(data[medium], positions=pos, widths=400, patch_artist=True)
        for box in boxP["boxes"]:
            box.set_facecolor("white")
        subP.set_xlim(0, pos[-1]+210)
        subP.set_ylim(-4, MAX_V + 2)
        subP.set_xticks([i for i in range(0, pos[-1], 60 * 24)])
        subP.set_xticklabels([i // (60 * 24) for i in range(0, pos[-1], 60 * 24)], fontsize=15)
    plot.savefig("%s.png" % outFileName)


def makeRcompatible(data: dict) -> "writes my_measurements.R":
    M_COUNT = len(data["H2O"][0]) // 20  # count of measurements
    y, x = {i: [] for i in data}, {i: [] for i in data}
    for medium in data:
        for j in range(20):
            day = 1
            arith = 0
            days_measures = 0
            for i in range(M_COUNT):
                if data[medium][0][i*20 + j]//(24*60) == day:
                    y[medium] += [arith/days_measures]
                    x[medium] += [day]
                    day += 1
                    arith = data[medium][1][i*20 + j]
                    days_measures = 1
                else:
                    days_measures += 1
                    arith += data[medium][1][i*20 + j]
            y[medium] += [arith/days_measures]
            x[medium] += [day]
    # assert(day == 6)
    with open("Analyse/my_measurements.csv", "w") as f:
        f.write("Medium,Messtag,Wuchshöhe,Matrikelnummer\n")
        for medium in data:
            xy = sorted(zip(x[medium], y[medium]))
            for xi, yi in xy:
                f.write("%s,%s,%s,%s\n" % ({"H2O": "Normal", "pH": "Acidic", "NaCl": "Salty"}[medium], xi, yi, 2139315))


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
        subP.set_title(["median", "arithmetic mean"][i], fontdict={"fontsize": 25})
        plot.xlabel("Zeitpunkt in Tagen", fontsize=20)
        plot.ylabel("Wachstumshöhe in mm", fontsize=20)
        subP.set_xticks([i for i in range(0, MAX_X, 60 * 24)])
        subP.set_xticklabels([i // (60 * 24) for i in range(0, MAX_X, 60 * 24)], fontsize=15)
        subP.set_xlim(0, MAX_X)
        subP.set_ylim(0, MAX_Y)
        addWatering(subP)

        for medium in data:
            x_values, y_values = [median, arithMean][i][medium]
            subP.plot(x_values, y_values, marker="o", linestyle="-", label=medium)
            plot.legend(loc="upper left", fontsize=15)

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
            if height == "NA":
                height = data[medium][1][-20]  # take NA values as its last measured value
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

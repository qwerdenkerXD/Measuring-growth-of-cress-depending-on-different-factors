from matplotlib import pyplot as plot

INIT_DATE = 30, 1, 2023, 10, 27
CSV_DELIM = ";"
PATH_RESULTS = "Results/"
MEDIUM_EQUIV = {"H2O": ["Normal", "Normal"], "pH": ["Acidic", "Sauer (pH ≈ 5)"], "NaCl": ["Salty", "Salzig (0,1 mol NaCl)"]}
MEDIUMS = list(MEDIUM_EQUIV.keys())
SAMPLES_PER_MED = 20
M_COUNT = None  # gets value in getMeasurements()


def main():
    data = getMeasurements()

    plotBoxed(data, "BoxPlot")
    plotScattered(data, "ScatterPlot")
    makeRcompatible(data)  # writes a file for a script from the course

    normalData = data[MEDIUMS[0]][1]
    print("Degrees of Freedom: %d" % (2 * SAMPLES_PER_MED - 2))
    all_accepted = []
    plot.clf()
    fig, subplots = plot.subplots(1, len(data)-1)
    fig.set_size_inches(30, 15)
    for medium, subP in zip(MEDIUMS[1:], subplots):
        subP.set_title(MEDIUM_EQUIV[medium][1], fontdict={"fontsize": 25})
        subP.set_xlabel("t-Wert", fontsize=20)
        subP.set_ylabel("T(t)", fontsize=20)
        for x, y in zip(subP.get_yticklabels(), subP.get_xticklabels()):
            x.set_fontsize(15)
            y.set_fontsize(15)
        t_value, hypTestRes, accepted = t_test(normalData, data[medium][1][-len(normalData):], subP, (1.687, 2.025))  # quantile values for alpha=5% from https://datatab.de/tutorial/tabelle-t-verteilung
        print("mean t-value for %s and %s: %f\n%s" % (MEDIUMS[0], medium, t_value, hypTestRes))
        all_accepted += [accepted]

    plot.savefig("%st_tests.png" % PATH_RESULTS)

    with open("Results/t_tests.csv", "w") as f:
        f.write("H0;%s;%s\n" % tuple(MEDIUMS[1:]))
        f.write("E(Normal) \\ \\ = E(M);%.2f\\%% akzeptiert;%.2f\\%% akzeptiert\n" % (all_accepted[0][0], all_accepted[1][0]))
        f.write("E(Normal) $<$= E(M);%.2f\\%% akzeptiert;%.2f\\%% akzeptiert\n" % (all_accepted[0][1], all_accepted[1][1]))
        f.write("E(Normal) $>$= E(M);%.2f\\%% akzeptiert;%.2f\\%% akzeptiert\n" % (all_accepted[0][2], all_accepted[1][2]))


def t_test(dataM1: "measurements Medium 1", dataM2: "measurements Medium 2", plot, t_dist_value=(None, None)) -> (float, str, "list of accepted percentages"):
    dataM1 = [dataM1[i*SAMPLES_PER_MED: (i+1)*SAMPLES_PER_MED] for i in range(len(dataM1) // SAMPLES_PER_MED)]
    dataM2 = [dataM2[i*SAMPLES_PER_MED: (i+1)*SAMPLES_PER_MED] for i in range(len(dataM2) // SAMPLES_PER_MED)]
    t_values = []
    for X, Y in zip(dataM1, dataM2):
        if sum(X) or sum(Y):  # t-values when both mediums had no grown seeds are skipped
            m, n = len(X), len(Y)
            arithM1 = sum(X) / m
            arithM2 = sum(Y) / n
            weightedVariance = (sum([(x - arithM1) ** 2 for x in X]) + sum([(y - arithM2) ** 2 for y in Y])) / (m + n - 2)
            if weightedVariance == 0:
                t_values += [0]
            else:
                t_values += [(m * n / (m + n)) ** .5 * (arithM1 - arithM2) / (weightedVariance ** .5)]

    def t_dist(t, gammafuncValue1, gammafuncValue2, degOfFreedom):
        from math import pi
        return gammafuncValue1 / ((degOfFreedom * pi)**.5 * gammafuncValue2) * (1 + t**2/degOfFreedom)**-((degOfFreedom+1)/2)

    hypTest = "Es werden nur Messungen betrachtet, bei denen min. ein Medium Höhen größer 0 aufweist\n"
    accepted = ["nicht getestet", "nicht getestet", "nicht getestet"]
    if t_dist_value != (None, None):
        quant95, quant975 = t_dist_value
        plot.axvline(quant95, color="red", label="95%-Quantil")
        plot.axvline(-quant95, color="red")
        plot.axvline(quant975, color="green", label="97,5%-Quantil")
        plot.axvline(-quant975, color="green")
        plot.legend(loc="upper left", fontsize=15)
        gamma1, gamma2 = 2.772432e+16, 6.402374e+15  # values for 19.5 ((38+1)/2) and 19 (38/2) from https://miniwebtool.com/de/gamma-function-calculator/
        plotTrange = range(round(min(t_values+[-quant975])*1000 - 500), round(max(t_values+[quant975])*1000 + 500), 10)
        plot.plot([t/1000 for t in plotTrange], [t_dist(t/1000, gamma1, gamma2, 38) for t in plotTrange], marker="", color="black")
        print(t_dist(0, gamma1, gamma2, 38))
        if quant975:
            percentage = 0  # how much percent of the measurements contradict the hypothesis
            for v in t_values:
                percentage += v > quant975
                percentage += v < -quant975
                plot.plot(v, t_dist(v, gamma1, gamma2, 38), marker="o", color="blue")
            percentage = 100 * percentage / len(t_values)
            accepted[0] = 100-percentage
            hypTest += "E(X) = E(Y): in %.2f%% aller Messungen akzeptiert, in %.2f%% abgelehnt\n" % (100-percentage, percentage)
        if quant95:
            percentage = 0  # how much percent of the measurements contradict the hypothesis
            for v in t_values:
                percentage += v > quant95
            percentage = 100 * percentage / len(t_values)
            accepted[1] = 100-percentage
            hypTest += "E(X) <= E(Y): in %.2f%% aller Messungen akzeptiert, in %.2f%% abgelehnt\n" % (100-percentage, percentage)
            percentage = 0  # how much percent of the measurements contradict the hypothesis
            for v in t_values:
                percentage += v < -quant95
            percentage = 100 * percentage / len(t_values)
            accepted[2] = 100-percentage
            hypTest += "E(X) >= E(Y): in %.2f%% aller Messungen akzeptiert, in %.2f%% abgelehnt\n" % (100-percentage, percentage)

    arith_t_value = sum(t_values) / len(t_values)
    return arith_t_value, hypTest, accepted


def plotBoxed(data: dict, outFileName: str) -> "saves plot as png":
    plot.clf()

    def splitData(data: dict) -> dict:
        res = {i: [] for i in data}
        for medium in data:
            x, y = data[medium]
            for i in range(M_COUNT):
                res[medium] += [[]]
                for j in range(SAMPLES_PER_MED):
                    res[medium][-1] += [y[i * SAMPLES_PER_MED + j]]
        return res

    def findMax(data: dict) -> int:
        maxV = -1
        for medium in data:
            maxInMedium = max(data[medium][1])
            if maxV < maxInMedium:
                maxV = maxInMedium
        return maxV

    MAX_V = findMax(data)
    firstMediumData = data[MEDIUMS[0]]
    pos = [firstMediumData[0][i * SAMPLES_PER_MED] for i in range(M_COUNT)]
    data = splitData(data)
    fig, plots = plot.subplots(1, len(data))
    fig.set_size_inches(30, 15)
    for medium, subP in zip(data, plots):
        addWatering(subP)
        subP.set_xlabel("Zeitpunkt in Tagen", fontsize=20)
        subP.set_ylabel("Wachstumshöhe in mm", fontsize=20)
        subP.set_title(MEDIUM_EQUIV[medium][1], fontdict={"fontsize": 25})
        boxP = subP.boxplot(data[medium], positions=pos, widths=400, patch_artist=True)
        for box in boxP["boxes"]:
            box.set_facecolor("white")
        subP.set_xlim(0, pos[-1]+210)
        subP.set_ylim(-4, MAX_V + 2)
        subP.set_xticks([i for i in range(0, pos[-1], 60 * 24)])
        # subP.set_xticklabels([i // (60 * 24) for i in range(0, pos[-1], 60 * 24)], fontsize=15)
        for label in subP.get_yticklabels():
            label.set_fontsize(15)
        subP.legend(loc="upper left", fontsize=15)

    plot.savefig("%s%s.png" % (PATH_RESULTS, outFileName))


def makeRcompatible(data: dict) -> "writes my_measurements.R":
    y, x = {i: [] for i in data}, {i: [] for i in data}
    for medium in data:
        for j in range(SAMPLES_PER_MED):
            day = 1
            arith = 0
            days_measures = 0
            for i in range(M_COUNT):
                if data[medium][0][i*SAMPLES_PER_MED + j]//(24*60) == day:
                    y[medium] += [arith/days_measures]
                    x[medium] += [day]
                    day += 1
                    arith = data[medium][1][i*SAMPLES_PER_MED + j]
                    days_measures = 1
                else:
                    days_measures += 1
                    arith += data[medium][1][i*SAMPLES_PER_MED + j]
            y[medium] += [arith/days_measures]
            x[medium] += [day]

    with open("Results/my_measurements.csv", "w") as f:
        f.write("Medium,Messtag,Wuchshöhe,Matrikelnummer\n")
        for medium in data:
            xy = sorted(zip(x[medium], y[medium]))
            for xi, yi in xy:
                f.write("%s,%s,%s,%s\n" % (MEDIUM_EQUIV[medium][0], xi, yi, 2139315))


def plotScattered(data: dict, outFileName: str) -> "saves plot as png":
    plot.clf()  # clear plot

    arithMean, median = {}, {}

    for medium in data:  # calculate medians and arith. means of data
        yArith, yMedian, xValues = [], [], []

        for i in range(M_COUNT):
            xValues += [data[medium][0][i * SAMPLES_PER_MED]]
            yData = sorted(data[medium][1][i * SAMPLES_PER_MED: i * SAMPLES_PER_MED + SAMPLES_PER_MED])
            yArith += [sum(yData) / SAMPLES_PER_MED]
            if SAMPLES_PER_MED % 2 == 0:
                yMedian += [(yData[SAMPLES_PER_MED // 2 - 1] + yData[SAMPLES_PER_MED // 2]) / 2]
            else:
                yMedian += [(yData[SAMPLES_PER_MED // 2]) / 2]

        arithMean[medium] = [xValues, yArith]
        median[medium] = [xValues, yMedian]

    firstMediumData = data[MEDIUMS[0]]
    x, y = firstMediumData
    MAX_X = x[-1]
    MAX_Y = max(y)

    for i in range(2):
        subP = plot.subplot(121 + i)
        subP.set_title(["Mediane", "Arithmetische Mittelwerte"][i], fontdict={"fontsize": 25})
        plot.xlabel("Zeitpunkt in Tagen", fontsize=20)
        plot.ylabel("Wachstumshöhe in mm", fontsize=20)
        subP.set_xticks([i for i in range(0, MAX_X, 60 * 24)])
        subP.set_xticklabels([i // (60 * 24) for i in range(0, MAX_X, 60 * 24)], fontsize=15)
        for label in subP.get_yticklabels():
            label.set_fontsize(15)
        subP.set_xlim(0, MAX_X)
        subP.set_ylim(0, MAX_Y)
        addWatering(subP)

        for medium in data:
            x_values, y_values = [median, arithMean][i][medium]
            subP.plot(x_values, y_values, marker="o", linestyle="-", label=medium)
            subP.legend(loc="upper left", fontsize=15)

    plot.savefig("%s%s.png" % (PATH_RESULTS, outFileName))


def getMeasurements() -> dict:
    global M_COUNT  # will be initialised with an integer

    data = {medium: [[], []] for medium in MEDIUMS}  # [x-values, y-values]

    with open("Wuchshohen.csv") as f:
        f.readline()  # skip first line
        for line in f:
            medium, dateTime, height, _ = line.split(CSV_DELIM)
            data[medium][0] += [relTime(dateTime)]
            if height == "NA":
                height = data[medium][1][-SAMPLES_PER_MED]  # take NA values as its last measured value
            data[medium][1] += [int(height)]

    for medium in data:
        valueCount = len(data[medium][0])
        assert valueCount % 20 == 0, "Missing measurement in %s" % medium
        M_COUNT = valueCount // SAMPLES_PER_MED  # count of measurements

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
        label = "Gießen"
        for line in f:
            dateTime, _ = line.split(CSV_DELIM)
            plot.axvline(relTime(dateTime), label=label)
            label = None


if __name__ == '__main__':
    main()

# This is a modified, shorter version of a script from study course


#' Step 1 - Read MY data:
plant.h.my <- read.table("Analyse/my_measurements.csv", sep = ",", header = TRUE, stringsAsFactors = TRUE)
#' Objects: plant.h.my


#' Step 2 - Read data of all OTHER students:
other.students.measurements <- list.files(path = "Analyse/measurements_other_students", pattern = "*.csv",
    full.names = TRUE, recursive = FALSE)
plant.h.other <- do.call(rbind, lapply(other.students.measurements, function(x) {
    read.table(x, sep = ",", header = TRUE, stringsAsFactors = FALSE)
}))
#' Obejcts: plant.h.other


#' Join my and other students measurements:
plant.h.all <- rbind(plant.h.my, plant.h.other)
#' Objects: plant.h.all

plant.h.all.min <- min(plant.h.all$Wuchshöhe)
plant.h.all.max <- max(plant.h.all$Wuchshöhe)
plant.h.days <- sort(unique(plant.h.all$Messtag))


#' Scatterplot of the three media's time-series, but separating my own
#' data from the others'.
plant.h.other.norm <- plant.h.other[which(plant.h.other$Medium == "Normal"), ]
plant.h.other.salty <- plant.h.other[which(plant.h.other$Medium == "Salty"), ]
plant.h.other.acidic <- plant.h.other[which(plant.h.other$Medium == "Acidic"), ]
plant.h.my.norm <- plant.h.my[which(plant.h.my$Medium == "Normal"), ]
plant.h.my.salty <- plant.h.my[which(plant.h.my$Medium == "Salty"), ]
plant.h.my.acidic <- plant.h.my[which(plant.h.my$Medium == "Acidic"), ]
png("Results/scatterplot_my_vs_others.png", 1000, 1000)
#' other's data:
plot(x = plant.h.other.norm$Messtag, plant.h.other.norm$Wuchshöhe, pch = 21, col = "black",
    ylim = c(plant.h.all.min, plant.h.all.max), xlab = "Tag", ylab = "Wuchshöhe [mm]")
axis(1, at=1:14)
points(x = plant.h.other.salty$Messtag, plant.h.other.salty$Wuchshöhe, pch = 21,
    col = "skyblue")
points(x = plant.h.other.acidic$Messtag, plant.h.other.acidic$Wuchshöhe, pch = 21,
    col = "orange")
#' my data:
points(x = plant.h.my.norm$Messtag, plant.h.my.norm$Wuchshöhe, pch = 23, col = "darkgrey")
points(x = plant.h.my.salty$Messtag, plant.h.my.salty$Wuchshöhe, pch = 23, col = "blue")
points(x = plant.h.my.acidic$Messtag, plant.h.my.acidic$Wuchshöhe, pch = 23, col = "darkred")
#' Draw dashes for the means (averages):
points(x = plant.h.days, y = sapply(plant.h.days, function(day) {
    mean(plant.h.other.norm[which(plant.h.other.norm$Messtag == day), "Wuchshöhe"], na.rm = TRUE)
}), pch = "-", col = "black", cex = 7)
points(x = plant.h.days, y = sapply(plant.h.days, function(day) {
    mean(plant.h.other.salty[which(plant.h.other.salty$Messtag == day), "Wuchshöhe"], na.rm = TRUE)
}), pch = "-", col = "skyblue", cex = 7)
points(x = plant.h.days, y = sapply(plant.h.days, function(day) {
    mean(plant.h.other.acidic[which(plant.h.other.acidic$Messtag == day), "Wuchshöhe"], na.rm = TRUE)
}), pch = "-", col = "orange", cex = 7)
points(x = plant.h.days, y = sapply(plant.h.days, function(day) {
    mean(plant.h.my.norm[which(plant.h.my.norm$Messtag == day), "Wuchshöhe"], na.rm = TRUE)
}), pch = "-", col = "darkgrey", cex = 7)
points(x = plant.h.days, y = sapply(plant.h.days, function(day) {
    mean(plant.h.my.salty[which(plant.h.my.salty$Messtag == day), "Wuchshöhe"], na.rm = TRUE)
}), pch = "-", col = "blue", cex = 7)
points(x = plant.h.days, y = sapply(plant.h.days, function(day) {
    mean(plant.h.my.acidic[which(plant.h.my.acidic$Messtag == day), "Wuchshöhe"], na.rm = TRUE)
}), pch = "-", col = "darkred", cex = 7)
legend("topleft", legend = c(c("H2O andere", "NaCl andere", "pH andere"),
    c("mein H2O", "mein NaCl", "mein pH")), fill = c("black", "skyblue", "orange",
    "darkgrey", "blue", "darkred"))
dev.off()
#' Open the new file 'scatterplot_time_series_my_versus_others.pdf' and look at
#' the scientific plot!
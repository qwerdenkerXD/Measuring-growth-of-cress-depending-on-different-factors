Reproduktion der aus den erfassten Daten produzierten Ergebnisse:
    Für die Generierung der Ergebnisse und der Hausarbeit müssen folgende Linux
    Befehle in diesem Supplement-Ordner ausgeführt werden:

        # Generierung der Ergebnisse
        python3 Analyse.py
        Rscript my_analysis.R
        # Generierung der Hausarbeit
        cd Hausarbeit
        pdflatex --shell-escape -halt-on-error Hausarbeit.tex
        biber Hausarbeit
        pdflatex --shell-escape -halt-on-error Hausarbeit.tex
        pdflatex --shell-escape -halt-on-error Hausarbeit.tex
        rm *.run.xml *.aux *.bbl *.bcf *.blg *.out *.lot *.lof *.toc *.log

    Dabei ist zu beachten, dass für python3 das Modul "matplotlib" zur Verfügung
    steht. Zur Installation wurde hier das Modul "pip" verwendet, welches dann
    mit "python3 -m pip install matplotlib==3.5.2" das benötigte Modul in der
    korrekten Version installiert.


Reproduktion der erfassten Daten:
    Für die Erfassung der Daten muss ein Experiment vorbereitet und durchgeführt
    werden. Dazu werden 60 Samen von Gartenkresse gesammelt, 5.85 g NaCl abgewogen
    und 4.5 ml Essigessenz mit pH-Wert 2.65 über 2 Monate dunkel, voneinander
    getrennt, bei Zimmertemperatur gelagert. Nach dieser Zeit werden drei saubere
    Tassen mit Fassungsvermögen 350 ml mit Watte, bestehend aus 100% Baumwolle,
    gefüllt, sodass eine ebene Oberfläche entsteht, die durch den Tassenrand
    begrenzt wird. Auf dieser Oberfläche werden nun Samen von Gartenkresse in einem
    5 * 4 Raster mittels Pinzette positioniert mit etwa 1 cm Abstand zwischen den
    Samen. Anschließend werden drei verschließbare Gläser bereitgestellt, mit
    mindestens 1 Liter Fassungsvermögen, die schon mal für die Aufbewahrung von
    Lebensmitteln benutzt wurden. Das erste Glas wird voll mit Leitungswasser
    aufgefüllt, welches dieselbe Zusammensetzung hat wie am 30.01.2023 in Bingen
    am Rhein in Deutschland. Das Wasser dieser Art wird auch für die folgenden
    Schritte benutzt. Anschließend wird das Salz in das nächste leere Glas gegeben.
    Hinzu werden 100ml Wasser eingefüllt, das Glas geschwenkt, bis das Salz
    vollständig darin gelöst ist und in einen Messbecher mit Fassungsvermögen von
    1 Liter gegossen. Dann wird deutlich weniger als 1 Liter Wasser in das Glas
    gegeben, ausgiebig geschwenkt und auch in den Messbecher gegeben. Nun wird der
    Messbecher leicht geschwenkt und zu 1 Liter mit Wasser aufgefüllt. Das Resultat
    wird nun zurück in das Glas gegeben. Anschließend wird der Messbecher zweimal
    gründlich mit Wasser ausgespült. Dann wird das Essig in das dritte Glas gefüllt,
    mit deutlich weniger als 1 Liter Wasser aufgefüllt und in den Messbecher gegeben.
    Dieser wird geschwenkt und zu 1 Liter aufgefüllt und in das Glas geleert. Alle
    Gläser werden direkt nach der Befüllung mit einem Schraubdeckel verschlossen.
    Die Tassen werden nun so im Raum platziert, dass sie ganztägig durchgehend
    Tageslicht abbekommen, aber nicht direkt in der Sonne oder am offenen Fenster
    stehen. Sie werden in einer Reihe aufgestellt: Wasser, Salzwasser, Essigwasser.
    Ihnen zugehörig werden die entsprechenden Gläser dazugestellt. Ein Foto von der
    Aufstellung wird in Results/preparation.png gespeichert
    Nun beginnt das Experiment mit Tag 0. Es werden folgende Schritte durchgeführt,
    die für 14 Tage mindestens einmal täglich wiederholt wird, wobei exakt einmal
    pro Tag gegossen wird (Schritt 2 und 3):
        1. Messen und notieren der Wuchshöhen jedes einzelnen Samens der neutralen
           Probe mit dem Maßband
        2. gleichmäßiges Gießen des Samenrasters mit drei Teelöffeln aus dem neutralen
           Medium
        3. Reinigen des genutzten Teelöffels (wird ausschließlich für dieses Medium
           verwendet)
        4. anschließendes Wiederholen der vorigen Schritte für die salzige und zum
           Schluss der sauren Probe
    Zudem ist es empfohlen, das Tag 0 Anfang Februar in Bingen am Rhein in Deutschland
    durchgeführt wird.
    Die Messdaten werden in "Wuchshöhen.csv" gespeichert. In die erste Spalte wird der
    Name des Mediums eingetragen, für normales Wasser "H2O", für Salzwasser "NaCl" und
    für Essigwasser "pH". In der zweite Spalte wird der Messtag des Formats
    "TT.MM.YYYY, hh:mm" (T=Tag, M=Monat, Y=Jahr, h=Stunde, m=Minute) erfasst, in
    der Dritten die gemessene Wuchshöhe in mm (NA wenn Pflanze abgestorben) und die
    vierte Spalte enthält meine Matrikelnummer (2139315).
    Wenn gegossen wird, wird dies in "Watering.csv" gespeichert. Die erste Spalte
    erhält den Zeitpunkt des Formats des Messtages in "Wuchshöhen.csv", und die zweite
    Spalte erhält die Menge an Medium, mit der jede Tasse bewässert wurde in Teelöffeln.
    Nach jeder Durchführung der oben genannten vier Schritte (respektive zwei, wenn
    am Tag schon gegossen wurde) werden die Änderungen mittels "git" versioniert.
    In "Materials.csv" werden alle verwendeten Materialien aufgelistet. Die erste
    Spalte enthält den entsprechende Materialnamen, die zweite die Menge des Materials
    und die Dritte den Zweck, die Vierte eine optionale erwähnenswerte Zusatzinfo,
    falls diese für die Reproduktion notwendig ist/sein könnte. In allen ".csv"-Dateien
    wird ein Semikolon als Trennzeichen verwendet.
    Nach der letzten Messung wird jede Tasse einzeln fotografiert. Die Fotos werden
    in Results/ gespeichert, dabei das Bild der Tasse, die mit normalem Wasser gegossen
    wurde als normal_after.png, mit Salzigem als salty_after.png und mit Saurem als
    acidic_after.png


Folgend sind alle Abhängigkeiten aufgelistet, die während der gesamten Arbeit
direkt oder indirekt verwendet wurden:
    Windows:
        direkt:
            Windows 10.0.22621.2134
            wsl 1.2.5.0
            Sublime Text 4.1.5.2
            Excel 16.0.16626.20170
            Terminal 1.17.11461.0
            OneDrive 23.153.724.3

        indirekt:
            iCloud 14.2.108.0
            Windscribe 2.6.14.0
            CareUEyes 2.1.12.0
            "Control Center 3.0" 6.33.3.0 (Herausgeber CLEVO)

    Linux (wsl):
        direkt:
            sudo 1.8.31
            apt 2.0.9
            rm 8.30
            mv 8.30
            mkdir 8.30
            git 2.25.1
            zip 3.0
            unzip 6.00
            texlive-full 2019.20200218-1 (via apt)
                pdflatex 3.14159265-2.6-1.40.20
                biber 2.14
            python3 3.8.10 (via apt)
            pip 20.0.2 (via apt)
            matplotlib 3.5.2 (via pip)
            r-base 3.6.3-2 (via apt)
                Rscript 3.6.3
            Ubuntu 20.04.6 LTS
            Kernel: Linux 5.15.90.1-microsoft-standard-WSL2
            zsh 5.8
            sha256sum 8.30
            cargo 1.69.0
            lsd 0.23.1 (via cargo)
            autojump 22.5.1 (via apt)

        indirekt:
            starship 1.14.2 (via cargo)
            oh-my-zsh (via git) (GitHub repo ohmyzsh/ohmyzsh at commit 03a0d5b)
                aktive plugins:
                    alias-finder
                    autojump
                    colored-man-pages
                    colorize
                    command-not-found
                    docker
                    extract
                    git
                    gitfast
                    nvm
                    npm
                    tmux
                    git-auto-fetch
                    history
                    ubuntu
                    zsh-syntax-highlighting (via git) (GitHub repo zsh-users/zsh-syntax-highlighting at commit 1386f12)
            dockerd 20.10.25

    Prozessor: i5-10500H
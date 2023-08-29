. ~/.bash_aliases
filename="WIAS_WS22_23_Sill"
if [ -f $filename.zip ]; then rm $filename.zip; fi
md tmp
cp Hausarbeit.pdf tmp/$filename.pdf
md tmp/Supplement
cp Readme.txt tmp/Supplement
cp -r */ tmp/Supplement
cp -r Analyse.py tmp/Supplement
cp -r my_analysis.R tmp/Supplement
cp -r *.csv tmp/Supplement
cd tmp
rm -r Supplement/tmp
rm Supplement/Analyse/*.*
zip -r -m -q ../$filename.zip *
cd ..
rm -r tmp
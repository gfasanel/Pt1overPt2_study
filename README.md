# Pt1overPt2_study

#Usage:
********************************************************************
./miniAOD_Z_pt1_pt2_plotter.py -n <file_number> -c <configuration>

./miniAOD_Z_pt1_pt2_plotter.py -n 12 -c leading/random

This will produce root histograms

If you want to loop over all the root files, just type:

makerHistos_pt1_pt2_all.sh

Then, you can make the plots

./Plot

Plot is a bash script which calls plotter.py and organizer.sh

(./plotter.py and organize them in directories on your web space:./organizer.sh)

****************************************************8
#Good practice

#! /usr/bin/python
chmod +x plotter.py

#! /bin/bash
chmod +x organizer.sh

At this point you specified which intepreter must be used, then, type just:

./plotter.py

./organizer.sh

no need to type "python script.py or source script.sh"





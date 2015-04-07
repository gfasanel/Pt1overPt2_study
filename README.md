# Pt1overPt2_study

#Usage:

./miniAOD_Z_pt1_pt2_plotter.py -n <file_number> -c <configuration>

./miniAOD_Z_pt1_pt2_plotter.py -n 1 -c leading/random

This will produce root histograms

If you want to loop over all the root files, just type:

makerHistos_pt1_pt2_all.sh

Then, you can make the plots

./plotter.py

and organize them in directories on your web space:

./organizer.sh


# Good Practice

#! /usr/bin/python
chmod +x script.py

#! /bin/bash
chmod +x script.sh

At this point you specified which intepreter must be used, then, type just:

./script.py

./script.sh

no need to type "python script.py or source script.sh"





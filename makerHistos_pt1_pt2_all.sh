#Working on AOD
#python Z_pt1_pt2_plotter.py -n 0
#python Z_pt1_pt2_plotter.py -n 1
#python Z_pt1_pt2_plotter.py -n 2
#python Z_pt1_pt2_plotter.py -n 3
#python Z_pt1_pt2_plotter.py -n 4
#python Z_pt1_pt2_plotter.py -n 5
#python Z_pt1_pt2_plotter.py -n 6
#python Z_pt1_pt2_plotter.py -n 7
#python Z_pt1_pt2_plotter.py -n 8
#python Z_pt1_pt2_plotter.py -n 9

#working on miniAOD
#python miniAOD_Z_pt1_pt2_plotter.py -n 0  -c leading
#python miniAOD_Z_pt1_pt2_plotter.py -n 1  -c leading
#python miniAOD_Z_pt1_pt2_plotter.py -n 2  -c leading
#python miniAOD_Z_pt1_pt2_plotter.py -n 3  -c leading
#python miniAOD_Z_pt1_pt2_plotter.py -n 4  -c leading
#python miniAOD_Z_pt1_pt2_plotter.py -n 5  -c leading
#python miniAOD_Z_pt1_pt2_plotter.py -n 6  -c leading
#python miniAOD_Z_pt1_pt2_plotter.py -n 7  -c leading
#python miniAOD_Z_pt1_pt2_plotter.py -n 8  -c leading
#python miniAOD_Z_pt1_pt2_plotter.py -n 9  -c leading
#python miniAOD_Z_pt1_pt2_plotter.py -n 10 -c leading
#python miniAOD_Z_pt1_pt2_plotter.py -n 11 -c leading
python miniAOD_Z_pt1_pt2_plotter.py -n 12 -c leading #200-400

python miniAOD_Z_pt1_pt2_plotter.py -n 12 -c random #200-400

#hadd -f histograms.root histograms_*.root 
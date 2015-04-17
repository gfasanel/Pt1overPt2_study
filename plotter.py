#! /usr/bin/python
import math, os
import ROOT

ROOT.gROOT.SetBatch()        # don't pop up canvases
ROOT.gROOT.SetStyle('Plain') # white background
ROOT.gStyle.SetOptStat(0)

ROOT.gStyle.SetFrameBorderMode(ROOT.kWhite)
ROOT.gStyle.SetFrameFillColor(ROOT.kWhite)
ROOT.gStyle.SetCanvasBorderMode(ROOT.kWhite)
ROOT.gStyle.SetCanvasColor(ROOT.kWhite)
ROOT.gStyle.SetPadBorderMode(ROOT.kWhite)
ROOT.gStyle.SetPadColor(ROOT.kWhite)
ROOT.gStyle.SetStatColor(ROOT.kWhite)

# Per le regioni uso i dizionari
pt_regions=['0_10','10_20','20_30','30_60','60_100','100_200']# just the label of the regions
regions={}
regions['0_10']=dict(name='ptEE0_10',ptmin=0.,ptmax=10.)
regions['10_20']=dict(name='ptEE10_20',ptmin=10.,ptmax=20.)
regions['20_30']=dict(name='ptEE20_30',ptmin=20.,ptmax=30.)
regions['30_60']=dict(name='ptEE30_60',ptmin=30.,ptmax=60.)
regions['60_100']=dict(name='ptEE60_100',ptmin=60.,ptmax=100.)
regions['100_200']=dict(name='ptEE100_200',ptmin=100.,ptmax=200.)

detector_regions=['BB','BE','EE']

from optparse import OptionParser
parser=OptionParser()
parser.add_option("-c","--configuration",dest="_1and2",default="leading",type="str")
parser.add_option("-n","--file_number",dest="_N",default=12,help="number of file")
parser.add_option("-m","--mean",dest="mean",default=0.,type=float,help="mean")
parser.add_option("-s","--sigma",dest="sigma",default=0.,type=float,help="sigma")
parser.add_option("-t","--test",action="store_true",help="test was done with 100 entries")
(options,args)=parser.parse_args()


print "Regions are: "
for region in pt_regions:
    print region, regions[region]['name']

variables=['pt1_reco','pt2_reco','pt1_gen','pt2_gen','pt1_Over_pt2_gen','pt1_Over_pt2_reco','pt1_Over_pt2_diff','ratio_vs_gen']
hist={}
graphs={}

for variable in variables:
    if variable is not 'ratio_vs_gen':
        hist[variable]={}
    if variable is 'ratio_vs_gen':
        graphs[variable]={}
    

for det in detector_regions:
    for variable in variables:
        if variable is not 'ratio_vs_gen':
            hist[variable][det]={}
        if variable is 'ratio_vs_gen':
            graphs[variable][det]={}

##########Opening the destination file##########################
mean=options.mean
sigma=options.sigma
test=''
if(options.test):
    test='_test'

mean_str=""
sigma_str=""
if(mean!=0 or sigma !=0):
    mean_str="_"+str(mean)
    mean_str=mean_str.replace(".","")
    sigma_str="_"+str(sigma)
    sigma_str=sigma_str.replace(".","")

histofile=ROOT.TFile(str('histograms_'+str(options._N)+"_"+str(options._1and2)+test+mean_str+sigma_str+'.root'),'READ')
print 'File is ', histofile.GetName()
###############################################################

for region in pt_regions:
    for det in detector_regions:
        #print regions[region]['name']
        #print str('pt1_reco_'+det+'_'+regions[region]['name'])

        hist['pt1_reco'][det][regions[region]['name']]          =histofile.Get(str('pt1_reco_'+det+'_'+regions[region]['name']))
        hist['pt2_reco'][det][regions[region]['name']]          =histofile.Get(str('pt2_reco_'+det+'_'+regions[region]['name']))
        hist['pt1_Over_pt2_reco'][det][regions[region]['name']] =histofile.Get(str('pt1_Over_pt2_reco_'+det+'_'+regions[region]['name']))
                                                                
        hist['pt1_gen'][det][regions[region]['name']]           =histofile.Get(str('pt1_gen_'+det+'_'+regions[region]['name']))
        hist['pt2_gen'][det][regions[region]['name']]           =histofile.Get(str('pt2_gen_'+det+'_'+regions[region]['name']))
        hist['pt1_Over_pt2_gen'][det][regions[region]['name']]  =histofile.Get(str('pt1_Over_pt2_gen_'+det+'_'+regions[region]['name']))

        hist['pt1_reco'][det][regions[region]['name']]          .GetEntries()
        hist['pt2_reco'][det][regions[region]['name']]          .GetEntries()
        hist['pt1_Over_pt2_reco'][det][regions[region]['name']] .GetEntries()
                                                      
        hist['pt1_gen'][det][regions[region]['name']]           .GetEntries()
        hist['pt2_gen'][det][regions[region]['name']]           .GetEntries()
        hist['pt1_Over_pt2_gen'][det][regions[region]['name']]  .GetEntries()

        hist['pt1_Over_pt2_diff'][det][regions[region]['name']]          =histofile.Get(str('pt1_Over_pt2_diff_'+det+'_'+regions[region]['name']))
        graphs['ratio_vs_gen'][det][regions[region]['name']]          =histofile.Get(str('ratio_vs_gen_'+det+'_'+regions[region]['name']))




canvas={}# a comparison plot for each region
diff_canvas={}
ratio_vs_gen_canvas={}

for det in detector_regions:
    canvas[det]={}
    diff_canvas[det]={}
    ratio_vs_gen_canvas[det]={}

# draw everything and save the histos

#print hist['pt1_Over_pt2_reco'][regions[region]['name']].GetEntries()

if not os.path.exists('~/scratch1/www/Pt1Pt2/pt1_pt2_plots'):
    os.makedirs('~/scratch1/www/Pt1Pt2/pt1_pt2_plots')

#file = ROOT.TFile('histograms.root','RECREATE')

for region in pt_regions:
    for det in detector_regions:
        ratio_vs_gen_canvas[det][str(region)]=ROOT.TCanvas(str('ratio_vs_gen_'+det+'_'+region),str('ratio_vs_gen_'+det+'_'+region))
        diff_canvas[det][str(region)]=ROOT.TCanvas(str('diff_'+det+'_'+region),str('diff_'+det+'_'+region))
        canvas[det][str(region)]=ROOT.TCanvas(str(det+'_'+region),str(det+'_'+region))
        canvas[det][str(region)].cd()
        canvas[det][str(region)].SetLeftMargin(0.1)
        print "plotting"
    #print regions[region]['name']
        hist['pt1_Over_pt2_gen'][det][regions[region]['name']].SetLineColor(ROOT.kRed)

        if(hist['pt1_Over_pt2_gen'][det][regions[region]['name']].Integral()!=0):
            hist['pt1_Over_pt2_gen'][det][regions[region]['name']].Scale(1./hist['pt1_Over_pt2_gen'][det][regions[region]['name']].Integral())
        if(hist['pt1_Over_pt2_reco'][det][regions[region]['name']].Integral()!=0):
            hist['pt1_Over_pt2_reco'][det][regions[region]['name']].Scale(1./hist['pt1_Over_pt2_reco'][det][regions[region]['name']].Integral())

        hist['pt1_Over_pt2_gen'][det][regions[region]['name']].SetMaximum(max([hist['pt1_Over_pt2_gen'][det][regions[region]['name']].GetMaximum(),hist['pt1_Over_pt2_reco'][det][regions[region]['name']].GetMaximum()]))

        hist['pt1_Over_pt2_gen'][det][regions[region]['name']].GetXaxis().SetTitle("pt_{1}/pt_{2}")
        hist['pt1_Over_pt2_gen'][det][regions[region]['name']].GetYaxis().SetTitleOffset(1.2)
        hist['pt1_Over_pt2_gen'][det][regions[region]['name']].GetYaxis().SetTitle("Normalized events")
        hist['pt1_Over_pt2_gen'][det][regions[region]['name']].Draw()
        hist['pt1_Over_pt2_reco'][det][regions[region]['name']].Draw("same")

        label=ROOT.TLatex(0.3,0.85,'Gen entries = %i'%hist['pt1_Over_pt2_gen'][det][regions[region]['name']].GetEntries())
        label_RMS=ROOT.TLatex(0.6,0.85,', RMS = %f'%hist['pt1_Over_pt2_gen'][det][regions[region]['name']].GetRMS())
        label.SetNDC() #This is telling root "Use normalized coordinates"
        label_RMS.SetNDC()

        label2=ROOT.TLatex(0.3,0.75,'Reco entries = %i'%hist['pt1_Over_pt2_reco'][det][regions[region]['name']].GetEntries())
        label2_RMS=ROOT.TLatex(0.6,0.75,', RMS = %f'%hist['pt1_Over_pt2_reco'][det][regions[region]['name']].GetRMS())
        label2.SetNDC()
        label2_RMS.SetNDC()

        label.Draw()
        label_RMS.Draw()
        label2.Draw()
        label2_RMS.Draw()

        leg=ROOT.TLegend(0.6,0.6,0.9,0.7)
        leg.SetBorderSize(0)
        leg.SetFillColor(ROOT.kWhite)
        leg.AddEntry(hist['pt1_Over_pt2_gen'][det][regions[region]['name']],"Generated","l")
        leg.AddEntry(hist['pt1_Over_pt2_reco'][det][regions[region]['name']],"Reconstruced","l")

        leg.Draw('same')
        canvas[det][str(region)].SaveAs(str('~/scratch1/www/Pt1Pt2/pt1_pt2_plots/'+det+'_'+region+'_'+options._1and2+test+mean_str+sigma_str+'.png'))

##************Diff canvas
        diff_canvas[det][str(region)].cd()
        diff_canvas[det][str(region)].SetBottomMargin(0.2)
        hist['pt1_Over_pt2_diff'][det][regions[region]['name']].GetXaxis().SetTitleOffset(1.8)
        hist['pt1_Over_pt2_diff'][det][regions[region]['name']].GetXaxis().SetTitle("#frac{pt1}{pt2}(reco - gen) ")        
        hist['pt1_Over_pt2_diff'][det][regions[region]['name']].GetYaxis().SetTitle("Events")
        hist['pt1_Over_pt2_diff'][det][regions[region]['name']].Draw()        
        label_diff=ROOT.TLatex(0.6,0.85,"RMS = %f"%hist['pt1_Over_pt2_diff'][det][regions[region]['name']].GetRMS())        
        label_diff.SetNDC()
        label_diff.Draw("same")
        diff_canvas[det][str(region)].SaveAs(str('~/scratch1/www/Pt1Pt2/pt1_pt2_plots/'+"diff"+"_"+det+'_'+region+'_'+options._1and2+test+mean_str+sigma_str+'.png'))

##************
        ratio_vs_gen_canvas[det][str(region)].cd()
        graphs['ratio_vs_gen'][det][regions[region]['name']].GetXaxis().SetTitle("pt1_{gen}/pt2_{gen}")
        graphs['ratio_vs_gen'][det][regions[region]['name']].GetYaxis().SetTitle("#frac{pt1}{pt2}(gen/reco)")
        graphs['ratio_vs_gen'][det][regions[region]['name']].Draw("AP*")        
        ratio_vs_gen_canvas[det][str(region)].SaveAs(str('~/scratch1/www/Pt1Pt2/pt1_pt2_plots/'+"ratio_vs_gen"+"_"+det+'_'+region+'_'+options._1and2+test+mean_str+sigma_str+'.png'))


canvas_ptZ=ROOT.TCanvas("ptZ","ptZ")
ptZ_gen=histofile.Get("ptZ_gen")
ptZ_gen.Draw()
canvas_ptZ.SaveAs('~/scratch1/www/Pt1Pt2/pt1_pt2_plots/ptZ_gen'+'_'+options._1and2+test+mean_str+sigma_str+'.png')

canvas_massZ=ROOT.TCanvas("massZ","massZ")
massZ_gen=histofile.Get("massZ_gen")
massZ_gen.Draw()
canvas_massZ.SaveAs('~/scratch1/www/Pt1Pt2/pt1_pt2_plots/massZ_gen'+'_'+options._1and2+test+mean_str+sigma_str+'.png')




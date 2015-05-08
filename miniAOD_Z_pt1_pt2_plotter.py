#!/usr/bin/python

#more info at https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookFWLitePython
#more info at https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD#MC_Truth
# http://cmslxr.fnal.gov/source/DataFormats/FWLite/interface/Event.h
# http://cmslxr.fnal.gov/lxr/
# dataset=/*DYToEE*/Phys14DR*/*AODSIM
# https://cmsweb.cern.ch/das/request?input=dataset%3D%2FDYToEE_Tune4C_13TeV-pythia8%2FPhys14DR-AVE20BX25_tsg_PHYS14_25_V3-v1%2FAODSIM&instance=prod%2Fglobal

import math, os
import ROOT
from Module_electron import *
from DataFormats.FWLite import Events, Handle
ROOT.gROOT.SetBatch()        # don't pop up canvases

######################Parsing arguments in python#####################
from optparse import OptionParser
parser=OptionParser()
parser.add_option("-n","--file_number",dest="_N",default=12,help="number of file")
parser.add_option("-c","--configuration",dest="_1and2",type="str",default="leading",help="configuration")
parser.add_option("-m","--mean",dest="mean",default=0.,type=float,help="mean")
parser.add_option("-s","--sigma",dest="sigma",default=0.,type=float,help="sigma")
parser.add_option("-t","--test",action="store_true",help="make a quick test with 100 entries")

(options,args)=parser.parse_args()

print "You are running on file ",options._N
print "and with",options._1and2," configuration"

events = Events("DY_200_400_miniAOD/6C63A3C9-2972-E411-9997-00266CFFBCD0.root") #I downloaded the miniAOD

# create handle outside of loop
ele_handle  = Handle ('std::vector<pat::Electron>')
ele_label = ("slimmedElectrons")

gen_handle  = Handle ('std::vector<reco::GenParticle>')
gen_label = ("prunedGenParticles") # pruned particles point to high level objectes, even the not stable ones

# loop over events

pt_regions=['0_10','10_20','20_30','30_60','60_100','100_200']# just the label of the regions

regions={}
regions['0_10']=dict(name='ptEE0_10',ptmin=0.,ptmax=10.)
regions['10_20']=dict(name='ptEE10_20',ptmin=10.,ptmax=20.)
regions['20_30']=dict(name='ptEE20_30',ptmin=20.,ptmax=30.)
regions['30_60']=dict(name='ptEE30_60',ptmin=30.,ptmax=60.)
regions['60_100']=dict(name='ptEE60_100',ptmin=60.,ptmax=100.)
regions['100_200']=dict(name='ptEE100_200',ptmin=100.,ptmax=200.)

detector_regions=['BB','BE','EE']
variables=['pt1_reco','pt2_reco','pt1_Over_pt2_reco','pt1_gen','pt2_gen','pt1_Over_pt2_gen','pt1_Over_pt2_diff','ratio_vs_gen']

hist={} #At this point, hist depends on 1 variable
graphs={}
for variable in variables:
    hist[variable]={} #At this point, hist depends on 2 variables
    graphs[variable]={}
for det in detector_regions:
    for variable in variables:
        hist[variable][det]={} #At this point, hist depends on 3 variables (and so on)
        graphs[variable][det]={}

####Histo depending only on the region###########
histo_ptZ_gen={}
histo_ptZ_reco={}
histo_ptsum_gen={}
histo_ptsum_reco={}

for det in detector_regions:
    histo_ptZ_gen[det]=ROOT.TH1F(str("ptZ_gen_"+det),str("ptZ_gen_"+det),300,0,300)
    histo_ptZ_reco[det]=ROOT.TH1F(str("ptZ_reco_"+det),str("ptZ_reco_"+det),300,0,300)
    histo_ptsum_gen[det]=ROOT.TH1F(str("ptsum_gen_"+det),str("ptsum_gen_"+det),300,100,400)
    histo_ptsum_reco[det]=ROOT.TH1F(str("ptsum_reco_"+det),str("ptsum_reco_"+det),300,100,400)

##Global histos #################################
histo_massZ=ROOT.TH1F("massZ","massZ",500,0,500)
histo_ptZ=ROOT.TH1F("ptZ","ptZ",300,0,300)

for region in pt_regions:
   for det in detector_regions:
       for variable in variables:
           if variable in ['pt1_reco','pt2_reco','pt1_gen','pt2_gen']:
               hist[variable][det][regions[region]['name']]=ROOT.TH1F(str(variable+'_'+det+'_'+regions[region]['name']),str(variable+'_'+det+'_'+regions[region]['name']),300,0,300)
           if variable in ['pt1_Over_pt2_reco','pt1_Over_pt2_gen']:
               hist[variable][det][regions[region]['name']]=ROOT.TH1F(str(variable+'_'+det+'_'+regions[region]['name']),str(variable+'_'+det+'_'+regions[region]['name']),200,0,5)
           if variable in ['pt1_Over_pt2_diff']:
               hist[variable][det][regions[region]['name']]=ROOT.TH1F(str(variable+'_'+det+'_'+regions[region]['name']),str(variable+'_'+det+'_'+regions[region]['name']),200,-1,1)               
           if variable in ['ratio_vs_gen']:
               graphs[variable][det][regions[region]['name']]=ROOT.TGraph()
               graphs[variable][det][regions[region]['name']].SetName(str(variable+'_'+det+'_'+regions[region]['name']))

uniform_test=ROOT.TH1F("uniform_test","uniform_test",100,0,1)
gauss_test=ROOT.TH1F("gauss_test","gauss_test",100,options.mean - 2,options.mean + 2)
rand=ROOT.TRandom3()
rand_gauss=ROOT.TRandom3()

counter =ROOT.TH1F("counter","counter",1,0,1)
counter_eles=ROOT.TH1F("counter_eles","counter_eles",1,0,1)
counter_none=ROOT.TH1F("counter_none","counter_none",1,0,1)
counter_eles_acceptance=ROOT.TH1F("counter_eles_acceptance","counter_eles_acceptance",1,0,1)
counter_reco=ROOT.TH1F("counter_reco","counter_reco",1,0,1)

####Dealing with counters for graphs#######
i={} #i is a counter, it depends on 1 variable
for det in detector_regions:
    i[det]={} #now i depends on 2 variables
#Initializing
for det in detector_regions:
    for region in pt_regions:
        i[det][regions[region]['name']]=0
##########################################

if (options.test): #Message
    print "This is a quick test with 500 entries"

mean=options.mean
sigma=options.sigma

# LOOP
for iev,event in enumerate(events):
    uniform_test.Fill(rand.Uniform(0,1)) #x_min,x_max
    gauss_test.Fill(rand_gauss.Gaus(mean,sigma)) #mean,sigma
    if(options.test):
        if iev > 500: break #For quick tests
    counter.Fill(0.5)

    # use getByLabel, just like in cmsRun
    event.getByLabel (ele_label,ele_handle)
    event.getByLabel (gen_label,gen_handle)
    #event.getByLabel (gen_packed_label,gen_packed_handle)
    # get the product
    electrons = ele_handle.product()
    gen_particles = gen_handle.product() # These are the pruned ==> use these ones

    gen1=0
    gen2=0
    ismatched1=0
    ismatched2=0

    #Dummy initialization of the objects
    gen_electron1=electron_object(999,0,0,0)
    gen_electron2=electron_object(999,0,0,0)
    reco_electron1=electron_object(999,0,0,0)
    reco_electron2=electron_object(999,0,0,0)

    vector_Z_gen=ROOT.TLorentzVector() # This is the mc Z, not the one built from the 2 eles (it's different because of FSR)

    for igen, genParticle in enumerate(gen_particles): #loop over generated particles
        if (abs(genParticle.pdgId())==11 and genParticle.mother(0).pdgId()==23 ):# it must be an electron, daughter of a Z boson
            if(gen1==0):
                gen_electron1.set_p4(genParticle.px(),genParticle.py(),genParticle.pz(),genParticle.energy())
                gen1=1

                for iele, electron in enumerate(electrons): #loop over reconstructed
                    factor1=1+rand_gauss.Gaus(mean,sigma)
                    reco_electron1.set_p4(electron.px(),electron.py(),electron.pz(),electron.energy())
                    dr=999
                    dr=reco_electron1.p4.DeltaR(gen_electron1.p4)
                    if dr<0.15:
                        ismatched1=1 #This tells if the gen1 is reconstructed
                        reco_electron1.set_p4(electron.px()*factor1,electron.py()*factor1,electron.pz()*factor1,electron.energy()*factor1)
                    if(ismatched1): 
                       break # This breaks the reconstuction loop for the first ele
                    
            elif (gen1==1 and gen2==0):
                counter_eles.Fill(0.5)
                gen_electron2.set_p4(genParticle.px(),genParticle.py(),genParticle.pz(),genParticle.energy())
                gen2=1

                vector_Z_gen.SetPxPyPzE(genParticle.mother(0).px(),genParticle.mother(0).py(),genParticle.mother(0).pz(),genParticle.mother(0).energy())
    

                for iele, electron in enumerate(electrons): #loop over reconstructed
                    factor2=1+rand_gauss.Gaus(mean,sigma)
                    reco_electron2.set_p4(electron.px(),electron.py(),electron.pz(),electron.energy())
                    dr=999
                    dr=reco_electron2.p4.DeltaR(gen_electron2.p4)
                    if dr<0.15:
                        ismatched2=1 #This tells if the gen2 is reconstructed
                        reco_electron2.set_p4(electron.px()*factor2,electron.py()*factor2,electron.pz()*factor2,electron.energy()*factor2)
                    if(ismatched2):
                       break #this breaks the reconstruction loop
                if(ismatched1 and ismatched2):
                    counter_reco.Fill(0.5)
                    break # This breaks the loop over the generated: 


    #Decide which one is "1"
    if(options._1and2=="leading"):
        if(gen_electron1.p4.Pt() < gen_electron2.p4.Pt()): #swap if 2 is the leading
            gen_electron1.swap(gen_electron2)
            reco_electron1.swap(reco_electron2)

    elif(options._1and2=="random"):
        if(rand.Uniform(0,1)>0.5): #If rand number  > 0.5 :swap
            gen_electron1.swap(gen_electron2)
            reco_electron1.swap(reco_electron2)

    #Now, you build your Z from your generated eles (for categorization BB, BE, EE)
    Z_gen=Zboson_object(gen_electron1,gen_electron2)
    Z_reco=Zboson_object(reco_electron1,reco_electron2)

    if (gen1 and gen2):
        detector_descriptor=Z_gen.regions
        if(detector_descriptor=='none'):
            counter_none.Fill(0.5)
        if(detector_descriptor!='none'):
            counter_eles_acceptance.Fill(0.5)

        if(detector_descriptor!="none"):
            histo_ptZ_gen[detector_descriptor].Fill(Z_gen.p4.Pt())
            histo_ptsum_gen[detector_descriptor].Fill(Z_gen.e1.p4.Pt() + Z_gen.e2.p4.Pt())

        for region in pt_regions: 
            if ( vector_Z_gen.Pt() >= regions[region]['ptmin'] and vector_Z_gen.Pt() < regions[region]['ptmax'] and detector_descriptor!='none'):
                hist['pt1_gen'][detector_descriptor][regions[region]['name']].Fill(gen_electron1.p4.Pt())
                hist['pt2_gen'][detector_descriptor][regions[region]['name']].Fill(gen_electron2.p4.Pt())
                hist['pt1_Over_pt2_gen'][detector_descriptor][regions[region]['name']].Fill(gen_electron1.p4.Pt()/gen_electron2.p4.Pt())
                histo_massZ.Fill(vector_Z_gen.M())
                histo_ptZ.Fill(vector_Z_gen.Pt())

    if (ismatched1 and ismatched2):
        if(detector_descriptor!="none"):
            histo_ptZ_reco[detector_descriptor].Fill(Z_reco.p4.Pt())
            histo_ptsum_reco[detector_descriptor].Fill(Z_reco.e1.p4.Pt() + Z_reco.e2.p4.Pt())

        for region in pt_regions: 
            if (vector_Z_gen.Pt() >= regions[region]['ptmin'] and vector_Z_gen.Pt() < regions[region]['ptmax'] and detector_descriptor!='none'):
                hist['pt1_reco'][detector_descriptor][regions[region]['name']]         .Fill(reco_electron1.p4.Pt())
                hist['pt2_reco'][detector_descriptor][regions[region]['name']]         .Fill(reco_electron2.p4.Pt())
                hist['pt1_Over_pt2_reco'][detector_descriptor][regions[region]['name']].Fill(reco_electron1.p4.Pt()/reco_electron2.p4.Pt())
                hist['pt1_Over_pt2_diff'][detector_descriptor][regions[region]['name']].Fill( (gen_electron1.p4.Pt()/gen_electron2.p4.Pt()) - (reco_electron1.p4.Pt()/reco_electron2.p4.Pt()) )

                i[detector_descriptor][regions[region]['name']]+=1
                graphs['ratio_vs_gen'][detector_descriptor][regions[region]['name']]   .SetPoint(i[detector_descriptor][regions[region]['name']],(gen_electron1.p4.Pt()/gen_electron2.p4.Pt()), (gen_electron1.p4.Pt()*reco_electron2.p4.Pt())/(gen_electron2.p4.Pt()*reco_electron1.p4.Pt()))

# Save the histos
print "Total number of events",counter.GetEntries()
print "Total number of events with 2 generated eles",counter_eles.GetEntries()
print "Total number of events with 2 generated eles inside the acceptance",counter_eles_acceptance.GetEntries()
print "Total number of events with 2 generated eles, but outside the acceptance",counter_none.GetEntries()
print "Total number of events with 2 reco eles (matched with gen)",counter_reco.GetEntries()

   
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

file = ROOT.TFile(str('histograms_'+str(options._N)+'_'+str(options._1and2)+test+mean_str+sigma_str+'.root'),'RECREATE')

for region in pt_regions:
    for det in detector_regions:
        for variable in variables:
            if variable != 'ratio_vs_gen':
                hist[variable][det][regions[region]['name']].Write()
            if variable in ['ratio_vs_gen']:
                graphs[variable][det][regions[region]['name']].Write()

for det in detector_regions:
    histo_ptZ_gen[det].Write()
    histo_ptZ_reco[det].Write()
    histo_ptsum_gen[det].Write()
    histo_ptsum_reco[det].Write()

#Additional histos
histo_ptZ.Write()
histo_massZ.Write()
uniform_test.Write()
gauss_test.Write()

counter.Write()
counter_eles.Write()
counter_none.Write()
counter_eles_acceptance.Write()
counter_reco.Write()

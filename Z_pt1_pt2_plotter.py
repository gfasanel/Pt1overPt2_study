#!/usr/bin/python
import math, os
import ROOT
from DataFormats.FWLite import Events, Handle

#more info at https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookFWLitePython
#more info at https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD#MC_Truth
# http://cmslxr.fnal.gov/source/DataFormats/FWLite/interface/Event.h
# http://cmslxr.fnal.gov/lxr/
# dataset=/*DYToEE*/Phys14DR*/*AODSIM
# https://cmsweb.cern.ch/das/request?input=dataset%3D%2FDYToEE_Tune4C_13TeV-pythia8%2FPhys14DR-AVE20BX25_tsg_PHYS14_25_V3-v1%2FAODSIM&instance=prod%2Fglobal

##########################STARTING TO DO SOMETHING#####################

######################Parsing arguments in python#####################
import sys,getopt #to handle arguments in python

def main(argv):# defining the main function, called later
   try:
      opts, args = getopt.getopt(argv,"hn:",["file_number="])#getopt takes three args: a list (argv),short options, long options
#short options that requires an argument are followed by :, long options requiring an argument are followed by =
   except getopt.GetoptError:
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'python Z_pt1_pt2_plotter.py -n #'
         print 'or'
         print 'python Z_pt1_pt2_plotter.py --file_number=#'
         sys.exit()
      elif opt in ("-n","--file_number"):
         global _N #defining a global variable _N
         _N=arg

if __name__ == "__main__":
   main(sys.argv[1:]) #argomento 0 e' il plotter.py, percio' lo scarti e ti prendi gli altri che seguono

########################################################################
###Defining classes#############
class gen_electron:
    def __init__(self, px,py,pz,E):#This is the constructor
        self.p4 = ROOT.TLorentzVector(px,py,pz,E)
        self.region = 'none'
        if abs(self.p4.Eta()) < 1.4442:
            self.region =  'barrel'
        elif abs(self.p4.Eta())>1.566  and abs(self.p4.Eta())<2.5:
            self.region = 'endcap'

class Zboson_object:
    def __init__(self, e1, e2):#This is the constructor
        self.e1 = e1
        self.e2 = e2
        self.p4 = e1.p4 + e2.p4
        self.regions = 'none'
        if self.e1.region=='barrel' and self.e2.region=='barrel':
            self.regions = 'BB'
        elif self.e1.region=='barrel' and self.e2.region=='endcap':
            self.regions = 'BE'
        elif self.e1.region=='endcap' and self.e2.region=='barrel':
            self.regions = 'BE'
        elif self.e1.region=='endcap' and self.e2.region=='endcap':
            self.regions = 'EE'




#AOD for DY
#sample_location= 'root://xrootd.unl.edu//store/mc/Phys14DR/DYToEE_Tune4C_13TeV-pythia8/AODSIM/AVE20BX25_tsg_PHYS14_25_V3-v1/10000/'
#filename=['0CCBF0FA-2289-E411-A5D4-003048F0E55A.root','34A140BA-1A89-E411-B4CD-003048F0E55A.root','386E81D1-5A89-E411-88B4-003048CF6346.root','4C2A4F24-1589-E411-8778-002590AC505C.root','52841D85-1C89-E411-91A8-0025907FD280.root','52BD2BCB-9D89-E411-89ED-003048D3CD6C.root','5EF5E61F-1889-E411-BA2C-0025907DCA72.root','A2EF7743-1689-E411-8EA2-002590AC4FC8.root','BCDC8148-1989-E411-8B64-002590DB9302.root','DA87A535-1789-E411-8167-002590AC4BF6.root']

#events = Events("root://xrootd.unl.edu//store/mc/Phys14DR/DYToEE_Tune4C_13TeV-pythia8/MINIAODSIM/AVE20BX25_tsg_PHYS14_25_V3-v1/10000/CE81818A-A289-E411-B899-003048D3CD6C.root") #i miniAOD non riesce ad aprirmeli

#M_50
#sample_location= 'root://xrootd.unl.edu//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/AODSIM/PU20bx25_tsg_castor_PHYS14_25_V1-v1/10000/'
#filename=['04ED5B57-5F84-E411-A94E-001E67397BC5.root',
#          '062E2D68-3980-E411-AF46-001E6739722E.root',
#          '0ECE5CCB-9480-E411-8EFD-002590A88812.root',
#          '16DA5962-BF80-E411-9DC6-002481E14E58.root',
#          '16E2793B-5283-E411-8B2D-0025905C38AA.root',
#          '187EFA20-DC81-E411-8866-002590A36FB2.root',
#          '18BD0DAC-AF80-E411-885E-001E67396FA9.root',
#          '1C4691C8-9B80-E411-A923-002481E14E58.root',
#          '1C622AF9-5180-E411-A155-0025B3E06394.root',
#          '206460D5-6F81-E411-9445-002590200B68.root']

#MiniAOD M-50
sample_location= 'root://xrootd.unl.edu//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/MINIAODSIM/PU20bx25_tsg_castor_PHYS14_25_V1-v1/10000/'
filename=['12BA0756-4681-E411-9C3D-002590A88812.root']
#          '062E2D68-3980-E411-AF46-001E6739722E.root',
#          '0ECE5CCB-9480-E411-8EFD-002590A88812.root',
#          '16DA5962-BF80-E411-9DC6-002481E14E58.root',
#          '16E2793B-5283-E411-8B2D-0025905C38AA.root',
#          '187EFA20-DC81-E411-8866-002590A36FB2.root',
#          '18BD0DAC-AF80-E411-885E-001E67396FA9.root',
#          '1C4691C8-9B80-E411-A923-002481E14E58.root',
#          '1C622AF9-5180-E411-A155-0025B3E06394.root',
#          '206460D5-6F81-E411-9445-002590200B68.root']

print str(sample_location+filename[int(_N)])


events = Events(str(sample_location+filename[int(_N)]))

# create handle outside of loop
ele_handle  = Handle ('std::vector<reco::GsfElectron>')
ele_label = ("gedGsfElectrons")

gen_handle  = Handle ('std::vector<reco::GenParticle>')
gen_label = ("genParticles")


ROOT.gROOT.SetBatch()        # don't pop up canvases
ROOT.gROOT.SetStyle('Plain') # white background

# loop over events

#loopo sugli eventi e a evento fissato mi prendo la collezione degli elettroni

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
hist={}# Ho bisogno di tutta una serie di istogrammi che dipendono dalla variabile, dalla regione in pt e dalla regione del detector
hist['pt1_reco']={}
hist['pt2_reco']={}
hist['pt1_Over_pt2_reco']={}
hist['pt1_gen']={}
hist['pt2_gen']={}
hist['pt1_Over_pt2_gen']={}

for det in detector_regions:
   hist['pt1_reco'][det]={}
   hist['pt2_reco'][det]={}
   hist['pt1_Over_pt2_reco'][det]={}
   hist['pt1_gen'][det]={}
   hist['pt2_gen'][det]={}
   hist['pt1_Over_pt2_gen'][det]={}

histo_ptZ_gen=ROOT.TH1F("ptZ_gen","ptZ_gen",100,0,100)
histo_massZ_gen=ROOT.TH1F("massZ_gen","massZ_gen",150,0,150)
#histo_ptZ_reco=ROOT.TH1F("ptZ_reco","ptZ_reco",100,0,100)
for region in pt_regions:
   print regions[region]['name']
   for det in detector_regions:
      hist['pt1_reco'][det][regions[region]['name']]=ROOT.TH1F(str('pt1_reco_'+det+'_'+regions[region]['name']),str('pt1_reco_'+det+'_'+regions[region]['name']),100,0,100)
      print str('pt1_reco_'+det+'_'+regions[region]['name'])
      hist['pt2_reco'][det][regions[region]['name']]=ROOT.TH1F(str('pt2_reco_'+det+'_'+regions[region]['name']),str('pt2_reco_'+det+'_'+regions[region]['name']),100,0,100)
      hist['pt1_Over_pt2_reco'][det][regions[region]['name']]=ROOT.TH1F(str('pt1_Over_pt2_reco_'+det+'_'+regions[region]['name']),str('pt1_Over_pt2_reco_'+det+'_'+regions[region]['name']),100,0,3)

      hist['pt1_gen'][det][regions[region]['name']]=ROOT.TH1F(str('pt1_gen_'+det+'_'+regions[region]['name']),str('pt1_gen_'+det+'_'+regions[region]['name']),100,0,100)
      hist['pt2_gen'][det][regions[region]['name']]=ROOT.TH1F(str('pt2_gen_'+det+'_'+regions[region]['name']),str('pt2_gen_'+det+'_'+regions[region]['name']),100,0,100)
      hist['pt1_Over_pt2_gen'][det][regions[region]['name']]=ROOT.TH1F(str('pt1_Over_pt2_gen_'+det+'_'+regions[region]['name']),str('pt1_Over_pt2_gen_'+det+'_'+regions[region]['name']),100,0,3)

# loop over the events
counter = 0
for iev,event in enumerate(events):

    counter =counter +1
    #if iev > 100: break #For quick tests
    #print iev #Ti stampa il numero dell'evento che stai considerando
    # use getByLabel, just like in cmsRun
    event.getByLabel (ele_label,ele_handle)
    event.getByLabel (gen_label,gen_handle)
    # get the product
    electrons = ele_handle.product()
    gen_particles = gen_handle.product()


    gen0=0
    gen1=0
    ismatched0=0
    ismatched1=0

    pt1=9999
    pt2=-1
    pt1_gen=9999
    pt2_gen=-1
    vector_Z_gen = ROOT.TLorentzVector(0,0,0,0)

    detector_descriptor='none'

    for igen, genParticle in enumerate(gen_particles): #loop over generated particles
        if (abs(genParticle.pdgId())==11 and genParticle.mother().pdgId()==23 ):# it must be an electron, daughter of a Z boson
            if(gen0==0):
                #print "Electron 0: ID, Mother ID", genParticle.pdgId(),genParticle.mother().pdgId()
                gen_electron0= gen_electron(genParticle.px(),genParticle.py(),genParticle.pz(),genParticle.energy())
                #print 'gen px,py,pz,E',gen_electron0.p4.Px(),gen_electron0.p4.Py(),gen_electron0.p4.Pz(),gen_electron0.p4.E()
                gen0=1
                pt1_gen=genParticle.pt()

                for iele, electron in enumerate(electrons): #loop over reconstructed
                    vector_reco = ROOT.TLorentzVector(electron.px(),electron.py(),electron.pz(),electron.energy())
                    dr=999
                    #dr=vector_reco.DeltaR(vector_gen)
                    dr=vector_reco.DeltaR(gen_electron0.p4)
                    if dr<0.15:
                        ismatched0=1 #This tells if the gen0 is reconstructed
                        pt1=vector_reco.Pt()
                break
                    
            elif (gen0==1 and gen1==0):
                #print "Electron 1: ID, Mother ID", genParticle.pdgId(),genParticle.mother().pdgId()
                gen_electron1= gen_electron(genParticle.px(),genParticle.py(),genParticle.pz(),genParticle.energy())
                gen1=1
                pt2_gen=genParticle.pt()

                Z=Zboson_object(gen_electron0,gen_electron1)
                vector_Z_gen.SetPxPyPzE(genParticle.mother().px(),genParticle.mother().py(),genParticle.mother().pz(),genParticle.mother().energy())
                detector_descriptor=Z.regions

                for iele, electron in enumerate(electrons): #loop over reconstructed
                    vector_reco1 = ROOT.TLorentzVector(electron.px(),electron.py(),electron.pz(),electron.energy())
                    dr=999
                    dr=vector_reco1.DeltaR(gen_electron1.p4)
                    if dr<0.15:
                        ismatched1=1 #This tells if the gen1 is reconstructed
                        pt2=vector_reco1.Pt()
                break

    if (gen0 and gen1):
        for region in pt_regions: 
            if ( vector_Z_gen.Pt() >= regions[region]['ptmin'] and vector_Z_gen.Pt() < regions[region]['ptmax'] and detector_descriptor!='none' and vector_Z_gen.M() >= 70 and vector_Z_gen.M() <=110 ):
                if(pt1_gen < pt2_gen): #swap if 2 is the leading
                   temp=pt1_gen
                   pt1_gen=pt2_gen
                   pt2_gen=temp

                hist['pt1_gen'][detector_descriptor][regions[region]['name']].Fill(pt1_gen)
                hist['pt2_gen'][detector_descriptor][regions[region]['name']].Fill(pt2_gen)
                hist['pt1_Over_pt2_gen'][detector_descriptor][regions[region]['name']].Fill(pt1_gen/pt2_gen)
                histo_ptZ_gen.Fill(vector_Z_gen.Pt())
                histo_massZ_gen.Fill(vector_Z_gen.M())

    if (ismatched0 and ismatched1):
        for region in pt_regions: 
            if (vector_Z_gen.Pt() >= regions[region]['ptmin'] and vector_Z_gen.Pt() < regions[region]['ptmax'] and detector_descriptor!='none' and vector_Z_gen.M() >= 70 and vector_Z_gen.M() <=110):
                if(pt1 < pt2): #swap if 2 is the leading
                   temp=pt1
                   pt1=pt2
                   pt2=temp
                hist['pt1_reco'][detector_descriptor][regions[region]['name']].Fill(pt1)
                hist['pt2_reco'][detector_descriptor][regions[region]['name']].Fill(pt2)
                hist['pt1_Over_pt2_reco'][detector_descriptor][regions[region]['name']].Fill(pt1/pt2)

# draw everything and save the histos

print "Total number of events",counter


#If directory doesn't exist, then create it
if not os.path.exists('~/scratch1/www/Pt1Pt2/pt1_pt2_plots'):
   os.makedirs('~/scratch1/www/Pt1Pt2/pt1_pt2_plots')
   
#file = ROOT.TFile('histograms.root','RECREATE')
file = ROOT.TFile(str('histograms_'+_N+'.root'),'RECREATE')

for region in pt_regions:
    for det in detector_regions:
       hist['pt1_gen'][det][regions[region]['name']].Write()
       hist['pt2_gen'][det][regions[region]['name']].Write()
       hist['pt1_Over_pt2_gen'][det][regions[region]['name']].Write()
###RECO
       hist['pt1_reco'][det][regions[region]['name']].Write()
       hist['pt2_reco'][det][regions[region]['name']].Write()
       hist['pt1_Over_pt2_reco'][det][regions[region]['name']].Write()

histo_ptZ_gen.Write()
histo_massZ_gen.Write()

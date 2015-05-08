filenames=[]

#MiniAOD M-50
sample_location= 'root://xrootd.unl.edu//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/MINIAODSIM/PU20bx25_tsg_castor_PHYS14_25_V1-v1/10000/'
filename=['12BA0756-4681-E411-9C3D-002590A88812.root',
          '1CFCCDC3-4381-E411-AC51-001E67396A22.root',
          '20678BB9-6E84-E411-8354-001E67397751.root',
          '3CCA8B48-6A84-E411-857C-001E67397756.root',
          '420FF764-3082-E411-9A15-002590A36FB2.root',
          '4AD60677-4581-E411-8943-0025B3E0654E.root',
          '620EEEAE-4E81-E411-A175-002590A88812.root',
          '6235AC67-2D82-E411-B094-002590200838.root',
          '90FB27D8-2E82-E411-8ECC-002590A36FB2.root',
          '9660E98A-7A84-E411-B008-001E67397B11.root']
for file in filename:
   filenames.append(sample_location+str(file))
#120-200
sample_location_120_200='root://xrootd.unl.edu//store/mc/Phys14DR/DYJetsToEEMuMu_M-120To200_13TeV-madgraph/MINIAODSIM/PU20bx25_PHYS14_25_V1-v2/10000/'
filename_120_200=['0626BCFB-C27C-E411-BFCF-002590747DDC.root',
                  'C645CDFB-C27C-E411-A3B0-002590747DDC.root']
for file in filename_120_200:
   filenames.append(sample_location_120_200+str(file))
#200-400
#only 1 file for this # file # 12
filenames.append("root://xrootd.unl.edu//store/mc/Phys14DR/DYJetsToEEMuMu_M-400To800_13TeV-madgraph/MINIAODSIM/PU20bx25_PHYS14_25_V1-v1/00000/6C63A3C9-2972-E411-9997-00266CFFBCD0.root")


##events = Events(str(filenames[int(options._N)])) ##Sometimes files are not available

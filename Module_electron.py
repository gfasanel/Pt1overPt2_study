import ROOT
###Defining classes#############
class electron_object:
    def __init__(self, px,py,pz,E):#This is the constructor
        self.p4 = ROOT.TLorentzVector(px,py,pz,E)
        self.region=self.compute_region()

    def compute_region(self):
        self.region = 'none'
        if abs(self.p4.Eta()) < 1.4442:
            self.region =  'barrel'
        elif abs(self.p4.Eta())>1.566  and abs(self.p4.Eta())<2.5:
            self.region = 'endcap'

    def set_p4(self, px,py,pz,E):#assign p4 and compute the region
        self.p4.SetPxPyPzE(px,py,pz,E)
        self.compute_region()

    def swap(self,electron2):#swap p4 and region
        px_temp=self.p4.Px()
        py_temp=self.p4.Py()
        pz_temp=self.p4.Pz()
        E_temp=self.p4.E()
        region_temp=self.region
        self.p4.SetPxPyPzE(electron2.p4.Px(),electron2.p4.Py(),electron2.p4.Pz(),electron2.p4.E())
        electron2.p4.SetPxPyPzE(px_temp,py_temp,pz_temp,E_temp)
        self.region=electron2.region
        electron2.region=region_temp

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

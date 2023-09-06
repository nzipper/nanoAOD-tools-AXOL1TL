from itertools import repeat, chain, islice
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
import numpy as np
import ugt_hls_emulator as ugt
ROOT.PyConfig.IgnoreCommandLineOptions = True

def l1iter(col, n=0, cut=None, pad=None):
    filtered = col if cut is None else filter(cut, col)
    padded = filtered if n<=0 else islice(chain(filtered, repeat(pad)), n)
    return padded

class axol1tlProducer(Module):
    def __init__(self, branch_name='axol1tl_score'):
        self.branch_name = branch_name
        self.nelectrons = 4
        self.nmuons = 4
        self.njets = 10

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch(self.branch_name, 'F')

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """Calculate AXOL1TL anomaly score from L1 objects and write branch"""
        axo_input = np.array([],dtype=int)

        sums = Collection(event, 'L1EtSum')
        for met in l1iter(sums,cut=lambda obj: obj.bx==0 and obj.etSumType==2):
            axo_input = np.append(axo_input, [met.hwPt,0,met.hwPhi])

        electrons = Collection(event, 'L1EG')
        for lep in l1iter(electrons,self.nelectrons,cut=lambda obj: obj.bx==0):
            vec = [lep.hwPt,lep.hwEta,lep.hwPhi] if lep else [0,0,0]
            axo_input = np.append(axo_input, vec)

        muons = Collection(event, 'L1Mu')
        for lep in l1iter(muons,self.nmuons,cut=lambda obj: obj.bx==0):
            vec = [lep.hwPt,lep.hwEta,lep.hwPhi] if lep else [0,0,0]
            axo_input = np.append(axo_input, vec)

        jets = Collection(event, 'L1Jet')
        for lep in l1iter(jets,self.njets,cut=lambda obj: obj.bx==0):
            vec = [lep.hwPt,lep.hwEta,lep.hwPhi] if lep else [0,0,0]
            axo_input = np.append(axo_input, vec)

        axo_score = ugt.anomaly_detection.hwint_to_anomaly_score(axo_input)
        self.out.fillBranch(self.branch_name, axo_score)

        return True


axol1tlModuleConstr = lambda: axol1tlProducer()

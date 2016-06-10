import ROOT
import math
ROOT.gROOT.SetBatch(True)

    
def calcDR(eta1, eta2, phi1, phi2) :
    # Make sure we don't end up with dR>6.2 at Phi wrap around
    if phi1 > 2. and phi2 < -2. : phi2 += 2*math.pi
    if phi1 < -2. and phi2 > 2. : phi1 += 2*math.pi
    dr_ = math.sqrt( (eta1 - eta2)**2 + (phi1 - phi2)**2 )
    if dr_ > 6.0 : print " dR: ",dr_
    return dr_

def calcDPhi(phi1, phi2) :
    # Make sure we don't end up with dPhi>6.2 at Phi wrap around
    if phi1 > 2. and phi2 < -2. : phi2 += 2*math.pi
    if phi1 < -2. and phi2 > 2. : phi1 += 2*math.pi
    dPhi = phi1 - phi2
    if dPhi > 6.0 : print " dPhi: ",dPhi
    return dPhi



rateFile = ROOT.TFile('L1Rates.root','r')
rateTree = rateFile.Get('l1UpgradeEmuTree/L1UpgradeTree')


rateLimit = 90
c = ROOT.TCanvas('c','c',600,600)

h1 = ROOT.TH1F('h1', 'Stage 2 Rate',rateLimit,0,rateLimit)
rateTree.Draw('L1UpgradeTree.egEt >> h1', 'L1UpgradeTree.egIso > 0')
h2 = ROOT.TH1F('h2', 'Stage 2 Rate',rateLimit,0,rateLimit)
h2.Sumw2()

for i in range(1, h1.GetNbinsX()+1) :
    print h1.Integral( i, rateLimit )
    h2.SetBinContent( i, h1.Integral( i, rateLimit ) )

# Normalize to 30 MHz
factor = 30000 / h1.Integral()
h2.Scale( factor )

h2.Draw()
h2.GetYaxis().SetTitle('Rate (kHz)')
h2.GetXaxis().SetTitle('L1 EG E_{T}')
c.SetLogy()
c.Print('/afs/cern.ch/user/t/truggles/www/TrkTrig/Stage2Rate.png')



effFile = ROOT.TFile('L1Eff.root','r')
effL1Tree = effFile.Get('l1UpgradeEmuTree/L1UpgradeTree')
effEMTree = effFile.Get('l1ElectronRecoTree/ElectronRecoTree')


etAll = ROOT.TH1F('etAll', 'Stage 2: L1 EG Obj E_{T}',100,0,200)
etMatch = ROOT.TH1F('etMatch', 'Stage 2: L1 EG Matching Offline',100,0,200)
dEta = ROOT.TH1F('dEta', 'Stage 2: L1 EG Matching Offline',80,-0.1,0.1)
dPhi = ROOT.TH1F('dPhi', 'Stage 2: L1 EG Matching Offline',80,-0.2,0.2)


cnt = 0
for i in range( 0, effL1Tree.GetEntries() ) :


    # Get the leading L1 EG object and Elec for each event
    effL1Tree.GetEntry(i)
    cnt += 1
    l1Objs = []
    if len(effL1Tree.egEt) == 0 : continue
    for j in range( 0, len(effL1Tree.egEt) ) :
        if effL1Tree.egIso[j] == 0 : l1Objs.append( (0., 0., 0.) )
        else : l1Objs.append( (effL1Tree.egEt[j], effL1Tree.egEta[j], effL1Tree.egPhi[j]) )
        #l1Objs.append( (effL1Tree.egEt[j], effL1Tree.egEta[j], effL1Tree.egPhi[j]) )
    l1Objs.sort(reverse=True)
    #print cnt, effL1Tree.egEt
    effEMTree.GetEntry(i)
    elecs = []
    for j in range( 0, len(effEMTree.et) ) :
        elecs.append( (effEMTree.et[j], effEMTree.eta[j], effEMTree.phi[j]) )
    elecs.sort(reverse=True)
    L1Obj = l1Objs[0]
    elec = elecs[0]
    
    etAll.Fill( L1Obj[0] )
    # check for match in DR
    #dr = math.sqrt( (L1Obj[1] - elec[1])**2 + (L1Obj[2] - elec[2])**2 )
    dr = calcDR( L1Obj[1], elec[1], L1Obj[2], elec[2] )
    #if (L1Obj[2] > 3.1 or L1Obj[2] < -3.1) and (elec[2] > 3.1 or elec[2] < -3.1) :
    #    if (L1Obj[2] > 0 and elec[2] < 0) or (L1Obj[2] < 0 and elec[2] > 0) : 
    #        if L1Obj[2] - elec[2] > 0.2 : 
    #            #dr2 = math.sqrt( (L1Obj[1] - elec[1])**2 + (L1Obj[2] - elec[2])**2 )
    #            print "dr",dr,"dPhi > 0.2",L1Obj[2], elec[2]
    #print dr
    if dr < 0.2 :
        etMatch.Fill( L1Obj[0] )
        dEta.Fill( L1Obj[1] - elec[1] )
        #print L1Obj[2], elec[2]
        #if L1Obj[2] - elec[2] > 0.2 : print "dPhi > 0.2",L1Obj[2], elec[2]
        #if L1Obj[2] > 0 and elec[2] < 0 : print "dPhi",L1Obj[2], elec[2]
        #if L1Obj[2] < 0 and elec[2] > 0 : print "dPhi",L1Obj[2], elec[2]
        dPhi.Fill( calcDPhi(L1Obj[2], elec[2]) )
        
c.Clear()
c.SetLogy(0)
etAll.GetYaxis().SetTitle('Counts')
etAll.GetXaxis().SetTitle('L1 EG E_{T}')
etAll.Draw()
c.Print('/afs/cern.ch/user/t/truggles/www/TrkTrig/Stage2etAll.png')
c.Clear()
etMatch.GetYaxis().SetTitle('Counts')
etMatch.GetXaxis().SetTitle('L1 to Offline Matching, L1 EG E_{T}')
etMatch.Draw()
c.Print('/afs/cern.ch/user/t/truggles/www/TrkTrig/Stage2etMatch.png')
c.Clear()
dEta.GetYaxis().SetTitle('Counts')
dEta.GetXaxis().SetTitle('L1 to Offline Matching, L1 EG d#eta(L1 - offline)')
dEta.Draw()
c.Print('/afs/cern.ch/user/t/truggles/www/TrkTrig/Stage2dEta.png')
c.Clear()
dPhi.GetYaxis().SetTitle('Counts')
dPhi.GetXaxis().SetTitle('L1 to Offline Matching, L1 EG d#phi(L1 - offline)')
dPhi.Draw()
c.Print('/afs/cern.ch/user/t/truggles/www/TrkTrig/Stage2dPhi.png')

effGraph = ROOT.TGraphAsymmErrors( etMatch, etAll )
effGraph.GetYaxis().SetTitle('Eff. (L1 Et/L1 Et of Matching)')
effGraph.GetXaxis().SetTitle('L1 EG E_{T}')
c.Clear()
c.SetGrid()
effGraph.SetTitle("Stage 2 Efficiency")
effGraph.Draw()
c.Print('/afs/cern.ch/user/t/truggles/www/TrkTrig/Stage2EGEff.png')


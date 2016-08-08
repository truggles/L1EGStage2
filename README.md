# L1EGStage2
For creating eff, rate and resolution plots for Stage2

Setup:
```
scramv1 project CMSSW CMSSW_8_0_7
cd CMSSW_8_0_7/src
eval `scramv1 runtime -sh`
```

```
git cms-init
git remote add cms-l1t-offline git@github.com:cms-l1t-offline/cmssw.git
git fetch cms-l1t-offline
git cms-merge-topic cms-l1t-offline:l1t-integration-v47.0
git cms-addpkg L1Trigger/L1TCommon
git clone git@github.com:truggles/L1EGStage2.git
scram b -j 8
```

Currently set up to run over the default Stage2 recommendations from here:
https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideL1TStage2Instructions

This is using these datasets<BR>
rate: dataset=/ZeroBias1/Run2015D-v1/RAW<BR>
eff: dataset=/DoubleEG/Run2015D-ZElectron-PromptReco-v4/RAW-RECO<BR>

To run:
```
cd efficiencies
. submitEff.sh
cd ../rates/
. submitRates.sh
```

After files are finished:
```
python plotRatesAndEff.py
```

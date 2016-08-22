# L1EGStage2
For creating eff, rate and resolution plots for Stage2

Currently using CMSSW_8_0_9 with checkout tag v76.1, most up to date as of Aug 8, 2016

Setup:
```
cmsrel CMSSW_8_0_9
cd CMSSW_8_0_9/src
eval `scramv1 runtime -sh`
git cms-init
git remote add cms-l1t-offline git@github.com:cms-l1t-offline/cmssw.git
git fetch cms-l1t-offline
git cms-merge-topic --unsafe cms-l1t-offline:l1t-integration-v78.0
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


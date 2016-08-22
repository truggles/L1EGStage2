date=2016Aug04

echo "hadd Efficiency file"
hadd -f L1Eff.root /data/truggles/TTEffDefault${date}-l1Ntuple_RAW2DIGI/l1Ntuple_RAW2DIGI-*/*.root

echo "hadd Rates file"
hadd -f L1Rates.root /data/truggles/TTRateDefault${date}-l1Ntuple_RAW2DIGI/l1Ntuple_RAW2DIGI-*/*.root

date=2016Aug21

farmoutAnalysisJobs \
        --input-file-list=rateFiles80X.txt \
        --input-files-per-job=1 \
        --output-dir=. \
        TTRateDefault${date} $CMSSW_BASE l1Ntuple_RAW2DIGI.py




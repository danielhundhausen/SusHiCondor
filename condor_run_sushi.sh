#!/bin/bash
initial_dir=$(pwd)
# Setup CMSSW
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd ../uhh2_run_ii_106x_v2/CMSSW_10_6_28/src/
eval `scramv1 runtime -sh`

# Go back to limits/ and execute runFits.py
cd $initial_dir
./condor_run_sushi.py $1 $2 $3 $4

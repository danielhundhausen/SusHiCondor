#!/nfs/dust/cms/user/hundhad/anaconda3/envs/py39/bin/python
from config_writer import ParamConfig

import numpy as np


params = ParamConfig()
mode = params.active_mode

if mode == "MA-MH":
    params = params["MA-MH"]
    job_args = [
        (MA, MH, tanb, params["sinba"])
        for MA in np.arange(params["mass_range"][0], params["mass_range"][1] + 1, params["stepsize_massgrid"])
        for MH in np.arange(params["mass_range"][0], params["mass_range"][1] + 1, int(params["stepsize_massgrid"] * params["points_per_job"]))
        for tanb in params["values_tanb"]
    ]
    cmd_args = []
    for args in job_args:
        cmd_args.append(f"{args[0]}, {args[1]}, {args[2]}, {args[3]}\n")


if mode == "MA-TANB":
    params = params["MA-TANB"]
    job_args = [
        (MA, MH, tanb, params["sinba"])
        for MA in np.arange(params["ma_range"][0], params["ma_range"][1] + 1, params["stepsize_ma"])
        for tanb in np.arange(params["tanb_range"][0], params["tanb_range"][1] + 1, params["stepsize_tanb"] * params["points_per_job"])
        for MH in params["values_mh"]
    ]
    cmd_args = []
    for args in job_args:
        cmd_args.append(f"{args[0]}, {args[1]}, {args[2]}, {args[3]}\n")


if mode == "TANB-SINBA":
    params = params["TANB-SINBA"]
    job_args = [
        (params["MA"], params["MH"], tanb, sinba)
        for tanb in np.arange(params["tanb_range"][0], params["tanb_range"][1] + 1, params["stepsize_tanb"])
        for sinba in np.arange(params["sinba_range"][0], params["sinba_range"][1] + 1, params["stepsize_sinba"] * params["points_per_job"])
    ]
    cmd_args = []
    for args in job_args:
        cmd_args.append(f"{args[0]}, {args[1]}, {args[2]}, {args[3]}\n")


condor_submit = (
    'Requirements = ( OpSysAndVer == "CentOS7" )\n'
    "# Request_GPUs = 1\n"
    "universe          = vanilla\n"
    "# Running in local mode with 4 cpu slots\n"
    "request_cpus      = 4\n"
    "notification      = Error\n"
    "initialdir        = /nfs/dust/cms/user/hundhad/SusHi-1.7.0/\n"
    "output            = condor_logs/$(MA)-$(MH).o\n"
    "error             = condor_logs/$(MA)-$(MH).e\n"
    "log               = condor_logs/$(MA).log\n"
    "# Requesting CPU and DISK Memory - default +RequestRuntime of 3h stays unaltered\n"
    # "getenv            = True\n"
    "RequestMemory     = 2G\n"
    "RequestDisk       = 2G\n"
    "JobBatchName      = SusHiJobs\n"
    "executable = /nfs/dust/cms/user/hundhad/SusHi-1.7.0/condor_run_sushi.sh\n"
    f"arguments         = $(MA) $(MH) $(tanb) $(sinba)\n"
    f"queue MA, MH, tanb, sinba from ({''.join(cmd_args)})\n"
)


with open("condor.submit", "w") as f:
    f.write(condor_submit)


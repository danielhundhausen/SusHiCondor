#!/nfs/dust/cms/user/hundhad/anaconda3/envs/py39/bin/python
import argparse
import os

import numpy as np

from config_writer import ConfigWriter, CONFIG_DIR, OUTPUT_DIR, ParamConfig


PARAMS = ParamConfig()


def write_and_run(MA, MH, tanb, sinba):
    writer = ConfigWriter(MA, MH, tanb=tanb, sinba=sinba)
    ggX = writer.write_config()
    # Run SusHi
    os.system(
        f"./bin/sushi "
        f"{CONFIG_DIR}/{ggX}_MA-{MA}_MH-{MH}_tanb{tanb}_sinba{sinba}.in "
        f"{OUTPUT_DIR}/{ggX}_MA-{MA}_MH-{MH}_tanb{tanb}_sinba{sinba}.out"
    )


def run_MA_MH(MA: int, MH_min: int, tanb: float, sinba: float):
    params = PARAMS["MA-MH"]
    for MH in range(MH_min, MH_min + params["stepsize_massgrid"] * params["points_per_job"] + 1e-10, params["stepsize_massgrid"]):
        print(f"Generatring SusHi .in file for {MA}/{MH} ...")
        write_and_run(MA, MH, tanb, sinba)


def run_MA_TANB(MA: int, MH: int, tanb_min: float, sinba: float):
    params = PARAMS["MA-TANB"]
    for tanb in np.arange(tanb_min, tanb_min + params["stepsize_tanb"] * params["points_per_job"] + 1e-10, params["stepsize_tanb"]):
        print(f"Generatring SusHi .in file for {MA}/{tanb} ...")
        write_and_run(MA, MH, tanb, sinba)


def run_TANB_SINBA(MA: int, MH: int, tanb: float, sinba_min: float):
    params = PARAMS["TANB-SINBA"]
    for sinba in np.arange(sinba_min, sinba_min + params["stepsize_sinba"] * params["points_per_job"] + 1e-10, params["stepsize_sinba"]):
        print(f"Generatring SusHi .in file for tanb{tanb}/sinba{sinba} ...")
        write_and_run(MA, MH, tanb, sinba)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("MA", type=int)
    parser.add_argument("MH", type=int)
    parser.add_argument("tanb", type=float)
    parser.add_argument("sinba", type=float)
    args = parser.parse_args()

    if PARAMS.active_mode == "MA-MH":
        run_MA_MH(args.MA, args.MH, args.tanb, args.sinba)

    if PARAMS.active_mode == "MA-TANB":
        run_MA_TANB(args.MA, args.MH, args.tanb, args.sinba)

    if PARAMS.active_mode == "TANB-SINBA":
        run_TANB_SINBA(args.MA, args.MH, args.tanb, args.sinba)

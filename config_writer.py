#!/nfs/dust/cms/user/hundhad/anaconda3/envs/py39/bin/python
import os
import yaml

import numpy as np

CONFIG_DIR = "sushi_configs"
OUTPUT_DIR = "sushi_outputs"


# Create directories for config and output
os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


class ParamConfig:

    def __init__(self):
        with open("config.yaml", 'r') as f:
            self.params = yaml.load(f, Loader=yaml.Loader)

        for k, v in self.params.items():
            setattr(self, k, v)

    def __getitem__(self, item):
        return self.params[item]


class ConfigWriter:

    ggX_ID_map = {
        "ggh": 11,
        "ggH": 12,
        "ggA": 21,
    }

    def __init__(self, MA, MH, tanb, sinba):
        self.ggX = "ggA" if MA > MH else "ggH"
        self.MA = MA
        self.MH = MH
        self.tanb = tanb
        self.sinba = sinba
        # Load paramters from config.yaml
        self.params = ParamConfig()
        # Definitions
        self.MC = np.max(MA, MH)
        self.beta = np.arctan(tanb)

    @property
    def m12(self):
        # Choice of m12 suggested by Thomas Biekoetter
        return np.sqrt(np.max(self.MA, self.MH) ** 2 * np.sin(self.beta) * np.cos(self.beta))

    @property
    def ggXID(self):
        return self.ggX_ID_map[self.ggX]

    @property
    def config_string(self):
        return (
            f"Block SUSHI\n"
            f"  1   2         # model: 0 = SM, 1 = MSSM, 2 = 2HDM, 3 = NMSSM\n"
            f"  2   {self.ggXID}        # 11 = h, 12 = H, 21 = A\n"
            f"  3   0         # collider: 0 = p-p, 1 = p-pbar\n"
            f"  4   13000.d0  # center-of-mass energy in GeV\n"
            f"  5   2         # order ggh: -1 = off, 0 = LO, 1 = NLO, 2 = NNLO, 3 = N3LO\n"
            f"  6   2         # order bbh: -1 = off, 0 = LO, 1 = NLO, 2 = NNLO\n"
            f"  7   1         # electroweak cont. for ggh:\n"
            f"                # 0 = no, 1 = light quarks at NLO, 2 = SM EW factor\n"
            f" 19   0         # 0 = silent mode of SusHi, 1 = normal output\n"
            f" 20   0         # ggh@nnlo subprocesses: 0=all, 10=ind. contributions\n"
            f"Block 2HDMC   # 2HDMC arXiv:0902.0851\n"
            f" -1   0                  # CMD line mode: 0 direct link, 1 command line mode\n"
            f"  1   2                  # 2HDMC key, 1=lambda basis, 2=physical basis, 3=H2 basis\n"
            f"  2   {self.params.thdm_type}   # 2HDM version type: (1=Type I,2=Type II,3=Flipped,4=Lepton Specific) \n"
            f"  3   {self.tanb}        # tan(beta)\n"
            f"  4   {self.m12}         # m12\n"
            f"  21  {self.params.sm_higgs_mass}   # mh\n"
            f"  22  {self.MH}          # MH\n"
            f"  23  {self.MA}          # MA\n"
            f"  24  {self.MC}          # MC\n"
            f"  25  {self.sinba}      # sin(beta-alpha)\n"
            f"  26  0.d0               # lambda6\n"
            f"  27  0.d0               # lambda7\n"
            f"  50  1\n"
            f"Block SMINPUTS    # Standard Model inputs\n"
            f"  1   1.27934000e+02  # alpha_em^(-1)(MZ) SM MSbar\n"
            f"  2   1.16637000e-05  # G_Fermi\n"
            f"  3   1.17200000e-01  # alpha_s(MZ) SM MSbar\n"
            f"  4   9.11876000e+01  # m_Z(pole)\n"
            f"  5   4.20000000e+00  # m_b(m_b)\n"
            f"  6   1.73300000e+02  # m_t(pole)\n"
            f"  8   1.27500000e+00  # m_c(m_c)\n"
            f"Block DISTRIB\n"
            f"  1   0    # distribution : 0 = sigma_total, 1 = dsigma/dpt,\n"
            f"    #                2 = dsigma/dy,   3 = d^2sigma/dy/dpt\n"
            f"    #                (values for pt and y: 22 and 32)\n"
            f"  2   0    # pt-cut: 0 = no, 1 = pt > ptmin, 2 = pt < ptmax,\n"
            f"    #         3 = ptmin < pt < ptmax\n"
            f" 21   30.d0  # minimal pt-value ptmin in GeV\n"
            f" 22   100.d0  # maximal pt-value ptmax in GeV\n"
            f"  3   0    # rapidity-cut: 0 = no, 1 = Abs[y] < ymax,\n"
            f"    #    2 = Abs[y] > ymin, 3 = ymin < Abs[y] < ymax\n"
            f" 31   0.5d0  # minimal rapidity ymin\n"
            f" 32   1.5d0  # maximal rapidity ymax\n"
            f"  4   0    # 0 = rapidity, 1 = pseudorapidity\n"
            f"Block SCALES\n"
            f"  1   0.5   # renormalization scale muR/mh\n"
            f"  2   0.5  # factorization scale muF/mh\n"
            f" 11   1.0   # renormalization scale muR/mh for bbh\n"
            f" 12   0.25  # factorization scale muF/mh for bbh\n"
            f"  3   0         # 1 = Use (muR,muF)/Sqrt(mh^2+pt^2) for dsigma/dpt and d^2sigma/dy/dpt\n"
            f"Block RENORMBOT # Renormalization of the bottom sector\n"
            f"  1   0   # m_b used for bottom Yukawa:  0 = OS, 1 = MSbar(m_b), 2 = MSbar(muR)\n"
            f"  4   4.75d0    # Fixed value of m_b^OS\n"
            f"Block PDFSPEC\n"
            f"  1   MMHT2014lo68cl.LHgrid  # name of pdf (lo)\n"
            f"  2   MMHT2014nlo68cl.LHgrid  # name of pdf (nlo)\n"
            f"  3   MMHT2014nnlo68cl.LHgrid  # name of pdf (nnlo)\n"
            f"  4   MMHT2014nnlo68cl.LHgrid  # name of pdf (n3lo)\n"
            f" 10  0    # set number - if different for LO, NLO, NNLO, N3LO use entries 11, 12, 13\n"
            f"Block VEGAS\n"
            f"# parameters for NLO SusHi\n"
            f"         1    10000   # Number of points\n"
            f"         2        5   # Number of iterations\n"
            f"         3       10   # Output format of VEGAS integration\n"
            f"# parameters for ggh@nnlo:\n"
            f"         4     2000   # Number of points\n"
            f"         5        5   # Number of iterations\n"
            f"        14     5000   # Number of points in second run\n"
            f"        15        2   # Number of iterations in second run\n"
            f"         6        0   # Output format of VEGAS integration\n"
            f"# parameters for bbh@nnlo:\n"
            f"         7     2000   # Number of points\n"
            f"         8        5   # Number of iterations\n"
            f"        17     5000   # Number of points in second run\n"
            f"        18        2   # Number of iterations in second run\n"
            f"         9        0   # Output format of VEGAS integration\n"
            f"Block FACTORS\n"
            f"  1   0.d0  # factor for yukawa-couplings: c\n"
            f"  2   1.d0  # t\n"
            f"  3   1.d0  # b\n"
        )

    def write_config(self):
        fname = f"type{self.params.thdm_type}_{self.ggX}_MA-{int(self.MA)}_MH-{int(self.MH)}_tanb{self.tanb}_sinba{self.sinba}.in"
        print(fname)
        with open(os.path.join(CONFIG_DIR, fname), "w") as f:
            f.write(self.config_string)
        return self.ggX

import pynmet
import numpy as np
import matplotlib
import datetime as dt
import os
from pynmet.getdata import get_from_web
from pathlib import Path
import pandas as pd

#%matplotlib inline

sm = pynmet.inmet('A809')

sm.dados.Radiacao['2017/09/23'].plot()


#sm.resample('1m')
#sm.dados.Precipitacao.plot.bar()

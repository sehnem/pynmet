import pynmet
import numpy as np
import matplotlib

#%matplotlib inline

sm = pynmet.inmet('A803')
# sm.dados.Temperatura.plot()

sm.resample('1m')
sm.dados.Temperatura.plot()

import pynmet

sm = pynmet.inmet('A803')
sm.dados.Temperatura.plot()

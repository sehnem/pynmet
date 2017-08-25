import pandas as pd


class InmetSeries(pd.Series):
    
    @property
    def _constructor(self):
        return InmetSeries


class InmetDataFrame(pd.DataFrame):
    
    header = ['Temperatura', 'Temperatura_max', 'Temperatura_min', 'Umidade',
              'Umidade_max', 'Umidade_min', 'Ponto_orvalho', 
              'Ponto_orvalho_max', 'Ponto_orvalho_min', 'Pressao',
              'Pressao_max', 'Pressao_min', 'Vento_velocidade','Vento_direcao',
              'Vento_rajada', 'Radiacao', 'Precipitacao']
    
    unidades = {'Temperatura':'°C', 'Temperatura_max':'°C',
                'Temperatura_min':'°C', 'Umidade':'%',
                'Umidade_max':'%', 'Umidade_min':'%', 'Ponto_orvalho':'°C', 
                'Ponto_orvalho_max':'°C', 'Ponto_orvalho_min':'°C',
                'Pressao':'hPa', 'Pressao_max':'hPa', 'Pressao_min':'hPa',
                'Vento_velocidade':'m/s','Vento_direcao':'°',
                'Vento_rajada':'m/s', 'Radiacao':'kJ/m²', 'Precipitacao':'mm'}
    
    def __init__(self, *args, **kw):
        super(InmetDataFrame, self).__init__(*args, **kw)
    
    @property
    def _constructor(self):
        return InmetDataFrame
    
    _constructor_sliced = InmetSeries
    
    def set_inmet_header(self):
        self.columns = InmetDataFrame.header
    
#    def plot_chuva(self):
#        ax = self['Precipitacao'].plot.bar()
#        ax.set_xlabel('')
#        ax.set_ylabel(InmetDataFrame.unidades['Precipitacao'])
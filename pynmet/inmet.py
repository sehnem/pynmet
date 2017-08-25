import os
import pandas as pd
import datetime as dt
from .getdata import get_from_web


class inmet:
    
    pynmet_path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(pynmet_path, 'data', 'estacoes.csv')
    sites = pd.read_csv(filepath, index_col='codigo', dtype={'codigo':str,
                                                             'alt':int})
    
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
    
    def __init__(self, code = None, dia_i = None, dia_f = None, lat = None,
                 lon = None, tz = 'UTC'):
        
        if dia_i is None:
            self.dia_i = self.dia_f = dt.date.today().strftime("%d/%m/%Y")
        elif dia_f is None:
            self.dia_i = self.dia_f = dia_i
        else:
            self.dia_i = dia_i
            self.dia_f = dia_f
        
        if code is None:
            lat 

        if code in inmet.sites.index.values:
            self.code = code
            self.cod_OMM = inmet.sites.loc[code].cod_OMM
            self.inicio_operacao = inmet.sites.loc[code].inicio_operacao
            self.lat = inmet.sites.loc[code].lat
            self.lon = inmet.sites.loc[code].lon
            self.alt = inmet.sites.loc[code].alt
            self.tz = tz
        
        self.dados = get_from_web(self.code, self.dia_i, self.dia_f)
        self.dados.tz_convert(self.tz)
    
    def plot_chuva(self):
        ax = self.dados['Precipitacao'].plot.bar()
        ax.set_xlabel('')
        ax.set_ylabel(InmetDataFrame.unidades['Precipitacao'])


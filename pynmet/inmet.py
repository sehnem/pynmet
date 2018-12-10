"""
Esse módulo é utilizado para realizar a interface com dados do inmet definindo
classes e os principais métodos associados a elas. É o principal método do
pacote.
"""

import os
import pandas as pd
import numpy as np
from .getdata import get_data
from .calculations import avg_wind


header = ['Temperatura', 'Temperatura_max', 'Temperatura_min', 'Umidade',
          'Umidade_max', 'Umidade_min', 'Ponto_orvalho',
          'Ponto_orvalho_max', 'Ponto_orvalho_min', 'Pressao',
          'Pressao_max', 'Pressao_min', 'Vento_velocidade',
          'Vento_direcao', 'Vento_rajada', 'Radiacao', 'Precipitacao']

unidades = {'Temperatura': '°C', 'Temperatura_max': '°C',
            'Temperatura_min': '°C', 'Umidade': '%',
            'Umidade_max': '%', 'Umidade_min': '%', 'Ponto_orvalho': '°C',
            'Ponto_orvalho_max': '°C', 'Ponto_orvalho_min': '°C',
            'Pressao': 'hPa', 'Pressao_max': 'hPa', 'Pressao_min': 'hPa',
            'Vento_velocidade': 'm/s', 'Vento_direcao': '°',
            'Vento_rajada': 'm/s', 'Radiacao': 'kJ/m²',
            'Precipitacao': 'mm'}


pynmet_path = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(pynmet_path, 'data', 'estacoes.csv')
sites = pd.read_csv(filepath, index_col='codigo', dtype={'codigo': str,
                                                         'alt': int})


def inmet(code, local=False):
    if code in sites.index.values:
        df = get_data(code, local)
        df.code = code
        df.cod_OMM = sites.loc[code].cod_OMM
        df.inicio_operacao = sites.loc[code].inicio_operacao
        df.lat = sites.loc[code].lat
        df.lon = sites.loc[code].lon
        df.alt = sites.loc[code].alt
        df.nome = sites.loc[code].nome[:-5]
        return df


@pd.api.extensions.register_dataframe_accessor("met")
class MetFunctions(object):
    def __init__(self, pandas_obj):
        self._obj = pandas_obj

    def plot_t(self):
        # return the geographic center point of this DataFrame
        self._obj['Temperatura'].plot()
        lat = self._obj.lat
        return float(lat+10)

    def resample(self, periodo):
        metodos = {'Temperatura': np.mean, 'Temperatura_max': np.max,
                   'Temperatura_min': np.min, 'Umidade': np.mean,
                   'Umidade_max': np.max, 'Umidade_min': np.min,
                   'Ponto_orvalho': np.mean, 'Ponto_orvalho_max': np.max,
                   'Ponto_orvalho_min': np.min, 'Pressao': np.mean,
                   'Pressao_max': np.max, 'Pressao_min': np.min,
                   'Vento_velocidade': np.mean, 'Vento_direcao': avg_wind,
                   'Vento_rajada': np.max, 'Radiacao': np.mean,
                   'Precipitacao': np.sum}
        return self.resample(periodo).agg(metodos)


# https://pandas.pydata.org/pandas-docs/stable/extending.html

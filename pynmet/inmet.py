"""
Esse módulo é utilizado para realizar a interface com dados do inmet definindo
classes e os principais métodos associados a elas. É o principal método do
pacote.
"""

import os
import pandas as pd
import numpy as np
from .getdata import get_from_ldb
from .calculations import avg_wind


class inmet:

    """
    Classe que agrupa dados e prâmetros de um estação do inmet.
    Parametros
    ----------
    code : string
        O código da estação do INMET, ex: 'A803'
    db : string, default $HOME/.inmetdb.hdf
        Banco de dados local utilizado para armazenamento de dados
    """
    pynmet_path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(pynmet_path, 'data', 'estacoes.csv')
    sites = pd.read_csv(filepath, index_col='codigo', dtype={'codigo': str,
                                                             'alt': int})

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

    def __init__(self, code=None, db=os.getenv("HOME") + '/.inmetdb.hdf'):
        if code in inmet.sites.index.values:
            self.code = code
            self.cod_OMM = inmet.sites.loc[code].cod_OMM
            self.inicio_operacao = inmet.sites.loc[code].inicio_operacao
            self.lat = inmet.sites.loc[code].lat
            self.lon = inmet.sites.loc[code].lon
            self.alt = inmet.sites.loc[code].alt
        self.dados = get_from_ldb(code, db)

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
        self.dados = self.dados.resample(periodo).agg(metodos)

    def set_timezone(self, tz='America/Sao_Paulo'):
        self.dados = self.dados.tz_convert(tz)


class inmet_region(object):

    def __init__(self, arg):
        self.arg = arg

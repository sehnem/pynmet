import base64
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime as dt
import os

from .frame import InmetDataFrame


class inmet:
    
    pag = 'http://www.inmet.gov.br/sonabra/pg_dspDadosCodigo_sim.php?'
    pynmet_path = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(pynmet_path, 'data', 'estacoes.csv')
    sites = pd.read_csv(filepath, index_col='codigo', 
                        dtype={'codigo':str, 'alt':int})

    
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
            
    def get_from_web(self):
        decoded = base64.b64encode(self.code.encode('ascii')).decode()
        est = self.pag + decoded
        page = requests.get(est)
        soup = BeautifulSoup(page.content, 'lxml')
        base64Str = str(soup.findAll('img')[0])[-11:-3]
        encoded = base64.b64decode(base64Str.encode('ascii')).decode()
        post_request = {'aleaValue': base64Str, 'dtaini': self.dia_i,
                        'dtafim': self.dia_f, 'aleaNum': encoded}
        page_table = requests.post(est, post_request)
        soup = BeautifulSoup(page_table.content, 'lxml')
        table = soup.find('tbody', align='right', valign='center')
        dados = []
        for line in table.findAll('tr'):
            temp = []
            for l in line.findAll('td'):
                temp.append(str(l.find('span').text))
            dados.append(temp)
        dados = InmetDataFrame(dados)
        data = pd.to_datetime(dados[0] + ' ' + dados[1], format="%d/%m/%Y %H")
        dados.set_index(data, inplace=True)
        dados = dados.drop([0, 1], axis=1)
        dados = dados.replace('////', np.nan)
        dados = dados.dropna(how='all')
        dados = dados.convert_objects(convert_numeric=True)
        dados.set_inmet_header()
        dados = dados.tz_localize('UTC')
        dados = dados.tz_convert(self.tz)
        return dados

import base64
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from .frame import InmetDataFrame


def get_from_web(code, dia_i, dia_f):
    pag = 'http://www.inmet.gov.br/sonabra/pg_dspDadosCodigo_sim.php?'
    decoded = base64.b64encode(code.encode('ascii')).decode()
    est = pag + decoded
    page = requests.get(est)
    soup = BeautifulSoup(page.content, 'lxml')
    base64Str = str(soup.findAll('img')[0])[-11:-3]
    encoded = base64.b64decode(base64Str.encode('ascii')).decode()
    post_request = {'aleaValue': base64Str, 'dtaini': dia_i,
                    'dtafim': dia_f, 'aleaNum': encoded}
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
    return dados
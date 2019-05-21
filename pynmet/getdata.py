import base64
import datetime as dt
import os
from io import StringIO

import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

pg_form = 'http://www.inmet.gov.br/sonabra/pg_dspDadosCodigo_sim.php?'
pg_data = 'http://www.inmet.gov.br/sonabra/pg_downDadosCodigo_sim.php'

header = ['Temperatura', 'Temperatura_max', 'Temperatura_min', 'Umidade',
          'Umidade_max', 'Umidade_min', 'Ponto_orvalho',
          'Ponto_orvalho_max', 'Ponto_orvalho_min', 'Pressao',
          'Pressao_max', 'Pressao_min', 'Vento_velocidade', 'Vento_direcao',
          'Vento_rajada', 'Radiacao', 'Precipitacao']

pynmet_path = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(pynmet_path, 'data', 'estacoes.csv')
sites = pd.read_csv(filepath, index_col='codigo',
                    dtype={'codigo': str, 'alt': int})


def b64_inmet(code, scheme='decode'):
    """
    Decoding/encoding of inmet base64 codes.

    Parameters
    ----------
    code : string, bytes
        String/code to be encoded/decoded.

    scheme : string, default 'decode'
        method to be used, 'decode' or 'encode'.

    Returns
    -------
    data : bytes, string
        The decoded/encoded string/code.
    """

    ascii_code = code.encode('ascii')
    if scheme == 'decode':
        data = base64.b64decode(ascii_code)
    elif scheme == 'encode':
        data = base64.b64encode(ascii_code).decode()
    else:
        raise ValueError("scheme argument must be 'encode' or 'decode'")

    return data


def clean_data_str(data_str):
    """
    Clean string retrieved from INMET page removing html tags and invalid
    data.
    
    Parameters
    ----------
    data_str : string
        String retrieved from INMET page.

    Returns
    -------
    data_str : string
        Cleaned string.
    """

    data_str = data_str.replace('\r', '').replace('\n', '')
    data_str = data_str.replace('\t', '')
    data_str = data_str.replace('<br>', '\n')
    data_str = data_str.replace('////', '').replace('///', '')
    data_str = data_str.replace('//', '').replace('/,', ',')

    return data_str


def inmet_string_to_df(data_str):
    data_str = clean_data_str(data_str)
    df = pd.read_csv(StringIO(data_str))
    df[['data', 'hora']] = df[['data', 'hora']].astype(str)
    data = pd.to_datetime(df['data'] + df['hora'], format="%d/%m/%Y%H")
    df.set_index(data, inplace=True)
    df.drop([' codigo_estacao', 'data', 'hora'], axis=1, inplace=True)
    df.columns = header
    df.dropna(how='all', inplace=True)
    df.sort_index(inplace=True)
    
    return df


def get_from_inmet(code, dia_i, dia_f):
    """
    Site do inmet
    """
    est = pg_form + b64_inmet(code, 'encode')
    session = requests.session()
    with session.get(est) as page:
        soup = BeautifulSoup(page.content, 'lxml')
        base64_str = str(soup.findAll('img')[0])[-11:-3]
        solved = b64_inmet(code, 'decode')
        post_request = {'aleaValue': base64_str,
                        'dtaini': dia_i,
                        'dtafim': dia_f,
                        'aleaNum': solved}
        session.post(est, post_request)
        try:  # exceção para estação sem dados no site do inmet
            data_str = session.get(pg_data).content.decode()
            df = inmet_string_to_df(data_str)
            return df
        except:
            df = pd.DataFrame(columns=header)
            return df
            pass


def db_engine(path=None):
    """
    Create the SQL database engine.
    
    Parameters
    ----------
    path : string, default None
        Path for the database engine.

    Returns
    -------
    data_str : Engine
        Engine from database.
    """

    if path is None:
        home = os.path.expanduser('~')
        path = os.path.join(home, '.cache', 'pynmet')
    if not os.path.exists(path):
        os.makedirs(path)
    engine = create_engine('sqlite:///' + os.path.join(path, 'inmet.db'), echo=False)

    return engine


def update_db(code, engine, force=False):
    """
    Update the given database based on station code.

    Parameters
    ----------
    code : string
        Code of inmet automatic weather station.

    engine : Engine
        Engine from database.

    force : boolean, default False
        Get all available data from INMET and overwrite database.
    """

    fmt = "%d/%m/%Y"
    dia_f = (dt.date.today() + dt.timedelta(1)).strftime(fmt)
    u_ano = dt.date.today() - dt.timedelta(days=365)
    if engine.dialect.has_table(engine, code) and not force:
        db = pd.read_sql(code, engine, columns=['TIME'], index_col='TIME')
        if len(db.index) == 0:
            dia_i = (u_ano).strftime(fmt)
        else:
            dia_u = db.index.max()
            if dia_u.date() < (u_ano):
                dia_i = (u_ano).strftime(fmt)
            else:
                dia_i = dia_u.strftime(fmt)  # TODO: warning for no index
    else:
        dia_i = (u_ano).strftime(fmt)

    dados = get_from_inmet(code, dia_i, dia_f)

    if engine.dialect.has_table(engine, code):
        dados = dados[~dados.index.isin(db.index)]

    dados.to_sql(code, engine, if_exists='append', index_label='TIME')


def read_db(code, engine):
    """
    """
    try:
        dados = pd.read_sql(code, engine, index_col='TIME')
    except:
        dados = pd.DataFrame(columns=header)

    return dados


def upgrade_db(path=None, engine=None):
    """
    """
    import tables
    
    if engine is None:
        engine = db_engine()

    if path is None:
        path = os.getenv("HOME") + '/.inmetdb.hdf'

    with tables.open_file(path, mode="r") as h5file:
        list(h5file.walk_groups())
        codes = h5file.root.__dict__['__members__']

    for code in codes:
        dados = pd.read_hdf(path, code)
        dados.index = dados.index.tz_localize(None)
        dados = dados.dropna(how='all')

        if engine.dialect.has_table(engine, code):
            db_index = pd.read_sql(code, engine, columns=['TIME'],
                                   index_col='TIME').index
            dados = dados[~dados.index.isin(db_index)]

        dados.to_sql(code, engine, if_exists='append', index_label='TIME')


def clean_duplicated():
    engine = db_engine()
    for code in sites.index:
        try:
            db = pd.read_sql(code, engine, index_col='TIME')
            db = db[~db.index.duplicated(keep='first')]
            db.to_sql(code, engine, if_exists='replace', index_label='TIME')
        except RuntimeWarning:
            print('It was not possible to clean {} data in the database'.format(
                code))


def get_data(code, local=False, force=False):
    """
    """
    engine = db_engine()

    if not local:
        update_db(code, engine, force)

    return read_db(code, engine)


def update_all(force=False):
    """
    """
    engine = db_engine()

    for code in sites.index:
        try:
            update_db(code, engine, force)
            print('{}: UPDATED'.format(code))
        except:
            print('It was not possible to retrieve {} data from INMET'.format(
                code))

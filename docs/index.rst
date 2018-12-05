.. toctree::
  :maxdepth: 1

  index

Pynmet
========

Pacote para aquisição automática dos dados de estações automáticas do INMET



Utilização
========

Download de dados de uma estação e geração do gráfico de temperatura.

.. code-block:: python

  import pynmet
  # Código da estação ex: A803
  estacao = pynmet.inmet('A803')
  estacao.dados.Temperatura.plot()

Os dados baixados são armazenados em um objeto que contém os dados extraídos e algumas informações da estação. Os dados são armazenados em "dados" que é um dataframe do pandas.

Os dados baixados são armazenados em um arquivo no $HOME do usuário. Toda vez que é utilizado o pacote atualiza com os últimos dados. Como o Inmet só disponibiliza o período de um ano em seu site esse é o período máximo na primeira vez que se carrega a estação.

A primeira vez utilização de cada estação leva um tempo maior para o carregamento pois são baixados 365 dias do site do INMET. É possível realizar o download ou atualização de todas as estações.

.. code-block:: python

  import pynmet
  # Atualiza todas as estações
  pynmet.update_all()

A primeira atualização demora mais de 1h porém novas atualizações de todas as estações levam menos de 10 minutos em conexões boas.


Contribua
========

- Issue Tracker: gitlab.com/sehnem/pynmet/issues
- Source Code: gitlab.com/sehnem/pynmet

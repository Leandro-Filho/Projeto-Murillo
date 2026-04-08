# Estação Meteorológica IoT 

Este projeto é um sistema completo de Internet das Coisas (IoT) para monitoramento meteorológico. Ele lê dados de temperatura e umidade (reais via Arduino ou simulados), envia para uma API REST construída em Python (Flask), armazena em um banco de dados SQLite e exibe os resultados em tempo real através de um painel web interativo.

## Estrutura do Projeto

Abaixo está a organização dos arquivos e diretórios do projeto:

> ```text
> Projeto Murillo/
> ├── requirements.txt         # Lista de dependências do Python
> ├── README.md                # Documentação do projeto
> └── src/                     # Código-fonte principal
>     ├── app.py               # Servidor web e API REST (Flask)
>     ├── config.py            # Configurações do sistema e porta serial
>     ├── database.py          # Funções de interação com o SQLite (CRUD)
>     ├── schema.sql           # Script de criação das tabelas do banco
>     ├── serial_reader.py     # Script que lê dados do Arduino/Simulador
>     └── templates/           # Arquivos de interface Front-end
>         ├── index.html       # Painel com gráficos (Chart.js)
>         └── historico.html   # Tabela com histórico completo
> ```

---

## Pré-requisitos e Dependências

Para rodar este projeto, você precisará ter o **Python 3.8+** instalado.

Primeiro, crie um arquivo chamado `requirements.txt` na raiz do seu projeto e cole o seguinte conteúdo nele:

```text
Flask>=3.0.0
pyserial>=3.5
requests>=2.31.0
```

## Como Instalar e Executar

Siga o passo a passo abaixo para rodar o projeto localmente:

### 1. Preparação do Ambiente
Abra o seu terminal na pasta raiz do projeto e crie/ative um ambiente virtual:

**No Linux / macOS:**
```bash
python -m venv .venv
source .venv/bin/activate
```
**No Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### 2. Instalação das Bibliotecas
Com o ambiente ativado (.venv), instale as dependências executando:

```bash
pip install -r requirements.txt
```

#### 3. Configuração do Hardware 

- Faça o upload do código C++ (leitura do sensor DHT) para a placa usando a IDE do Arduino.

- Abra o arquivo src/config.py.

- Altere MODO_SIMULACAO = False.

- Ajuste a PORTA_SERIAL para a porta correta do seu dispositivo (ex: COM3 ou /dev/ttyACM0).

#### 4. Executando o Sistema

O sistema exige que a API (Flask) e o Leitor Serial rodem simultaneamente. Você precisará de dois terminais separados (lembre-se de ativar o ambiente virtual executando source .venv/bin/activate em ambos!).

**Terminal 1 (Iniciando a API e a Interface Web):**
```bash
python src/app.py
```
**Acesse o painel web no navegador através do endereço: http://127.0.0.1:5000**

**Terminal 2 (Iniciando o Leitor/Simulador de Sensores):**

```bash
python src/serial_reader.py
```

Este script ficará rodando em loop, lendo os dados da porta serial (ou gerando simulações) e enviando para a API via método POST a cada 5 segundos.

## Como Ver o Vídeo da Aplicação?

Acesse por aqui -> Clique Aqui[xxxxxx]
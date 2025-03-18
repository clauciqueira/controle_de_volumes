# Controle de Volumes

## Descrição

Meu Projeto é uma aplicação Python que permite gerenciar dados de quantidade de volumes e quando foram enviados para filiais. O objetivo deste projeto é facilitar a organização dos volumes de envio para cada loja.

## Por que é útil?

Este projeto é útil porque ajuda a economizar tempo e melhora a eficiência no gerenciamento de volumes.

## Começando

Para começar a usar o projeto, siga estas etapas:

### Pré-requisitos

- Certifique-se de ter o Python 3.x instalado em seu sistema.
- Instale as dependências necessárias executando:
  ```bash
  pip install -r requirements.txt
  ```

### Clonar o Repositório

Clone o repositório do GitHub:

```bash
git clone https://github.com/clauciqueira/controle_de_volumes.git
```

## Criar Executável e Instalador

### Usando cx_Freeze

Certifique-se de que o arquivo `setup.py` esteja salvo no diretório raiz do projeto `d:\controle_de_volumes` e execute-o a partir desse diretório:

```bash
cd d:\controle_de_volumes
python setup.py build
```

Para criar o instalador MSI, execute:

```bash
python setup.py bdist_msi
```

Os arquivos gerados serão salvos no diretório `dist`.

### Usando PyInstaller

Certifique-se de que o arquivo `setup_pyinstaller.spec` esteja salvo no diretório raiz do projeto `d:\controle_de_volumes` e execute-o a partir desse diretório:

```bash
cd d:\controle_de_volumes
pyinstaller setup_pyinstaller.spec
```

Os arquivos gerados serão salvos no diretório `dist`.

## Depuração

Para depurar o executável, você pode usar as seguintes opções:

1. Adicione `print` statements no código para verificar o fluxo de execução.
2. Verifique os arquivos de log gerados para mensagens de erro.
3. Utilize um depurador como `pdb` para depuração interativa.

Para iniciar a depuração com `pdb`, adicione a seguinte linha no ponto onde deseja iniciar a depuração:

```python
import pdb; pdb.set_trace()
```

## Manutenção

Este projeto é mantido por:

Claudecir C. Lemos - c.ciqueira@hotmail.com

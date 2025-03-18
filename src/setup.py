from setuptools import setup, find_packages  

setup(  
    name='MeuProjeto',  # Corrigido para não conter espaços  
    version='1.0',  
    author='Claudecir C. Lemos',  
    author_email='c.ciqueira@hotmail.com',  
    description='Uma descrição breve do seu projeto tem por função principal controle de volumes.',  
    long_description=open('README.md').read(),  # Se você tiver um arquivo README.md  
    long_description_content_type='text/markdown',  
    url='https://github.com/usuario/meu_projeto',  # URL do repositório, se aplicável  
    packages=find_packages(),  # Encontra automaticamente os pacotes  
    install_requires=[  
        'beeware',  # Dependências do seu projeto  
    ],  
    classifiers=[  
        'Programming Language :: Python :: 3',  
        'License :: OSI Approved :: MIT License',  # Altere conforme a licença  
        'Operating System :: OS Independent',  
    ],  
    python_requires='>=3.6',  # Especifique a versão mínima do Python  
)  
# MongoDB Product Updater

Este projeto contém um script em Python que realiza a atualização de registros em uma coleção MongoDB com base em um arquivo CSV. O script é projetado para ativar/desativar produtos e atualizar informações específicas como tempo de entrega, estoque real e status de SEO.

## Funcionalidades

- **Atualização de produtos**: O script lê um arquivo CSV contendo informações de produtos e atualiza a coleção MongoDB correspondente.
- **Remoção de duplicatas**: Mantém apenas o registro com menor prazo para cada ID de produto no CSV.
- **Determinação automática de SEO ativo**: Define o campo `activeForSeo` com base em regras específicas.
- **Registro de operações**: As operações de atualização e desativação são registradas em um arquivo de log para fácil acompanhamento.

## Requisitos

- Python 3.x
- Bibliotecas Python:
  - `pandas`
  - `pymongo`
  - `logging`
- MongoDB

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/tiagoceridorio/mongodb-product-updater.git
   ```

2. Instale as dependências necessárias:

   ```bash
   pip install pandas pymongo
   ```

3. Configure o MongoDB:

   Certifique-se de que o MongoDB esteja rodando e acessível. Atualize a string de conexão no script se necessário.

## Uso

1. Coloque o arquivo CSV contendo os dados dos produtos no mesmo diretório que o script. O arquivo deve ter o nome `update.29.07.csv` ou modifique o caminho para o arquivo CSV no script.

2. Execute o script:

   ```bash
   python update_products.py
   ```

3. O script irá:

   - Carregar e processar o CSV.
   - Atualizar ou desativar produtos na coleção MongoDB com base nas informações do CSV.
   - Registrar as operações realizadas no arquivo `update_products.log`.

## Logs

Os logs de execução são armazenados no arquivo `update_products.log`, onde você pode verificar o status das atualizações realizadas, incluindo sucessos e erros de validação.

## Estrutura do Projeto

```plaintext
mongodb-product-updater/
├── update_products.py      # Script principal para atualização de produtos
├── update.29.07.csv        # Arquivo CSV com dados dos produtos
└── update_products.log     # Arquivo de log gerado pelo script
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto é licenciado sob a [MIT License](LICENSE).

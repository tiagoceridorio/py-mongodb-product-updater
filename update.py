import pandas as pd
import logging
from pymongo import MongoClient

# Configurações do MongoDB
mongo_client = MongoClient('mongodb+srv://localhost/')
db = mongo_client['graodegente']
collection = db['m_product']

# Configurações de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Adicionar manipulador de arquivo
file_handler = logging.FileHandler('update_products.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Carregar a lista CSV
csv_path = 'update.29.07.csv'
df = pd.read_csv(csv_path)

# Ordenar o DataFrame por ID e prazo
df_sorted = df.sort_values(by=['ID', 'prazo'])

# Remover duplicatas mantendo o registro com menor prazo para cada ID
df_filtered = df_sorted.drop_duplicates(subset=['ID'], keep='first')

# Função para determinar o valor de activeForSeo
def determine_active_for_seo(mix_value):
    if pd.isna(mix_value) or mix_value == '#N/A':
        return True
    return False

# Obter todos os produtos da coleção
all_products = collection.find()

# Iterar sobre todos os produtos
for product in all_products:
    product_id = product['productId']
    matching_rows = df_filtered[df_filtered['ID'] == product_id]
    
    if not matching_rows.empty:
        for _, row in matching_rows.iterrows():
            prazo = row['prazo']
            mix = row['Mix']
            quantidade = row['Quantidade']
            active_for_seo = determine_active_for_seo(mix)
            
            # Ativar o registro, atualizar deliveryTime, realStock e definir activeForSeo
            result = collection.update_many(
                {'productId': product_id},
                {'$set': {
                    'isActive': True,
                    'deliveryTime': prazo,
                    'activeForSeo': active_for_seo,
                    'realStock': quantidade
                }}
            )
            if result.modified_count > 0:
                # Validação da atualização
                updated_product = collection.find_one({'productId': product_id})
                if updated_product and updated_product['deliveryTime'] == prazo and \
                   updated_product['activeForSeo'] == active_for_seo and \
                   updated_product['realStock'] == quantidade:
                    log_message = (f'Produto {product_id} atualizado e validado: '
                                   f'isActive=True, deliveryTime={prazo}, '
                                   f'activeForSeo={active_for_seo}, realStock={quantidade}')
                    logger.info(log_message)
                else:
                    logger.error(f'Erro na validação do produto {product_id}')
    else:
        # Desativar o registro
        result = collection.update_many(
            {'productId': product_id},
            {'$set': {'isActive': False}}
        )
        if result.modified_count > 0:
            # Validação da desativação
            updated_product = collection.find_one({'productId': product_id})
            if updated_product and not updated_product['isActive']:
                log_message = f'Produto {product_id} desativado e validado: isActive=False'
                logger.info(log_message)
            else:
                logger.error(f'Erro na validação da desativação do produto {product_id}')

print("Atualização completa.")

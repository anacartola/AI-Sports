import pandas as pd
import numpy as np
# %%%
# Definindo os parâmetros
num_clients = 1000
np.random.seed(42)

# Definindo as categorias de consumidores
categories = ['free-to-play', 'premium', 'ultimate']
payment_options = {
    'premium': {'one_time': 64.50, 'monthly': 5.50, 'monthly_count': 12},
    'ultimate': {'one_time': 140.00, 'monthly': 12.00, 'monthly_count': 12}
}

# Função para gerar novos clientes ao longo do ano
def generate_new_clients(start_id, num_new_clients, start_date):
    new_clients = []
    for i in range(num_new_clients):
        client_id = start_id + i
        initial_category = np.random.choice(categories, p=[0.11, 0.74, 0.15])
        new_clients.append({
            'client_id': client_id,
            'initial_category': initial_category,
            'current_category': initial_category,
            'start_date': start_date
        })
    return new_clients

# Função para calcular a receita e gerar as datas de pagamento
def generate_payment_records(client):
    payment_records = []
    start_date = pd.Timestamp(client['start_date'])
    current_date = start_date
    
    # Gerando os pagamentos conforme o nível inicial
    initial_revenue, current_revenue = 0, 0
    if client['initial_category'] == 'premium':
        if np.random.rand() < 0.5:
            initial_revenue = payment_options['premium']['one_time']
            payment_records.append({'client_id': client['client_id'], 'category': 'premium', 'payment_date': current_date, 'amount': initial_revenue})
        else:
            for month in range(12):
                current_date += pd.DateOffset(months=1)
                payment_records.append({'client_id': client['client_id'], 'category': 'premium', 'payment_date': current_date, 'amount': payment_options['premium']['monthly']})
            initial_revenue = payment_options['premium']['monthly'] * payment_options['premium']['monthly_count']
    elif client['initial_category'] == 'ultimate':
        if np.random.rand() < 0.5:
            initial_revenue = payment_options['ultimate']['one_time']
            payment_records.append({'client_id': client['client_id'], 'category': 'ultimate', 'payment_date': current_date, 'amount': initial_revenue})
        else:
            for month in range(12):
                current_date += pd.DateOffset(months=1)
                payment_records.append({'client_id': client['client_id'], 'category': 'ultimate', 'payment_date': current_date, 'amount': payment_options['ultimate']['monthly']})
            initial_revenue = payment_options['ultimate']['monthly'] * payment_options['ultimate']['monthly_count']

    # Gerando os pagamentos conforme o nível atual, caso tenha havido mudança
    if client['current_category'] != client['initial_category']:
        change_date = start_date + pd.DateOffset(months=np.random.randint(1, 12))
        current_date = change_date
        if client['current_category'] == 'premium':
            if np.random.rand() < 0.5:
                current_revenue = payment_options['premium']['one_time']
                payment_records.append({'client_id': client['client_id'], 'category': 'premium', 'payment_date': current_date, 'amount': current_revenue})
            else:
                for month in range(current_date.month, 12):
                    current_date += pd.DateOffset(months=1)
                    payment_records.append({'client_id': client['client_id'], 'category': 'premium', 'payment_date': current_date, 'amount': payment_options['premium']['monthly']})
                current_revenue = payment_options['premium']['monthly'] * (12 - current_date.month + 1)
        elif client['current_category'] == 'ultimate':
            if np.random.rand() < 0.5:
                current_revenue = payment_options['ultimate']['one_time']
                payment_records.append({'client_id': client['client_id'], 'category': 'ultimate', 'payment_date': current_date, 'amount': current_revenue})
            else:
                for month in range(current_date.month, 12):
                    current_date += pd.DateOffset(months=1)
                    payment_records.append({'client_id': client['client_id'], 'category': 'ultimate', 'payment_date': current_date, 'amount': payment_options['ultimate']['monthly']})
                current_revenue = payment_options['ultimate']['monthly'] * (12 - current_date.month + 1)

    annual_revenue = initial_revenue + current_revenue
    return payment_records, annual_revenue

# Inicializando a lista de clientes
clients = []

# Gerando os clientes mês a mês
for month in range(1, 13):
    new_clients = generate_new_clients((month - 1) * num_clients + 1, num_clients, f'2024-{month:02d}-01')
    clients.extend(new_clients)

# Lista para armazenar todos os registros de pagamento
all_payment_records = []
total_revenue = 0

# Gerando os registros de pagamento para cada cliente
for client in clients:
    payment_records, annual_revenue = generate_payment_records(client)
    all_payment_records.extend(payment_records)
    total_revenue += annual_revenue

# Criando DataFrames para os clientes e registros de pagamento
df_clients = pd.DataFrame(clients)
payment_df = pd.DataFrame(all_payment_records)

# Exportando para Excel
with pd.ExcelWriter('clientes.xlsx') as writer:
    df_clients.to_excel(writer, sheet_name='Clients', index=False)
    payment_df.to_excel(writer, sheet_name='Payments', index=False)

# %%

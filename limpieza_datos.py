import pandas as pd
import io

# Cargar los datos
df = pd.read_csv('desafio_2026/events_raw.csv')

# Eliminar duplicados exactos y por event_id (priorizando la primera aparición)
df = df.drop_duplicates(subset=['event_id'], keep='first')

# Convertir timestamp a formato datetime
df['event_timestamp'] = pd.to_datetime(df['event_timestamp'])

# Llenamos con "unknown" o podrías usar la moda (el más frecuente)
df['device'] = df['device'].fillna('unknown')

# Para logins, el monto debe ser 0.0
df.loc[df['event_type'] == 'login', 'amount'] = df.loc[df['event_type'] == 'login', 'amount'].fillna(0.0)

# Para compras (purchase) sin monto, imputamos con la mediana para no afectar promedios
median_purchase = df[df['event_type'] == 'purchase']['amount'].median()
df.loc[df['event_type'] == 'purchase', 'amount'] = df.loc[df['event_type'] == 'purchase', 'amount'].fillna(median_purchase)

# Si es una compra y no tiene moneda, ponemos USD (que es la predominante)
df.loc[df['event_type'] == 'purchase', 'currency'] = df.loc[df['event_type'] == 'purchase', 'currency'].fillna('USD')

# Limpiar espacios en blanco en strings (por si acaso)
df['country'] = df['country'].str.strip()

#print("Resumen de limpieza:")
#print(df.info())
#print("\nPrimeras filas limpias:")
#print(df.head())

# seleccionamos las columnas relevantes para un inicio de sesión
df_logins = df[df['event_type'] == 'login'][['event_id', 'user_id', 'event_timestamp', 'device', 'country']].copy()

# Seleccionamos columnas de transacciones 
df_purchases = df[df['event_type'] == 'purchase'][['event_id', 'user_id', 'event_timestamp', 'amount', 'currency', 'device', 'country']].copy()

df_purchases = df_purchases.dropna(subset=['amount'])

# --- EXPORTACIÓN ---

# Guardar en archivos separados
df_logins.to_csv('desafio_2026/tabla_logins.csv', index=False)
df_purchases.to_csv('desafio_2026/tabla_purchases.csv', index=False)
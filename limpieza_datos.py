import pandas as pd
import io

# 1. Cargar los datos
df = pd.read_csv('events_raw.csv')

## --- PROCESO DE LIMPIEZA ---

# 2. Eliminar duplicados exactos y por event_id (priorizando la primera aparición)
df = df.drop_duplicates(subset=['event_id'], keep='first')

# 3. Convertir timestamp a formato datetime
df['event_timestamp'] = pd.to_datetime(df['event_timestamp'])

# 4. Manejo de valores nulos en 'device'
# Llenamos con "unknown" o podrías usar la moda (el más frecuente)
df['device'] = df['device'].fillna('unknown')

# 5. Manejo de la columna 'amount' (Monto)
# Para logins, el monto debe ser 0.0
df.loc[df['event_type'] == 'login', 'amount'] = df.loc[df['event_type'] == 'login', 'amount'].fillna(0.0)

# Para compras (purchase) sin monto, imputamos con la mediana para no afectar promedios
median_purchase = df[df['event_type'] == 'purchase']['amount'].median()
df.loc[df['event_type'] == 'purchase', 'amount'] = df.loc[df['event_type'] == 'purchase', 'amount'].fillna(median_purchase)

# 6. Estandarizar moneda
# Si es una compra y no tiene moneda, ponemos USD (que es la predominante)
df.loc[df['event_type'] == 'purchase', 'currency'] = df.loc[df['event_type'] == 'purchase', 'currency'].fillna('USD')

# 7. Limpiar espacios en blanco en strings (por si acaso)
df['country'] = df['country'].str.strip()

## --- VERIFICACIÓN ---

print("Resumen de limpieza:")
print(df.info())
print("\nPrimeras filas limpias:")
print(df.head())

# 8. Guardar el archivo limpio
# df.to_csv('archivo_limpio.csv', index=False)
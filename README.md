# Desafio Tecnico 2026
**Dev:** Daniel Carrasco
---

### Capas de Datos:
*   **Bronze Layer:** Ingesta as-is de la API en formato Parquet. Mantiene metadatos de auditoría .
*   **Silver Layer:** Datos tipados y normalizados, la limpieza de estos para evitar vacios y/o duplicidad de columnas.
*   **Gold Layer:** Optimizado para herramientas de BI (Looker,PowerBI) donde los reportes de negocio se pueden realizar conectandolos con unas consultas simples , y/o scripts sql simplificados desde origen (Bigquery).
* revisar los graficos adicionales para mayor información. carpeta images.

### Tablas generadas desde los archivos mediante ETL:
*   **Fact_Sales:** 
*   **Fact_Logins:** 
---

### Manejo de Late Events
Para cumplir con el supuesto de eventos que llegan con hasta 3 días de retraso, se genera un campo adicional par atener esto en cuenta ya que la fecha de ingesta y la fecha del evento seran diferentes, mas aun esto no afecta la generacion de datos, o la inserción dentro de las tablas.

### Evolución de Esquema 
Los campos nuevos detectados en la capa Bronze se almacenan en una columna de tipo `JSON` para evitar rupturas del pipeline, permitiendo que el se acceda a este campo independientemente y pueda ser analizado.

### Warehouse
Se selecciona BigQuery debido a:
*   **Escalabilidad:** Manejo nativo de volúmenes de TBs sin gestión de infraestructura.
*   **Costos:** Modelo de pago por consulta y almacenamiento separado.
*   **Particionamiento:** Soporte nativo para particiones por día y clustering.

---

## Reglas de Transformación y Limpieza
1.  **Deduplicación:** Se aplica `ROW_NUMBER() OVER(PARTITION BY event_id ORDER BY event_timestamp DESC)` para manejar re-intentos de la API.
2.  **Validación de Montos:** Filtro estricto `amount >= 0`. Los valores negativos se envían a una tabla de cuarentena para auditoría.
3.  **Tratamiento de Nulos:** 
    *   `user_id` faltante: Registro descartado (Hard Error).
    *   `device_info` faltante: Etiquetado como "Unknown".
4.  **Estandarización:** Conversión de todas las zonas horarias a `UTC` y normalización de códigos de país (ISO 3166-1 alpha-2).

---

## Calidad de Datos 
Se definieron los siguientes tests (ejecutados vía dbt o Great Expectations):
*   **Integridad Referencial:** Todo `sale` debe estar vinculado a un `user_id` existente en `Dim_User`.
*   **Unicidad:** El `event_id` debe ser único en la capa Silver.
*   **Consistencia Histórica:** Validación de que el `total_sum(amount)` del batch de hoy no varíe más de un 20% respecto al promedio de los últimos 7 días (detección de anomalías).

---

## Requerimientos de Negocio 
Las consultas SQL para obtener las métricas solicitadas (Revenue por usuario, País, Tasa de Conversión) se encuentran en la carpeta `/queries`.

> **Nota sobre Conversión:** Se calcula el ratio de usuarios que realizaron un `purchase` en una ventana de tiempo posterior a su primer `login`.

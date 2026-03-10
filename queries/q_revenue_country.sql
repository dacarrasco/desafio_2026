SELECT
country, currency, SUM(amount) as revenue
from
`bd_events.fact_purchase`
GROUP BY 1,2
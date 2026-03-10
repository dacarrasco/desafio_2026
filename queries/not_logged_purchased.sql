---query que devuelve las compras realizadas por usuarios que no han iniciado sesión en el mismo día o el día siguiente al inicio de sesión---
SELECT *
FROM 
`bd_events.fact_purchase` 
WHERE event_id not in(
SELECT b.event_id
FROM
`bd_events.fact_login` a
LEFT JOIN
`bd_events.fact_purchase` b
ON 
a.user_id = b.user_id
where 
DATE_DIFF(DATE(b.event_timestamp),DATE(a.event_timestamp),DAY)between 0 and 1)
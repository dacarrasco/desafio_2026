SELECT count(1)
FROM
`bd_events.fact_login` a
LEFT JOIN
`bd_events.fact_purchase` b
ON 
a.user_id = b.user_id
and 
 DATE(a.event_timestamp) = DATE(b.event_timestamp)
WHERE b.event_id is not null
--- este considera la compra realizada el mismo dia del login, si se quisiera considerar la compra realizada en cualquier momento despues del login, se podria cambiar la condicion a:
VENTAS = """
SELECT 
    FROM_UNIXTIME(v.created_at) as created_at, 
    v.total - COALESCE(c.deuda, 0) AS total, 
    v.id 
FROM 
    view_venta AS v
LEFT JOIN 
    (SELECT 
         id, 
         fecha_credito, 
         SUM(deuda) AS deuda 
     FROM 
         view_credito 
     WHERE 
         deuda > 1 
     GROUP BY 
         id, 
         fecha_credito) AS c 
ON 
    v.id = c.id 
    AND DATE(v.created_at) = DATE(c.fecha_credito);
"""

VENTA_DETALLE = """
SELECT
    vd.id,
    c.nombre AS cliente,
    c.id AS cliente_id,
    vd.venta_id,
    vd.producto_id,
    p.nombre AS producto,
    p.costo,
    p.precio_publico,
    p.precio_mayoreo,
    p.precio_menudeo,
    vd.cantidad,
    vd.precio_venta,
    vd.created_by,
    u.nombre AS creado_por,
    p.tipo_medida,
    -- Ajuste de cantidad dependiendo del tipo de medida
    CASE
        WHEN p.tipo_medida = 20 THEN 'Kilos'
        WHEN p.tipo_medida = 10 THEN 'Piezas'
        ELSE '--'
    END AS unidad_medida,
    pertenece.id AS pertenece_id,
    pertenece.nombre AS pertenece,
    suc.id AS ruta_asignada_id,
    suc.nombre AS ruta_asignada,
    vd.created_at,
    DATE(FROM_UNIXTIME(vd.created_at)) AS fecha,  -- Solo la fecha
    TIME(FROM_UNIXTIME(vd.created_at)) AS hora
FROM
    venta_detalle AS vd
INNER JOIN
    producto AS p ON p.id = vd.producto_id
INNER JOIN
    user AS u ON u.id = vd.created_by
LEFT JOIN
    venta AS v ON vd.venta_id = v.id  -- Cambiado de vd.id a vd.venta_id para corregir el JOIN
LEFT JOIN
    cliente AS c ON c.id = v.cliente_id
LEFT JOIN
    sucursal AS suc ON v.ruta_sucursal_id = suc.id
LEFT JOIN
    sucursal AS pertenece ON v.sucursal_id = pertenece.id
"""


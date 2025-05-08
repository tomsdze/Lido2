SELECT products.*,
           taisitajs.name AS taisitajs_nosaukums,
           krasa.name AS krasa_nosaukums,
           materiali.name AS materiali_nosaukums  -- Šeit ir "materiali"
    FROM products
    LEFT JOIN taisitajs ON products.taisitajs = taisitajs.id
    LEFT JOIN krasa ON products.krasa = krasa.id
    LEFT JOIN materiali ON products.material = materiali.id  -- Un šeit

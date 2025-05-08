SELECT
    "products".*,
    "taisitajs"."name" AS "taisitajs"
FROM       
    "products"
    LEFT JOIN "taisitajs" ON "products"."taisitajs_id" = "taisitajs"."id"
SELECT
    "products".*,
    "krasa"."name" AS "krasa"
FROM       
    "products"
    LEFT JOIN "krasa" ON "products"."krasa_id" = "krasa"."id"   
SELECT
    "products".*,
    "material"."name" AS "material"
FROM       
    "products"
    LEFT JOIN "material" ON "products"."material_id" = "material"."id"
    
    
    Sign in to enable AI completions, or disable inline completions in Settings (DBCode > AI).
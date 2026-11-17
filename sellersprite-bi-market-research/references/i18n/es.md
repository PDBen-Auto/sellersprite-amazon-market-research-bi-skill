# Investigación de mercado y BI SellerSprite

`sellersprite-bi-market-research` · Español

## Objetivo y alcance

Ampliar intención inicial a ASIN pertinentes, separar capas y crear BI auditable deduplicado por ASIN padre.

## Fundamento y dependencias

Mercado/tarea definidos, XLSX estándar/detallado y palabras clave necesarias, Python 3/openpyxl. En línea exige cuenta/navegador SellerSprite autorizado. Estimaciones no son liquidaciones Amazon.

## Entradas

Alcance/fecha/mercado/inclusión-exclusión, seed_keyword/seed_asins para descubrir; exportaciones condicionales; reglas/atributos/destinos opcionales. Ninguna credencial.

## Salidas

Manifest de candidatos con razones y cobertura detallada; padre/mes/año/YTD/periodos/ingresos de marca/momentum; dashboard.html autónomo, auditoría y carencias.

## Procedimiento

1. Fijar tarea
2. agrupar palabras y core_direct/adjacent_substitute/excluded_noise/review
3. revisar pendientes/exclusiones importantes
4. denominador solo aceptados con detalle
5. deduplicar padre/mes sin sumar hermanos
6. separar unidades/ingresos/GMV modelado/meses comparables
7. rango global fijo y momentum separado de oportunidades
8. revisar cifras/filtros/imágenes/páginas.

## Límites y condiciones de parada

Muestra de búsqueda no es TAM. Sin detalle no hay historia; sin ingresos, marca/rango N/A. Desconocido≠0. Separar US/CA/MX. No eludir acceso; rango por ingreso de muestra, no Amazon BSR.

## Ejemplo de solicitud

Usa `$sellersprite-bi-market-research` — Crear BI de mercado directo desde palabras/competidores sin añadir candidatos sin detalle al denominador de ventas; responde en español y conserva pruebas, datos desconocidos y límites de autorización.

## Especificación completa

[Entrada del Skill y referencias detalladas](../../SKILL.md).

Usa el idioma solicitado expresamente; si no se indica, sigue el de la petición. Conserva comandos, identificadores, claves JSON, valores enumerados, unidades y citas originales. Separa traducciones y originales. No deduzcas país, moneda ni jurisdicción por el idioma. Lee las referencias detalladas pertinentes y conserva todos los controles y permisos existentes.

Antes de entregar, concilia entradas, pruebas, valores ausentes, archivos y criterios de finalización originales. Marca como no verificados los pasos no ejecutados; el éxito de un script no valida conclusiones comerciales.

## Cobertura lingüística y validación

Esta guía localizada cubre objetivo, requisitos, entradas, salidas, pasos, ejemplos y límites; no traduce línea por línea todas las referencias. La documentación técnica detallada, los casos históricos, errores de scripts, interfaces de ejemplo e imágenes mantienen su idioma original y pueden explicarse a petición. Se comprueban estructura, enlaces y restricciones esenciales; no se afirma una revisión por hablantes nativos de cada idioma.


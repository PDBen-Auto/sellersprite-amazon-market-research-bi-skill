# Investigación de mercado y BI SellerSprite

[简体中文](README.zh-CN.md) | [English](README.en.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Español](README.es.md) | [Português](README.pt.md)

Usa el idioma solicitado expresamente; si no se indica, sigue el de la petición. Conserva comandos, identificadores, claves JSON, valores enumerados, unidades y citas originales. Separa traducciones y originales. No deduzcas país, moneda ni jurisdicción por el idioma. Lee las referencias detalladas pertinentes y conserva todos los controles y permisos existentes.

## Instalación y uso

Descarga o clona el repositorio y copia el directorio del Skill indicado, con sus references, scripts, assets y demás dependencias existentes, al directorio de Skills del entorno. Conserva el nombre y SKILL.md. Cambiar el idioma de la documentación no requiere otra instalación. Los comandos son opciones, no pruebas de instalación ni activación.

```sh
git clone https://github.com/PDBen-Auto/sellersprite-amazon-market-research-bi-skill.git
```

## Investigación de mercado y BI SellerSprite

`sellersprite-bi-market-research`

Ampliar intención inicial a ASIN pertinentes, separar capas y crear BI auditable deduplicado por ASIN padre.

Directorio del Skill: `.`

**Fundamento y dependencias**

Mercado/tarea definidos, XLSX estándar/detallado y palabras clave necesarias, Python 3/openpyxl. En línea exige cuenta/navegador SellerSprite autorizado. Estimaciones no son liquidaciones Amazon.

**Entradas**

Alcance/fecha/mercado/inclusión-exclusión, seed_keyword/seed_asins para descubrir; exportaciones condicionales; reglas/atributos/destinos opcionales. Ninguna credencial.

**Salidas**

Manifest de candidatos con razones y cobertura detallada; padre/mes/año/YTD/periodos/ingresos de marca/momentum; dashboard.html autónomo, auditoría y carencias.

[Procedimiento · Límites y condiciones de parada · Ejemplo de solicitud](references/i18n/es.md)

> Usa `$sellersprite-bi-market-research` — Crear BI de mercado directo desde palabras/competidores sin añadir candidatos sin detalle al denominador de ventas; responde en español y conserva pruebas, datos desconocidos y límites de autorización.

## Cobertura lingüística y validación

Esta guía localizada cubre objetivo, requisitos, entradas, salidas, pasos, ejemplos y límites; no traduce línea por línea todas las referencias. La documentación técnica detallada, los casos históricos, errores de scripts, interfaces de ejemplo e imágenes mantienen su idioma original y pueden explicarse a petición. Se comprueban estructura, enlaces y restricciones esenciales; no se afirma una revisión por hablantes nativos de cada idioma.

Antes de entregar, concilia entradas, pruebas, valores ausentes, archivos y criterios de finalización originales. Marca como no verificados los pasos no ejecutados; el éxito de un script no valida conclusiones comerciales.

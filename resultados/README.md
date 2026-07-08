# Corpus simulado de prueba — Proyecto IH-2025-I-445

## ⚠️ Naturaleza del corpus

**Todos los recursos de este paquete son deliberadamente apócrifos.** Las 250 personas, biografías, testimonios y fichas son ficticias y fueron generadas sintéticamente con el único propósito de probar el comportamiento de la plataforma (ingesta, ruteo, cotejo entre archivos, detección de regularidades). Ninguna persona real está representada, y **no se incluyen datos de menores de edad: todas las personas simuladas son adultas (19–82 años)**.

El corpus toma como espejo estructural un insumo real (carta de presentación de trayectoria de una traductora comunitaria) y multiplica esa forma en escenarios congruentes con los cuatro ecosistemas del proyecto y con las experiencias de campo documentadas (Escuela Miguel Hidalgo, taller INSP/dengue, ecosistema de discapacidades CDMX).

## Composición (250 recursos)

| Ecosistema | Recursos |
|---|---|
| Traducción, salud y justicia cognitiva (Morelos) | 70 |
| Dengue / ecosalud (Cuernavaca) | 60 |
| Escuela Miguel Hidalgo, Ciudad Chapultepec (zona de riesgo) | 60 |
| Discapacidades CDMX (PILARES) | 60 |

| Formato | Recursos | Tipo de archivo |
|---|---|---|
| Biografía de vida (transcripción oral, con muletillas y marcas de audio) | 66 | .txt |
| Carta de presentación de trayectoria | 61 | 40 .docx / 21 .txt |
| Testimonio | 59 | .txt |
| Ficha de participante (semiestructurada) | 38 | 10 .docx / 28 .txt |
| Notas personales de campo (diario) | 26 | .txt |

Longitudes: 75 cortas, 111 medias, 64 largas (85–564 palabras).

## Regularidades sembradas a propósito (*ground truth* para cotejo)

La plataforma debería poder **encontrar** estas regularidades sin que se le indiquen. Sirven para validar la detección:

1. **Lugares ancla compartidos entre archivos:** Centro de Salud de Tlayacapan, Hospital "José G. Parres" (Cuernavaca), Centro de Salud de Villa de Ayala, PILARES "Carlos Monsiváis" (Portales), PILARES "Gabriel Vargas" (Iztapalapa), Escuela Primaria "Miguel Hidalgo" (Ciudad Chapultepec), el mercado de Villa de Ayala, la barranca de Ciudad Chapultepec.
2. **Eventos compartidos:** la jornada de descacharrización de marzo de 2026; la feria escolar de prevención del dengue de noviembre de 2025; el Día Nacional de la Lengua de Señas Mexicana.
3. **Personas-ancla ficticias mencionadas por múltiples testimonios:** doña Eulalia (partera de Hueyapan), el delegado Reynaldo Ocampo, la maestra Imelda, Óscar (intérprete de LSM), Chabela (promotora de vectores).
4. **12 pares familiares:** personas que comparten apellido, lugar de origen y lengua, y que se mencionan mutuamente por nombre (columna `pariente` del manifiesto).
5. **16 cruces de ecosistema:** personas cuya narración conecta dos ecosistemas (p. ej., traductora que se suma a la descacharrización; madre de familia que menciona PILARES). Columna `cruce_ecosistema`.
6. **Temas transversales:** desconfianza institucional post-pandemia; el saber comunitario como conocimiento legítimo; la lengua como derecho y no como apoyo; la crítica a la palabra "inclusión"; la petición de que los datos "regresen" a la comunidad.
7. **Herramientas mencionadas:** App-Salud Aedes, ovitrampas, patio limpio.

## MANIFEST.csv

Metadatos por recurso: id, archivo, ecosistema, formato, longitud, número de palabras, nombre, edad, rol, lengua, origen, residencia, sitio ancla, cruce de ecosistema, pariente, y marca explícita de dato sintético. Útil como tabla de verdad para evaluar clasificación y agrupamiento.

## Reproducibilidad

Generado con `gen_corpus.py` (incluido), semilla fija `445`. Modificar la semilla o los pesos produce variantes del corpus.

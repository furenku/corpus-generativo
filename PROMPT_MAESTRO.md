# Prompt maestro — Corpus sintético para evaluación de RAG
**Proyecto IH-2025-I-445 · v1.0**

> Este documento es la especificación formal (el "prompt") que gobierna la
> generación del corpus. Reemplaza al prompt primitivo en prosa. Está escrito
> para ser ejecutado por una persona operadora, por `gen_corpus.py`, o por un
> agente LLM. Toda iteración del corpus debe partir de aquí y registrar qué
> palanca se movió (§9) y qué versión resultó.

---

## 1. Rol y misión

Actúas como **arquitecto de datos sintéticos para evaluación de sistemas RAG**.
Tu tarea es fabricar un acervo documental **deliberadamente apócrifo** que
imite, en forma y textura, los insumos reales que este proyecto recibiría de
campo, tomando como **único espejo con la realidad** un insumo auténtico
(§3). El corpus no describe a ninguna persona real: es un banco de pruebas.

## 2. Objetivo instrumental (qué se evalúa, y por qué existe el corpus)

El corpus **no es el fin**; es el instrumento. Su razón de ser es **medir la
calidad de las conversaciones que un sistema RAG sostiene sobre este acervo**,
comparando **modelos de distintos proveedores y tamaños** en tareas de:

- **Ingesta y chunking** — que documentos de formato y longitud heterogéneos se
  segmenten sin perder coherencia narrativa ni metadatos.
- **Recuperación (retrieval)** — que el sistema encuentre las *regularidades
  sembradas* (§7) sin que se le indiquen: lugares, eventos, personas y vínculos
  compartidos entre archivos.
- **Fidelidad y cotejo cruzado** — que las respuestas citen la evidencia correcta
  y detecten cuándo dos documentos hablan de la misma persona, lugar o hecho.
- **Robustez de registro** — que el modelo tolere oralidad, muletillas, marcas de
  audio (`[pausa]`, `[inaudible]`), fichas semiestructuradas y prosa formal.
- **Comportamiento ante lo ausente/ambiguo** — que no alucine parentescos, datos
  o vínculos que el corpus no contiene.

> Cada decisión de diseño del corpus debe justificarse contra una de estas
> capacidades evaluables. Si un rasgo no ayuda a discriminar modelos, sobra.

## 3. Insumo-espejo (la única ancla real)

`insumos/CARTA DE PRESENTACION TRAYECTORIA REYNA GONZALES MENTADO.docx`

Carta de presentación de trayectoria de una traductora comunitaria voluntaria
(mixteco↔español) en el sector salud y educativo de Morelos. De ella se hereda,
**no el contenido, sino la forma**:

- registro de primera persona, testimonial, con marca temporal y lugar;
- estructura carta formal ("A quien corresponda… Atentamente");
- oficio comunitario no titulado, saber situado, lengua como derecho;
- trayectoria vital contada por hitos de edad y por lugares concretos.

Todo el corpus es una **multiplicación especulativa** de esa forma hacia otros
ecosistemas y condiciones.

## 4. Invariantes éticos y de seguridad (NO negociables)

1. **100% sintético.** Ninguna persona, evento privado ni dato real (salvo la
   forma del insumo-espejo). Cada archivo y el manifiesto llevan marca explícita
   de dato apócrifo.
2. **Solo personas adultas** (rango 19–82). **Cero datos de menores**, ni como
   sujetos ni como titulares de datos. Los menores pueden aparecer como
   referencia narrativa genérica (p. ej. "las niñas y niños de la escuela"),
   nunca individualizados.
3. **Sin PII plausible-real.** No usar CURP, teléfonos, correos, direcciones
   exactas ni combinaciones que puedan colisionar con una persona real.
4. **Dignidad y verosimilitud, no caricatura.** Las condiciones (discapacidad,
   migración, lengua indígena, pobreza) se representan desde la experiencia
   situada, sin folclorismo ni tono inspiracional.
5. **Trazabilidad.** El corpus es reproducible (semilla fija) y auditable
   (manifiesto = tabla de verdad).

## 5. Universo de simulación (ecosistemas)

Cuatro ecosistemas, congruentes con las experiencias de campo del proyecto.
Cada persona simulada vive en exactamente uno (con posibles *cruces*, §7):

| Clave | Ecosistema | Escenario ancla |
|---|---|---|
| `traduccion` | Traducción, salud y justicia cognitiva (Morelos) | Centros de salud, hospital, trámites escolares; lenguas indígenas |
| `dengue` | Ecosalud / dengue (Cuernavaca, taller INSP) | Brigadas de vectores, ovitrampas, descacharrización |
| `escuela` | Escuela Primaria "Miguel Hidalgo" (colonia en zona de riesgo) | Comunidad escolar, barranca, prevención participativa |
| `discapacidad` | Ecosistema de discapacidad (CDMX, PILARES) | LSM, braille, accesibilidad, crítica a la "inclusión" |

## 6. Ejes de variación (para forzar heterogeneidad)

Cada recurso combina, de forma pseudoaleatoria y balanceada:

- **Persona:** nombre, género, **edad 19–82**, lengua/origen, rol, años de oficio.
- **Formato de archivo:** `biografia_oral` (transcripción con oralidad) ·
  `carta_presentacion` (espeja el insumo real) · `testimonio` ·
  `ficha_participante` (semiestructurada) · `notas_de_campo` (diario).
  → mezclar tipos de archivo: `.txt` y `.docx`.
- **Longitud:** `corta` / `media` / `larga` (≈ 85–560 palabras).
- **Registro:** oral (muletillas, marcas de audio) ↔ escrito formal.
- **Condición representada:** que a través de la variación se vean distintas
  condiciones de vida y de acceso (lengua, discapacidad, migración, género,
  edad, informalidad laboral).

**Objetivo cuantitativo por defecto: 250 recursos.** Distribución sugerida:
`traduccion` 70 · `dengue` 60 · `escuela` 60 · `discapacidad` 60.

## 7. Regularidades sembradas = *ground truth* (lo más importante para RAG)

Para poder **medir** retrieval y cotejo, el corpus siembra a propósito señales
que un buen sistema debe reencontrar sin ayuda. Documentar cada una en el
manifiesto:

1. **Lugares-ancla compartidos** entre múltiples archivos (centros de salud,
   hospital, PILARES, la escuela, el mercado, la barranca).
2. **Eventos compartidos** con fecha (jornada de descacharrización mar-2026;
   feria escolar del dengue nov-2025; Día Nacional de la LSM).
3. **Personas-ancla ficticias** citadas por varios testimonios (doña Eulalia,
   delegado Reynaldo Ocampo, maestra Imelda, Óscar intérprete de LSM, Chabela).
4. **Pares familiares** (~12): comparten apellido, origen y lengua, y se
   mencionan mutuamente por nombre → prueba de resolución de entidades.
5. **Cruces de ecosistema** (~16): una narración conecta dos ecosistemas →
   prueba de recuperación multi-hop.
6. **Temas transversales** recurrentes (desconfianza institucional post-pandemia;
   saber comunitario legítimo; lengua/seña como derecho; crítica a "inclusión";
   petición de que los datos "regresen" a la comunidad).
7. **Herramientas nombradas** (App-Salud Aedes, ovitrampas, patio limpio).

> Regla de oro: **toda regularidad sembrada debe quedar registrada en el
> manifiesto**, para que sea evaluable como pregunta con respuesta conocida (§11).

## 8. Especificación de salida

- `resultados/txt/` y `resultados/docx/` — un archivo por recurso.
- **Nomenclatura:** `SIM_{id:04d}_{ecosistema}_{formato}_{longitud}.{ext}`.
- **Encabezado/marca de síntesis** visible en cada archivo cuando el formato lo
  admita.
- `resultados/MANIFEST.csv` — **tabla de verdad**, una fila por recurso:
  `id, archivo, ecosistema, formato, longitud, palabras, nombre, edad, rol,
  lengua, origen, residencia, sitio_ancla, cruce_ecosistema, pariente,
  sintetico`. Ampliable con columnas de ground-truth adicionales (§11).
- `resultados/README.md` — naturaleza del corpus, composición y regularidades.
- `resultados/gen_corpus.py` — generador reproducible (semilla fija).

## 9. Palancas de iteración

Al iterar, **mover una palanca a la vez** y anotar versión + efecto:

| Palanca | Dónde | Efecto |
|---|---|---|
| Semilla (`445`) | `rng = random.Random(N)` | Variante completa reproducible |
| Conteo total / mezcla por ecosistema | `plan` en `make_personas` | Escala y balance |
| Pesos de formato | `elegir_formato` | + cartas vs. + transcripciones, etc. |
| Pesos de longitud | `elegir_largo` | Distribución de tamaños de chunk |
| Densidad de oralidad | `oraliza` (umbrales) | Dificultad de registro |
| # pares familiares / # cruces | `make_personas` | Dificultad de cotejo y multi-hop |
| Catálogos (anclas, roles, lenguas) | constantes top del script | Riqueza semántica |
| Fracción `.docx` vs `.txt` | export | Diversidad de ingesta |

## 10. Criterios de aceptación (checklist)

- [ ] N recursos generados; distribución por ecosistema/formato/longitud dentro de tolerancia.
- [ ] 0 sujetos menores de edad; todas las edades ∈ [19, 82].
- [ ] Cada archivo y cada fila del manifiesto marcados como sintéticos.
- [ ] Todas las regularidades de §7 presentes **y** registradas en el manifiesto.
- [ ] Sin PII plausible-real; sin duplicados textuales idénticos.
- [ ] Regenerable de cero desde `gen_corpus.py` con la semilla declarada.

## 11. Puente a la evaluación (cómo el corpus prueba a los modelos)

Del manifiesto se derivan **conjuntos de preguntas con respuesta conocida** para
comparar proveedores/tamaños de forma objetiva. Familias de consulta sugeridas:

- **Factual de un salto:** "¿Qué lengua habla y dónde atiende {persona}?" →
  respuesta en su ficha/manifiesto.
- **Cotejo de entidades:** "¿Quiénes de este acervo son familiares entre sí?" →
  columna `pariente`.
- **Multi-hop / cruce:** "¿Qué personas de traducción participaron también en la
  jornada de descacharrización?" → columna `cruce_ecosistema`.
- **Agregación por ancla:** "¿Cuántos testimonios mencionan el PILARES Carlos
  Monsiváis?" → `sitio_ancla`.
- **Negativa/anti-alucinación:** preguntas cuya respuesta el corpus **no**
  contiene → el modelo debe abstenerse.

Métricas objetivo: recall@k y precisión de recuperación contra el ground-truth,
fidelidad de cita, tasa de alucinación, y consistencia entre proveedores a igual
prompt. **Reportar por modelo, por tamaño y por familia de pregunta.**

---
*Fin del prompt maestro v1.0. Cambios sustantivos ⇒ subir versión y anotar en el commit.*

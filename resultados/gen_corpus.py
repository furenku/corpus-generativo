# -*- coding: utf-8 -*-
"""
Generador de corpus sintético (deliberadamente apócrifo) para pruebas de la
plataforma del proyecto IH-2025-I-445. Todas las personas, biografías y
testimonios son ficticios. Solo adultos (18+). Semilla fija: reproducible.
"""
import random, csv, os, re

rng = random.Random(445)

OUT = "/home/claude/corpus"

# ---------------------------------------------------------------- anclas
# Regularidades sembradas a propósito (ground truth para cotejo)
ANCLAS = {
    "cs_tlayacapan": "Centro de Salud de Tlayacapan",
    "hosp_parres": 'Hospital General de Cuernavaca "José G. Parres"',
    "cs_ayala": "Centro de Salud de Villa de Ayala",
    "pilares_monsivais": 'PILARES "Carlos Monsiváis" de la colonia Portales',
    "pilares_vargas": 'PILARES "Gabriel Vargas" de Iztapalapa',
    "escuela_hidalgo": 'Escuela Primaria "Miguel Hidalgo" de la colonia Ciudad Chapultepec',
    "barranca": "la barranca que corre detrás de la colonia Ciudad Chapultepec",
    "jornada_marzo": "la jornada de descacharrización de marzo de 2026",
    "feria_dengue": "la feria escolar de prevención del dengue de noviembre de 2025",
    "dia_lsm": "el Día Nacional de la Lengua de Señas Mexicana",
    "app_aedes": "la aplicación App-Salud Aedes",
    "dona_eulalia": "doña Eulalia, la partera de Hueyapan",
    "delegado_reynaldo": "el delegado Reynaldo Ocampo",
    "maestra_imelda": "la maestra Imelda",
    "interprete_oscar": "Óscar, el intérprete de LSM",
    "promotora_chabela": "Chabela, la promotora de vectores",
    "mercado_ayala": "el mercado de Villa de Ayala",
}

NOMBRES_F = ["Reyna","Angélica","Guadalupe","Rosalba","Herminia","Catalina","Yolanda","Marisol","Petra","Antonia","Silvia","Beatriz","Norma","Irene","Leticia","Verónica","Ofelia","Camila","Zenaida","Fidelia","Aurelia","Micaela","Juana","Estela","Rufina","Delfina","Xóchitl","Itzel","Nayeli","Citlali","Erandi","Yaretzi","Lucía","Margarita","Elvira","Socorro","Amalia","Cristina","Sandra","Gabriela","Patricia","Rocío del Carmen","Enedina","Hortensia","Bertha","Elodia"]
NOMBRES_M = ["Marcelino","Aurelio","Fidencio","Bonifacio","Ernesto","Raymundo","Gregorio","Isidro","Melitón","Eusebio","Refugio","Crisóforo","Tomás","Pablo","Andrés","Camilo","Efrén","Leobardo","Nicolás","Ismael","Rogelio","Vicente","Faustino","Herminio","Cuauhtémoc","Tonatiuh","Emiliano","Abundio","Genaro","Sabino","Anselmo","Froylán","Epifanio","Jacinto","Silvestre","Maximino","Arnulfo","Celerino","Domingo","Octavio"]
APELLIDOS = ["González Mentado","Flores Cantú","Mendoza Salgado","Ortiz de la Cruz","Ramírez Xochihua","Bautista Flores","Santiago Cruz","López Tecpanécatl","Hernández Popoca","Castañeda Ruiz","Villanueva Ocampo","Ayala Benítez","Cuevas Morales","Delgado Ríos","Espinosa Zamudio","Franco Torres","Galindo Peña","Ibarra Solís","Juárez Cano","Lara Medina","Meza Cárdenas","Nava Rendón","Olvera Ponce","Peralta Guzmán","Quintero Alba","Rosales Vega","Sedano Trujillo","Tapia Onofre","Uribe Camacho","Vázquez de Jesús","Zepeda Marín","Alarcón Bravo","Barrios Coronel","Cortés Amaro","Domínguez Petlacalco","Estrada Reyna","Figueroa Anaya","Gaspar Melchor","Huerta Escamilla","Islas Bermúdez","Jiménez Toledano","Luna Carrasco","Martínez Yopihua","Noriega Palma","Osorio Bello","Pineda Cuenca","Reyes Tlacomulco","Salazar Prieto","Téllez Aranda","Valdés Colín"]

LENGUAS = [("mixteco","Potoichán, Guerrero"),("mixteco","San Juan Mixtepec, Oaxaca"),("náhuatl","Hueyapan, Morelos"),("náhuatl","Cuentepec, Morelos"),("náhuatl","Xoxocotla, Morelos"),("tlapaneco (me'phaa)","Malinaltepec, Guerrero"),("amuzgo","Xochistlahuaca, Guerrero"),("tsotsil","Chenalhó, Chiapas"),("hñähñu (otomí)","Ixmiquilpan, Hidalgo"),("mazateco","Huautla de Jiménez, Oaxaca"),("zapoteco","Juchitán, Oaxaca"),("totonaco","Papantla, Veracruz"),("mixe","Tlahuitoltepec, Oaxaca"),("tlahuica","San Juan Atzingo, Estado de México")]

RESIDENCIAS_MOR = ["Tepoztlán, Morelos","Tlayacapan, Morelos","Villa de Ayala, Morelos","Cuautla, Morelos","Yautepec, Morelos","Temixco, Morelos","Cuernavaca, Morelos","Jiutepec, Morelos"]
COLONIAS_CVA = ["Ciudad Chapultepec","Antonio Barona","Lagunilla","Patios de la Estación","Satélite","Ampliación Lázaro Cárdenas","La Carolina","Flores Magón"]
COLONIAS_CDMX = ["Portales","Narvarte","Santa Cruz Meyehualco","San Miguel Teotongo","Doctores","Obrera","Pedregal de Santo Domingo","Agrícola Oriental"]

ROLES = {
 "traduccion": [("traductora comunitaria","f"),("traductor comunitario","m"),("intérprete en salud","x"),("partera tradicional","f"),("promotora de salud comunitaria","f"),("acompañante de trámites","x"),("gestora comunitaria","f"),("médico pasante en zona rural","x"),("enfermera de centro de salud","f"),("trabajadora social","f")],
 "dengue": [("brigadista de vectores","x"),("promotora de salud","f"),("técnico entomológico","m"),("líder vecinal","x"),("comerciante del mercado","x"),("ayudante municipal","x"),("verificadora de ovitrampas","f"),("chofer de la unidad de nebulización","m"),("enfermera de campo","f"),("delegada de colonia","f")],
 "escuela": [("maestra de primaria","f"),("maestro de primaria","m"),("madre de familia","f"),("padre de familia","m"),("conserje de la escuela","x"),("directora","f"),("brigadista de protección civil","x"),("vendedora de la cooperativa escolar","f"),("psicóloga educativa","f"),("supervisor de zona escolar","m")],
 "discapacidad": [("persona sorda, tallerista de LSM","x"),("intérprete de LSM","x"),("activista con discapacidad motriz","x"),("persona ciega, instructora de braille","x"),("mediadora educativa de PILARES","f"),("madre de una persona sorda adulta","f"),("usuario de silla de ruedas, promotor cultural","m"),("persona con discapacidad psicosocial, colaboradora de colectivo","f"),("tallerista de danza inclusiva","x"),("funcionaria de área de diversidad funcional","f")],
}

def make_personas():
    personas = []
    plan = [("traduccion",70),("dengue",60),("escuela",60),("discapacidad",60)]
    pid = 0
    for eco, n in plan:
        for _ in range(n):
            pid += 1
            genero = rng.choice(["f","m"])
            nombre = rng.choice(NOMBRES_F if genero=="f" else NOMBRES_M)
            apellido = rng.choice(APELLIDOS)
            edad = rng.randint(19, 82)
            rol, rg = rng.choice(ROLES[eco])
            # ajustar rol a género cuando el rol es marcado
            if rg != "x" and rg != genero:
                rol_alt = [r for r,g in ROLES[eco] if g in (genero,"x")]
                rol = rng.choice(rol_alt)
            lengua, origen = rng.choice(LENGUAS)
            if "pasante" in rol:
                edad = rng.randint(23, 31)
            anios = max(1, min(edad-16, rng.randint(2, 38)))
            p = dict(id=pid, eco=eco, genero=genero, nombre=nombre, apellido=apellido,
                     edad=edad, rol=rol, lengua=lengua, origen=origen, anios=anios)
            if eco=="traduccion":
                p["residencia"] = rng.choice(RESIDENCIAS_MOR)
                p["sitio"] = "el " + rng.choice([ANCLAS["cs_tlayacapan"], ANCLAS["hosp_parres"], ANCLAS["cs_ayala"], ANCLAS["cs_tlayacapan"]])
            elif eco=="dengue":
                p["residencia"] = "Cuernavaca, Morelos"
                p["colonia"] = rng.choice(COLONIAS_CVA)
                p["sitio"] = ANCLAS["jornada_marzo"] if rng.random()<0.5 else ANCLAS["app_aedes"]
            elif eco=="escuela":
                p["residencia"] = "Cuernavaca, Morelos"
                p["colonia"] = "Ciudad Chapultepec" if rng.random()<0.7 else rng.choice(COLONIAS_CVA)
                p["sitio"] = ANCLAS["escuela_hidalgo"]
            else:
                p["residencia"] = "Ciudad de México"
                p["colonia"] = rng.choice(COLONIAS_CDMX)
                p["sitio"] = ANCLAS["pilares_monsivais"] if rng.random()<0.65 else ANCLAS["pilares_vargas"]
            personas.append(p)
    # clusters familiares: 12 pares comparten apellido/origen y se mencionan
    idx = list(range(len(personas))); rng.shuffle(idx)
    fam = []
    for k in range(12):
        a, b = personas[idx[2*k]], personas[idx[2*k+1]]
        b["apellido"] = a["apellido"]; b["origen"] = a["origen"]; b["lengua"] = a["lengua"]
        a["pariente"] = b["nombre"]; b["pariente"] = a["nombre"]
        a["parentesco"] = "hermana" if b["genero"]=="f" else "hermano"
        b["parentesco"] = "hermana" if a["genero"]=="f" else "hermano"
        fam.append((a["id"], b["id"]))
    # cruces de ecosistema (~16 personas mencionan otro ecosistema)
    cruz = rng.sample(personas, 16)
    for p in cruz:
        p["cruce"] = True
    return personas, fam

# ---------------------------------------------------------------- fragmentos
def G(p, f, m):  # concordancia de género
    return f if p["genero"]=="f" else m

def frag_origen(p):
    v = [
        "Nací en {origen}, en una familia donde el {lengua} era la lengua de la casa, del campo y de los rezos.",
        "Soy de {origen}. Crecí hablando {lengua}; el español lo fui aprendiendo después, en la escuela y en los mandados.",
        "Mi pueblo es {origen}. Ahí aprendí de mis abuelos el {lengua} y también aprendí a escuchar antes de hablar.",
        "Vengo de {origen}. En mi casa se hablaba puro {lengua}; el español llegó cuando salimos a trabajar fuera.",
        "Soy {originaria} de {origen}. Tengo {edad} años y desde hace tiempo vivo en {residencia}.",
        "Nací hace {edad} años en {origen}. Mi madre me enseñó el {lengua} y también me enseñó que la palabra se cuida como se cuida la milpa.",
    ]
    t = rng.choice(v)
    return t.format(originaria=G(p,"originaria","originario"), **p)

def frag_migracion(p):
    v = [
        "Cuando era {joven} salimos de {origen} porque el trabajo no alcanzaba. Llegamos a {residencia} sin conocer a nadie, y lo primero que entendí es que aquí mi lengua no valía lo mismo que allá.",
        "Nos venimos a {residencia} hace muchos años. Al principio yo hacía de todo: el campo, la obra, la cocina. Pero siempre me buscaban los paisanos para que les ayudara a explicarse en español.",
        "Migré a {residencia} siguiendo a mi familia. Allá quedó la casa de adobe; acá empezó otra vida, con otros papeles, otras filas, otras ventanillas.",
        "Salí de mi pueblo a los {edadsalida} años. En {residencia} aprendí que hay puertas que se abren con el español y puertas que solo se abren con la confianza.",
    ]
    return rng.choice(v).format(joven=G(p,"joven","joven"), edadsalida=rng.randint(12,26), **p)

# --- ecosistema traducción / salud / justicia cognitiva
def frag_trad_inicio(p):
    v = [
        "Empecé a acompañar a la gente casi sin darme cuenta: una vecina embarazada que no entendía lo que le decía el doctor, y yo en medio, pasando las palabras de un lado a otro. De eso hace ya {anios} años.",
        "Mi primer acompañamiento fue con mi tía, en una consulta donde el médico hablaba rápido y ella solo asentía por respeto. Ahí entendí que asentir no es entender. Desde entonces no he dejado de hacerlo.",
        "Hace {anios} años que hago traducción del {lengua} al español en los servicios de salud. Nadie me nombró para esto; me fue nombrando la necesidad de la gente.",
        "Comencé ayudando en los trámites de la escuela, cuando las mamás que hablan {lengua} no podían inscribir a sus hijos. Después vinieron las consultas médicas, las farmacias, el registro civil.",
        "Todo empezó con {dona_eulalia}. Ella atendía a las embarazadas de la región y me pedía que la acompañara a las citas de control, porque muchas señoras hablaban {lengua} y en la clínica nadie las entendía.",
    ]
    return rng.choice(v).format(dona_eulalia=ANCLAS["dona_eulalia"], **p)

def frag_trad_practica(p):
    v = [
        "Actualmente colaboro en {sitio}, donde apoyo en consultas, en enfermería, en la farmacia y en cualquier situación donde haga falta que las palabras crucen de una lengua a otra sin perder su peso.",
        "Mi trabajo no es solo cambiar palabras: es explicar qué significa un diagnóstico, qué se puede preguntar, qué derechos se tienen. En {sitio} me conocen y me llaman cuando llega un paciente que habla {lengua}.",
        "Acompaño sobre todo a mujeres embarazadas y a personas mayores. En {sitio} he aprendido que la desconfianza no es ignorancia: es memoria de malos tratos.",
        "Traduzco en {sitio} de manera voluntaria. He acompañado partos, urgencias, vacunaciones y también malas noticias, que son las más difíciles de traducir porque duelen en las dos lenguas.",
        "Además de la clínica, ayudo en la inscripción de niñas y niños en las escuelas públicas de la zona de Villa de Ayala; muchas familias me conocen por {mercado}, y de puesto en puesto se corre la voz de que ahí ando yo para servir de puente con las instituciones.",
    ]
    return rng.choice(v).format(mercado=ANCLAS["mercado_ayala"], **p)

def frag_trad_escena(p):
    v = [
        "Recuerdo a una señora a la que le dijeron 'ayuno' y ella entendió que ya no debía comer nunca antes de las medicinas. Estuvo tres días casi sin probar alimento. Cuando lo platicamos en {lengua}, lloró de alivio. Eso es lo que pasa cuando no hay traducción: no es un malentendido, es un riesgo.",
        "Una vez, en {sitio}, el doctor dijo 'es necesario referirla'. La paciente entendió que la estaban regañando. Tuve que explicarle que 'referir' era mandarla con otro médico. Son palabras chiquitas que cargan mucho miedo.",
        "Hubo un caso que no olvido: un señor con diabetes que decía a todo que sí. Cuando le pregunté en {lengua} qué había entendido, me dijo: 'que estoy mal de la sangre y que es mi culpa'. Nadie le había dicho eso, pero eso fue lo que le llegó.",
        "A veces los papeles piden firmar un consentimiento informado. Yo pregunto: ¿consentimiento de qué, informado en qué lengua? Mi trabajo empieza justo en esa pregunta.",
        "Me ha tocado traducir en la madrugada, por teléfono, cuando una comadre llega a urgencias del {hosp} y nadie le entiende. La voz también acompaña, aunque el cuerpo esté lejos.",
    ]
    return rng.choice(v).format(hosp=ANCLAS["hosp_parres"], **p)

def frag_trad_cierre(p):
    v = [
        "Para mí es un orgullo poder contribuir con mi lengua, mis raíces y mi tiempo para que mi gente ejerza su derecho a la salud sin barreras. No pido reconocimiento; pido que un día este trabajo no haga falta porque las instituciones hablen también nuestras lenguas.",
        "Sigo haciendo esto de manera voluntaria porque creo que nadie debería enfermarse dos veces: una del cuerpo y otra de no ser {entendida}.",
        "Lo que yo sé no está en un título, está en {anios} años de salas de espera. Si este proyecto sirve para que ese saber cuente, aquí está mi historia.",
        "Sueño con que haya intérpretes reconocidas y pagadas en cada clínica. Mientras eso llega, aquí seguimos, las de siempre, poniendo el cuerpo y la palabra.",
    ]
    return rng.choice(v).format(entendida=G(p,"entendida","entendido"), **p)

# --- ecosistema dengue
def frag_den_inicio(p):
    v = [
        "Llevo {anios} años trabajando en el control del dengue en Cuernavaca, primero como {rol} y siempre a pie, casa por casa, patio por patio.",
        "Entré a esto de los mosquitos casi por accidente, cubriendo a un compañero, y me quedé {anios} años. Uno aprende a leer los patios como otros leen periódicos.",
        "Soy {rol} en la colonia {colonia}. Mi trabajo empieza donde empieza el agua estancada: una cubeta, una llanta, un florero del panteón.",
        "Después de la pandemia todo cambió: la gente ya no abre la puerta igual, ya no cree igual. Yo lo vi con mis propios ojos, porque llevo {anios} años tocando esas mismas puertas.",
    ]
    return rng.choice(v).format(**p)

def frag_den_practica(p):
    v = [
        "Participé en {jornada} en la colonia {colonia}. Sacamos camiones enteros de cacharros, pero lo más importante no fueron los fierros: fueron las pláticas en las banquetas, donde la gente cuenta por qué guarda el agua, por qué desconfía, por qué está cansada.",
        "Ahora registramos las ovitrampas con {app}. A mí al principio me costó el teléfono, no le voy a mentir, pero entendí que si el dato no se sube, es como si el trabajo no existiera para los de arriba.",
        "Trabajo de la mano con {chabela}; ella conoce a las señoras de la colonia y sin ella no se abre ni la mitad de las puertas. El mapa de los criaderos también es un mapa de confianzas.",
        "Coordino con {delegado} las visitas por manzana. Él dice que el problema no es el mosquito sino el agua que no llega, y algo de razón tiene: donde no hay agua entubada, la gente almacena, y donde se almacena, el mosquito pone.",
        "En el mercado la cosa es distinta: los comerciantes no pueden dejar el puesto para ir a pláticas. Entonces la plática va al puesto. Cinco minutos, un volante, una revisada a las cubetas, y a la siguiente.",
    ]
    return rng.choice(v).format(jornada=ANCLAS["jornada_marzo"], app=ANCLAS["app_aedes"], chabela=ANCLAS["promotora_chabela"], delegado=ANCLAS["delegado_reynaldo"], **p)

def frag_den_escena(p):
    v = [
        "Una señora me dijo: 'ustedes vienen cuando hay brote y luego desaparecen'. No supe qué contestarle porque es verdad. Eso también es un dato, aunque no quepa en el formato.",
        "En {feria} me tocó ver a los niños explicándoles el ciclo del mosquito a sus papás. Ahí pensé: la información sí está llegando, lo que no está llegando es la confianza entre nosotros los adultos.",
        "Los casos asintomáticos son la mayoría, eso nos explicaron los epidemiólogos. O sea que el vecino que se siente bien también puede estar moviendo el virus. Explicar eso sin asustar es un arte que nadie nos enseñó.",
        "Hubo una casa donde encontramos veintitrés criaderos. No era descuido: era una familia que junta agua porque la pipa pasa cada quince días. El criadero era la punta; abajo estaba la desigualdad.",
        "Después del huracán se llenó todo de recipientes y la gente tenía otras urgencias. Pedirles que pensaran en mosquitos parecía una burla. Aprendí que la prevención tiene calendario, y el calendario lo pone la vida de la gente, no la campaña.",
    ]
    return rng.choice(v).format(feria=ANCLAS["feria_dengue"], **p)

def frag_den_cierre(p):
    v = [
        "Si algo he aprendido en {anios} años es que el patio limpio funciona cuando hay relación, no cuando hay regaño. La campaña que no escucha, no fumiga nada.",
        "Yo lo que quiero es que lo que vemos en campo llegue arriba sin que se le caiga la mitad en el camino. Que el relato del brigadista valga como dato, porque lo es.",
        "Seguimos porque la colonia es nuestra. Aquí viven mis hijos, aquí se enferma mi gente. Eso no lo paga la quincena.",
        "Le entro a esto de la plataforma si sirve para que no se pierda lo que sabemos los de a pie. Que quede escrito, aunque sea con mis palabras rancheras.",
    ]
    return rng.choice(v).format(**p)

# --- ecosistema escuela
def frag_esc_inicio(p):
    v = [
        "Trabajo desde hace {anios} años en la {escuela}. Conozco a las familias, conozco {barranca}, y conozco lo que significa dar clases en una zona que los mapas llaman 'de riesgo'.",
        "Soy {rol} y mi vida gira alrededor de la {escuela}: ahí estudiaron mis hijos, ahí participo en las faenas, ahí me toca opinar aunque a veces nadie pregunte.",
        "Llegué a la colonia hace {anios} años, cuando todavía no estaba tan poblada la parte de abajo, la que da a {barranca}. La escuela fue lo primero que nos organizó como vecinos.",
        "Soy {rol}. Me tocó la época en que la colonia creció hacia donde no debía: hacia la barranca. La escuela quedó en medio, entre el riesgo de allá abajo y el descuido de allá arriba.",
    ]
    return rng.choice(v).format(escuela=ANCLAS["escuela_hidalgo"], barranca=ANCLAS["barranca"], **p)

def frag_esc_practica(p):
    v = [
        "Cuando organizamos {feria}, los grupos prepararon maquetas del ciclo del mosquito, carteles y hasta obritas de teatro. Los adultos íbamos de visitantes y salíamos de alumnos. Eso me hizo pensar quién enseña a quién en realidad.",
        "Con {imelda} armamos un comité de madres y padres para revisar los tinacos y los bebederos de la escuela cada viernes. Suena poca cosa, pero es la primera vez que la revisión no depende de que venga alguien de fuera.",
        "En temporada de lluvias vivimos con el pendiente de la barranca: la escuela está cerca y hay familias que viven todavía más cerca. Protección civil viene, mide, apunta, y nosotros nos quedamos con las mismas preguntas.",
        "Los de la brigada de vectores vinieron a capacitarnos. Lo bueno fue que esta vez no fue solo plática: caminamos juntos la colonia, señalando criaderos, y los vecinos salían a preguntar. La escuela sirvió de excusa para hablarnos entre nosotros.",
        "Yo atiendo la cooperativa y desde ahí se ve todo: quién falta, quién llega sin desayunar, qué familia anda en apuros. La cooperativa es el consultorio sin bata de la escuela.",
    ]
    return rng.choice(v).format(feria=ANCLAS["feria_dengue"], imelda=ANCLAS["maestra_imelda"], **p)

def frag_esc_escena(p):
    v = [
        "En la feria, un alumno le explicó a su abuelo cómo el agua del florero cría larvas. El señor, que ha vivido setenta años junto a la barranca, le contestó con lo que él sabe del agua, de las crecidas, de los años buenos y malos. Ahí había dos saberes platicando de igual a igual. Eso no lo he visto en ningún curso.",
        "Después de una lluvia fuerte se cerró el paso de abajo y varios niños no llegaron. Las mamás organizamos una cadena de avisos por teléfono, casa por casa. Nadie nos lo pidió; salió de la pura necesidad. Ahora esa cadena sirve para todo: avisos de la escuela, de salud, de seguridad.",
        "Un ingeniero vino a decirnos que la ladera 'presenta inestabilidad'. Una vecina le contestó: 'eso mi suegra lo dice desde hace treinta años, nomás que ella lo dice en cristiano'. Todos nos reímos, pero la frase se me quedó: el conocimiento ya estaba aquí, lo que faltaba era que lo tomaran en serio.",
        "Me tocó traducirle a una mamá que habla {lengua} durante la junta de inscripciones. La dirección no tenía manera de atenderla y yo apenas la ayudé con lo que pude. Pensé en cuántas familias se quedan fuera no por falta de interés sino por falta de lengua.",
        "Cuando vino la universidad a 'levantar datos', una maestra pidió que también nos dejaran los resultados, porque siempre se los llevan y no regresan. Esta vez quedó por escrito. Ya veremos.",
    ]
    return rng.choice(v).format(**p)

def frag_esc_cierre(p):
    v = [
        "La escuela es el corazón de la colonia. Si el proyecto quiere entender cómo circula el conocimiento aquí, que empiece por el patio a la hora del recreo y por la puerta a la hora de la salida.",
        "No queremos ser 'población beneficiaria'. Queremos ser parte de los que piensan el problema, porque el problema lo vivimos nosotros con dirección y código postal.",
        "Yo firmo donde haga falta, pero pido una cosa: que lo que contemos regrese. Que no se vuelva un archivo dormido en una oficina.",
        "Sigo aquí porque creo en esta escuela. Con goteras, con barranca y con todo, es el lugar donde esta colonia se piensa a sí misma.",
    ]
    return rng.choice(v).format(**p)

# --- ecosistema discapacidad
def frag_dis_inicio(p):
    v = [
        "Soy {rol}. Tengo {edad} años y buena parte de mi vida ha transcurrido explicando lo que no debería necesitar explicación: que mi forma de estar en el mundo no es un déficit.",
        "Participo desde hace {anios} años en actividades del {sitio}. Llegué buscando un taller y encontré una comunidad.",
        "Soy {rol}. Aprendí más en los pasillos del {sitio} que en muchas oficinas dedicadas, en teoría, a personas como yo.",
        "Mi historia con la discapacidad no empezó conmigo: empezó con las escaleras, con las ventanillas, con los formatos que no contemplan mi existencia. Yo estaba bien; el entorno era el problema.",
    ]
    return rng.choice(v).format(**p)

def frag_dis_lsm(p):
    rol = p["rol"]
    v = []
    if "sorda" in rol and "madre" not in rol:
        v += [G(p, "Soy sorda de nacimiento", "Soy sordo de nacimiento") + " y la Lengua de Señas Mexicana es mi lengua, no mi terapia. Crecí en una escuela oralista donde me sentaban adelante 'para que leyera los labios', como si mirar fijamente fuera lo mismo que entender.",
              "Aprendí LSM ya de {adulta}, y fue como si me devolvieran algo que siempre fue mío. Ahora doy taller en el {sitio} y veo llegar a personas oyentes, a familias, a vecinas curiosas. La lengua convoca."]
    if "intérprete" in rol:
        v += ["Trabajo como intérprete de LSM. Mi lugar es un lugar raro: soy puente, pero el puente no decide a dónde van los que cruzan. He aprendido a interpretar sin robar la voz, o mejor dicho, sin robar las manos."]
    v += ["En {dia} participé en el conversatorio del {pilares}. No se hablaba 'sobre' las personas sordas: eran las personas sordas quienes tomaban la palabra pública, señando. Los oyentes, por una vez, eran quienes necesitaban intérprete."]
    return rng.choice(v).format(dia=ANCLAS["dia_lsm"], pilares=ANCLAS["pilares_monsivais"], adulta=G(p,"adulta","adulto"), **p)

def frag_dis_practica(p):
    rol = p["rol"]
    v = ["Doy seguimiento a las actividades del {sitio}. Al principio la institución quería llamar a todo 'inclusión'. Varios propusimos otras palabras, porque la inclusión siempre supone que hay un adentro que nos hace el favor de recibirnos."]
    if "tallerista" in rol or "instructora" in rol or "mediadora" in rol:
        v += ["Doy un taller en el {sitio}. El primer día siempre pregunto lo mismo: ¿quién decidió que esto era 'para personas con discapacidad' y no, simplemente, para personas? De esa pregunta sale todo el programa del curso.",
              "Mi taller en el {sitio} empezó con cuatro asistentes y ahora no cabemos. No fue publicidad: fue que la gente corrió la voz de que aquí nadie te corrige el cuerpo."]
    if "intérprete" in rol or "sorda" in rol:
        v += ["Colaboro con {oscar} en las actividades del {sitio}. Entre los dos hemos ido armando un glosario de señas para términos de salud, porque en el hospital la falta de intérprete puede costar un diagnóstico."]
    if "silla" in rol or "motriz" in rol:
        v += ["Me muevo en silla de ruedas por una ciudad que se dice accesible en los folletos. Levanto registro de cada rampa rota, de cada elevador 'temporalmente fuera de servicio' que lleva años así. Mi cuaderno es un censo de promesas."]
    if "psicosocial" in rol:
        v += ["Acompaño a otras personas con discapacidad psicosocial en sus trámites. Lo más duro no son los papeles: es el tono con que te hablan cuando decides decir tu diagnóstico en voz alta."]
    if "ciega" in rol:
        v += ["Enseño braille y uso de lector de pantalla en el {sitio}. La mitad de mis alumnas son personas mayores que perdieron la vista de grandes; la otra mitad, familiares que por fin entendieron que aprender es más útil que compadecer."]
    if "madre" in rol:
        v += ["Mi hijo es sordo y ya es un adulto. Yo aprendí LSM a los cincuenta años, en el {sitio}, junto a otras madres. Ahora interpreto en las juntas vecinales para que él participe como cualquier vecino, porque lo es."]
    if "funcionaria" in rol:
        v += ["Trabajo del lado institucional, y lo digo sin orgullo automático: he visto cómo un formato mal diseñado puede deshacer en cinco minutos lo que un taller construyó en meses. Mi labor cotidiana es pelear esos formatos por dentro."]
    if "promotor" in rol or "activista" in rol:
        v += ["Organizo recorridos por la colonia {colonia} para levantar un mapa de accesibilidad hecho por nosotros mismos: banquetas, transporte, mercados. El mapa oficial dice una cosa; nuestros cuerpos dicen otra."]
    return rng.choice(v).format(oscar=ANCLAS["interprete_oscar"], **p)

def frag_dis_escena(p):
    v = [
        "En un evento oficial pusieron el templete con escalones y sin rampa. El discurso era sobre accesibilidad. Nadie pareció notar la ironía, salvo nosotros, que la notamos siempre porque la vivimos siempre.",
        "Una tallerista dijo algo que me quedó grabado: 'no queremos ser incluidos en su mundo; queremos que el mundo se rehaga con nosotros adentro desde el principio'. Ahí está toda la discusión, me parece.",
        "En el conversatorio del {pilares}, una persona sorda mayor contó que pasó décadas sin lengua, señando a escondidas. Cuando terminó, el silencio del público no fue vacío: fue respeto. Hay silencios que dicen más que los aplausos.",
        "Me pidieron dar una plática 'motivacional'. Contesté que mi vida no es material de inspiración para terceros, pero que con gusto hablaba de rampas, presupuestos e intérpretes. No me volvieron a llamar. Lo cuento sin amargura: también así se dibuja el mapa.",
        "Cuando cerramos la sesión, una compañera dijo que esto se trata de abrir el corazón, poco a poco. Suena sencillo, pero nombra algo que ningún reglamento nombra.",
    ]
    return rng.choice(v).format(pilares=ANCLAS["pilares_monsivais"], **p)

def frag_dis_cierre(p):
    v = [
        "No pido sensibilidad; pido presupuesto, intérpretes y diseño desde el origen. La ternura que no cambia estructuras es decoración.",
        "Sigo participando porque el {sitio} es de los pocos lugares donde mi palabra —hablada, señada o escrita— llega entera.",
        "Si esta plataforma va a guardar nuestras historias, que las guarde con nuestras palabras y nuestros términos. La voz antes que la resonancia.",
        "Lo que sabemos las personas con discapacidad sobre esta ciudad no está en ningún diagnóstico oficial. Está en nuestros cuerpos y en nuestros trayectos. Ojalá este archivo sepa escucharlo.",
    ]
    return rng.choice(v).format(**p)

FRAGS = {
 "traduccion": [frag_trad_inicio, frag_trad_practica, frag_trad_escena, frag_trad_cierre],
 "dengue": [frag_den_inicio, frag_den_practica, frag_den_escena, frag_den_cierre],
 "escuela": [frag_esc_inicio, frag_esc_practica, frag_esc_escena, frag_esc_cierre],
 "discapacidad": [frag_dis_inicio, frag_dis_practica, frag_dis_escena, frag_dis_cierre],
}

def frag_cruce(p):
    v = [
        "Además de esto, hace poco me sumé como {voluntaria} a {jornada}, porque el dengue también se ceba con los que menos tienen y ahí hacía falta gente que hablara {lengua}.",
        "También he colaborado con la {escuela}, apoyando en {feria}; los problemas no vienen separados y nosotros tampoco deberíamos trabajar separados.",
        "Hace poco me invitaron a un conversatorio en el {pilares}; descubrí que lo que ellos dicen de la lengua de señas es lo mismo que nosotros decimos de nuestras lenguas: no es un apoyo, es un derecho.",
        "Cuando el centro de salud organizó pláticas de dengue, me pidieron traducirlas al {lengua}. Fue la primera vez que una campaña de salud habló mi idioma, literalmente.",
    ]
    t = rng.choice(v)
    return t.format(jornada=ANCLAS["jornada_marzo"], escuela=ANCLAS["escuela_hidalgo"],
                    feria=ANCLAS["feria_dengue"], pilares=ANCLAS["pilares_monsivais"],
                    voluntaria=G(p,"voluntaria","voluntario"), **p)

def frag_pariente(p):
    return ("Parte de este camino lo he hecho junto a mi {parentesco} {pariente}, que también participa en estas "
            "actividades; entre la familia nos vamos pasando el oficio y la terquedad.").format(**p)

# ---------------------------------------------------------------- formatos
MULETILLAS = ["pues", "este...", "o sea", "digamos", "cómo le diré", "fíjese que", "la verdad"]
MARCAS = ["[pausa]", "[risas]", "[inaudible]", "[se escucha ruido de calle]", "[suspira]"]

def oraliza(texto):
    """Convierte prosa escrita en registro oral de transcripción."""
    crudo = texto.replace("\n", " ")
    oraciones = [o.strip() for o in re.split(r"(?<=[.!?]) +", crudo) if o.strip()]
    out = []
    for o in oraciones:
        o = o.rstrip(".")
        r = rng.random()
        if r < 0.28 and o:
            o = rng.choice(MULETILLAS).capitalize() + ", " + o[0].lower() + o[1:]
        if rng.random() < 0.16 and not o.endswith(("?", "!", "'")):
            o += ", ¿no?"
        o += "." if not o.endswith(("?", "!")) else ""
        if rng.random() < 0.10:
            o += " " + rng.choice(MARCAS)
        out.append(o)
    return " ".join(out)

MESES = ["enero","febrero","marzo","abril","mayo","junio"]
def fecha_2026():
    return f"{rng.randint(2,27)} de {rng.choice(MESES)} de 2026"

def cuerpo(p, n_frags):
    """Ensambla n fragmentos narrativos coherentes para la persona."""
    inicio, practica, escena, cierre = FRAGS[p["eco"]]
    partes = [frag_origen(p)]
    if rng.random() < 0.55:
        partes.append(frag_migracion(p))
    partes.append(inicio(p))
    extras = []
    while len(partes) + len(extras) < n_frags - 1:
        extras.append(rng.choice([practica, escena])(p))
    partes += extras
    if p.get("pariente") and rng.random() < 0.9:
        partes.append(frag_pariente(p))
    if p.get("cruce"):
        partes.append(frag_cruce(p))
    if p["eco"] == "discapacidad" and rng.random() < 0.45:
        partes.insert(2, frag_dis_lsm(p))
    partes.append(cierre(p))
    # deduplicar por si el azar repite un fragmento idéntico
    vistos, limpio = set(), []
    for x in partes:
        if x not in vistos:
            vistos.add(x); limpio.append(x)
    return limpio

def fmt_carta(p, largo):
    n = {"corta":4, "media":6, "larga":9}[largo]
    parr = cuerpo(p, n)
    lugar = p["residencia"].split(",")[0]
    lineas = [f"{lugar}, a {fecha_2026()}.", "", "A quien corresponda:", ""]
    lineas.append(f"Mi nombre es {p['nombre']} {p['apellido']}. Me dirijo a usted con el propósito de compartir la trayectoria que he desarrollado como {p['rol']}, con la intención de que esta experiencia pueda ser considerada dentro del ecosistema de conocimiento y aprendizaje situado.")
    lineas.append("")
    for x in parr:
        lineas.append(x); lineas.append("")
    lineas += ["Agradezco su atención y quedo a disposición para cualquier información adicional.", "", "Atentamente,", "", f"{p['nombre']} {p['apellido']}", f"{p['rol'].capitalize()} — {p['residencia']}"]
    return "\n".join(lineas)

def fmt_biografia_oral(p, largo):
    n = {"corta":5, "media":8, "larga":12}[largo]
    parr = cuerpo(p, n)
    dur = {"corta": rng.randint(9,18), "media": rng.randint(22,40), "larga": rng.randint(45,80)}[largo]
    head = [
        "TRANSCRIPCIÓN DE ENTREVISTA — BIOGRAFÍA DE VIDA",
        f"Proyecto IH-2025-I-445 · Ecosistema: {p['eco']}",
        f"Persona entrevistada: {p['nombre']} {p['apellido']} ({p['edad']} años, {p['rol']})",
        f"Fecha: {fecha_2026()} · Duración aproximada: {dur} min",
        "Nota: transcripción de audio; se conservan muletillas y marcas de oralidad.",
        "-" * 60, ""]
    aperturas = [
        "E: Gracias por recibirnos. ¿Podría contarnos su historia, desde donde usted quiera empezar?",
        "E: Le agradezco su tiempo. Cuénteme, ¿cómo llegó usted a este trabajo?",
        "E: Empecemos por donde usted prefiera: su pueblo, su familia, su oficio.",
    ]
    body = [rng.choice(aperturas), ""]
    for i, x in enumerate(parr):
        body.append("P: " + oraliza(x))
        body.append("")
        if i in (1, max(2, len(parr)//2)) and rng.random() < 0.8:
            repes = ["E: ¿Y cómo fue eso para usted?", "E: ¿Me puede dar un ejemplo?", "E: ¿Qué pasó después?", "E: ¿Y la gente cómo respondía?", "E: ¿Eso cuándo fue, más o menos?"]
            rng.shuffle(repes)
            pregunta = next(q for q in repes if q not in body)
            body.append(pregunta); body.append("")
    body.append("E: Muchas gracias. ¿Algo más que quiera que quede grabado?")
    body.append("")
    finales = ["P: Pues nomás eso: que se use bien lo que aquí dije. [risas] Que no se quede guardado.",
               "P: Que le pongan mi nombre como es, y que la historia regrese a la comunidad. Eso sería todo.",
               "P: No, ya dije mucho. [pausa] Bueno, sí: gracias por escuchar. Eso casi nunca pasa."]
    body.append(rng.choice(finales))
    return "\n".join(head + body)

def fmt_testimonio(p, largo):
    n = {"corta":3, "media":5, "larga":7}[largo]
    parr = cuerpo(p, n)
    head = [f"TESTIMONIO — {p['nombre']} {p['apellido']}",
            f"{p['rol'].capitalize()}, {p['edad']} años · {p['residencia']} · {fecha_2026()}", ""]
    return "\n".join(head + [x + "\n" for x in parr])

def fmt_ficha(p, largo):
    n = {"corta":2, "media":4, "larga":6}[largo]
    parr = cuerpo(p, n)
    filas = [
        "FICHA DE PARTICIPANTE — ECOSISTEMAS DE CONOCIMIENTO Y APRENDIZAJE SITUADO",
        f"Proyecto: IH-2025-I-445 · Fecha de registro: {fecha_2026()}",
        "-" * 60,
        f"Nombre: {p['nombre']} {p['apellido']}",
        f"Edad: {p['edad']} años",
        f"Lugar de origen: {p['origen']}",
        f"Residencia actual: {p['residencia']}" + (f" (colonia {p['colonia']})" if p.get("colonia") else ""),
        f"Lengua(s): {p['lengua']} y español" if p["eco"] in ("traduccion",) or rng.random()<0.3 else "Lengua(s): español",
        f"Rol en el ecosistema: {p['rol']}",
        f"Años de experiencia: {p['anios']}",
        f"Espacio principal de actividad: {p['sitio']}",
        "-" * 60,
        "SEMBLANZA (en palabras de la persona participante):", ""]
    return "\n".join(filas + [x + "\n" for x in parr])

def fmt_diario(p, largo):
    n = {"corta":3, "media":5, "larga":8}[largo]
    parr = cuerpo(p, n)
    head = [f"NOTAS PERSONALES DE CAMPO — {p['nombre']} {p['apellido']} ({p['rol']})", ""]
    fechas = sorted(((rng.randint(0,5), rng.randint(2,27)) for _ in parr))
    body = []
    for (m, d), x in zip(fechas, parr):
        body.append(f"{d} de {MESES[m]} de 2026."); body.append(x); body.append("")
    return "\n".join(head + body)

FORMATOS = {
    "carta_presentacion": fmt_carta,
    "biografia_oral": fmt_biografia_oral,
    "testimonio": fmt_testimonio,
    "ficha_participante": fmt_ficha,
    "diario_personal": fmt_diario,
}

def elegir_formato(p):
    pesos = {"carta_presentacion":22, "biografia_oral":30, "testimonio":22, "ficha_participante":16, "diario_personal":10}
    if p["eco"] == "traduccion":
        pesos["carta_presentacion"] += 12  # espeja el insumo real (Reyna)
    fmts, w = zip(*pesos.items())
    return rng.choices(fmts, weights=w, k=1)[0]

def elegir_largo():
    return rng.choices(["corta","media","larga"], weights=[30,45,25], k=1)[0]

# ---------------------------------------------------------------- main
def main():
    personas, fam = make_personas()
    manifest = []
    for p in personas:
        fmt = elegir_formato(p)
        largo = elegir_largo()
        texto = FORMATOS[fmt](p, largo)
        fname = f"SIM_{p['id']:04d}_{p['eco']}_{fmt}_{largo}.txt"
        with open(os.path.join(OUT, "txt", fname), "w", encoding="utf-8") as f:
            f.write(texto)
        manifest.append(dict(id=p["id"], archivo=fname, ecosistema=p["eco"], formato=fmt,
                             longitud=largo, palabras=len(texto.split()),
                             nombre=f"{p['nombre']} {p['apellido']}", edad=p["edad"],
                             rol=p["rol"], lengua=p["lengua"], origen=p["origen"],
                             residencia=p["residencia"], sitio_ancla=p["sitio"],
                             cruce_ecosistema="sí" if p.get("cruce") else "no",
                             pariente=p.get("pariente",""),
                             sintetico="SÍ — dato apócrifo de prueba"))
    with open(os.path.join(OUT, "MANIFEST.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(manifest[0].keys()))
        w.writeheader(); w.writerows(manifest)
    print(f"Generados {len(manifest)} recursos.")
    print("Pares familiares (ids):", fam)

if __name__ == "__main__":
    main()

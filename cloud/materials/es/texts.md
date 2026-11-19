# Many Worlds Cloud · Español

## Eslóganes
- Sepa qué está expuesto en su nube y qué hacer al respecto.
- De miles de comprobaciones fallidas a tres listas sobre las que actuar.
- Lo no analizado nunca se muestra como limpio.

## Descripción breve
Many Worlds Cloud lee lo que Prowler, el escáner de código abierto, encuentra en sus cuentas en la nube y lo convierte en un informe y en una lista de cosas sobre las que actuar: riesgos, incidentes y tareas.

## Descripción media
Many Worlds Cloud convierte los análisis de seguridad en la nube en decisiones. Prowler, el escáner de código abierto, comprueba sus cuentas de AWS, Azure, Google Cloud, Kubernetes y Microsoft 365 con un rol de solo lectura. Many Worlds Cloud lee los resultados y redacta un informe que empieza diciendo hasta qué punto pudo analizarse su nube, ordena los hallazgos por gravedad y termina en tres listas: riesgos para el registro, incidentes para el SOC y tareas para una cola. Un botón las envía a SpaceRisk.

## Descripción larga
Un escáner de seguridad en la nube devuelve miles de filas, y con eso nadie puede decidir. Many Worlds Cloud lee lo que Prowler, el escáner de código abierto, encuentra en sus cuentas en la nube y lo convierte en un informe que tres tipos de lector pueden usar. La dirección recibe un resumen ejecutivo que responde en una página: si el riesgo sube o baja, qué está abierto a internet, quién tiene acceso de administrador. Los responsables de la nube reciben una vista que baja hasta el recurso concreto. Quienes hacen el trabajo reciben el informe completo con las pruebas. Cada informe empieza con qué cuentas se analizaron y qué comprobaciones no pudieron ejecutarse, de modo que una cuenta sin analizar nunca se muestra como limpia. Los hallazgos se ordenan por gravedad, cada uno con por qué importa, qué hacer y las pruebas, y se relacionan con marcos como CIS, ISO 27001, NIS2 y ENS. El informe termina en tres listas: riesgos, incidentes y tareas. Un botón las envía a un registro de SpaceRisk, y hay exportaciones para un SIEM, Jira, ServiceNow, Excel y PowerPoint. Many Worlds Cloud solo lee. Funciona en su propio servidor y no cambia nada en su nube.

## Funciones
- **Solo lee:** No se instala nada en su nube ni se cambia nada en ella. Prowler analiza cada cuenta en la nube con un rol de solo lectura. Many Worlds Cloud lee los resultados. Nunca escribe en sus cuentas y nunca pide los secretos que encuentra, solo dónde están.
- **¿Se puede confiar en estos resultados?:** El informe empieza diciendo hasta qué punto pudo analizarse su nube. Una cuenta que está en silencio porque el análisis falló nunca debe leerse como una cuenta sin problemas. Por eso cada informe empieza con qué cuentas se analizaron, cuándo, y qué comprobaciones no pudieron ejecutarse.
- **Hallazgos, ordenados por gravedad:** Cada hallazgo incluye por qué importa, qué hacer y las pruebas. Un hallazgo es algo que el análisis observó y que requiere una decisión. Los peores aparecen primero, y cada uno puede rastrearse hasta el recurso y la comprobación que hay detrás.
- **Cumplimiento:** Vea qué requisitos cumple y cuáles no. Prowler relaciona sus comprobaciones con los marcos por los que preguntan los auditores. El informe muestra cada marco requisito por requisito, con los hallazgos que hay detrás de cada incumplimiento.
- **Conclusiones:** El informe termina en tres listas sobre las que alguien puede actuar. Los riesgos van a un registro, los incidentes a un SOC y las tareas a una cola. Cada valoración lleva la regla que la produjo.
- **Todas las cuentas a la vez:** Ordene sus cuentas en la nube por lo que hay que decidir. Con más de una cuenta, suscripción o proyecto las tiene una junto a otra: cuál necesita atención primero, qué ocurre en varias frente a lo que ocurre en una sola, y cuáles no pudieron analizarse por completo.

## Texto estándar
Acerca de Many Worlds Cloud: Many Worlds Cloud es una aplicación de informes para la seguridad en la nube. Lee los resultados de Prowler, el escáner de seguridad en la nube de código abierto, y los convierte en un informe con tres vistas y tres listas sobre las que actuar: riesgos, incidentes y tareas. Funciona en su propio servidor, solo lee, y puede enviar sus conclusiones a un registro de riesgos de SpaceRisk. Many Worlds Cloud forma parte de la familia Many Worlds de Frivold Digital, junto con Many Worlds Historian y Many Worlds Identity.

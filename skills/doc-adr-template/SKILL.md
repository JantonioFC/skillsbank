---
id: doc-adr-template
name: doc-adr-template
description: Genera documentos ADR (Architectural Decision Record) para registrar
  decisiones arquitectónicas del proyecto.
category: documentacion-de-codigo
risk: safe
source: personal
date_added: '2026-03-11'
---


# doc-adr-template

Genera un documento ADR (Registro de Decision Arquitectonica) cuando el usuario necesita documentar una decision de arquitectura.

## Cuando usar esta skill
- Cuando el usuario necesita registrar y justificar una decision arquitectonica importante (eleccion de tecnologia, patron de diseno, cambio de infraestructura)
- Cuando se requiere documentar alternativas consideradas y los trade-offs de una decision tecnica
- Cuando se necesita trazabilidad historica de decisiones para que futuros ingenieros comprendan el contexto

## Instrucciones
1. Analizar el contexto del proyecto actual (stack, arquitectura, equipo)
2. Rellenar la plantilla adaptandola al contexto especifico
3. Usar espanol para el contenido, manteniendo terminos tecnicos en ingles donde corresponda
4. No dejar secciones vacias — si algo no aplica, indicar "N/A" con justificacion
5. Preguntar al usuario si hay secciones que requieren decisiones pendientes

## Plantilla

# **ADR [ID]: [Titulo de la Decision Arquitectonica]**

**Fecha de Registro:** [YYYY-MM-DD]

**Estado Actual:** [Propuesto / Bajo Revision / Aprobado / Superado por ADR-XXX / Deprecado]

**Autores:** [Nombre del responsable / Arquitecto / Equipo de Ingenieria]

**RFC de Referencia:** [Enlace a RFC-XXX que origino el debate]

**Nivel de Impacto:** [Local (Componente) / Departamental (Servicio) / Global (Arquitectura del Sistema)]

**Modulos y Servicios Afectados:** [Ej. Core API, Auth Gateway, Infraestructura de Mensajeria, CI/CD Pipeline]

## **1. Contexto y Definicion del Problema**

Describe la situacion especifica, tecnica o de negocio, que nos obligo a tomar una decision critica en este momento. Esta seccion debe capturar el "espiritu de la epoca" del sistema para que futuros ingenieros comprendan las presiones del momento.

* **Fuerzas Impulsoras (Drivers):** Cual era el problema puntual y que lo disparo?
  * *Ejemplo Tecnico:* "El sistema actual de colas basado en memoria no garantiza el orden de los mensajes (FIFO) bajo una carga de 50k eventos/seg, lo que causa inconsistencias en el estado de las transacciones financieras".
  * *Ejemplo de Negocio:* "La necesidad de cumplir con la normativa GDPR exige que los datos de usuario sean eliminados fisicamente de todos los backups en menos de 48 horas".
* **Restricciones y Limitaciones:** Factores externos o internos que acotaron nuestro margen de maniobra.
  * *Ej. Presupuesto:* "Limitacion de gasto en servicios gestionados de AWS a un maximo de $500/mes para este microservicio".
  * *Ej. Tiempo:* "La solucion debe implementarse antes del cierre del trimestre fiscal".
  * *Ej. Stack:* "Debemos mantener la compatibilidad con Node.js 18 LTS".
* **Supuestos e Hipotesis de Partida:** Que dabamos por sentado al momento de decidir?
  * *Ejemplo:* "Asumimos que el volumen de trafico no escalara mas de un 200% en los proximos 12 meses basandonos en las proyecciones de marketing".

## **2. Decision Arquitectonica y Justificacion**

Esta es la declaracion formal, definitiva y vinculante de la solucion adoptada. Debe ser redactada de forma tecnica, clara y sin ambiguedades.

* **Sentencia de Decision:** "Hemos decidido adoptar [Tecnologia/Patron/Libreria] para [Proposito especifico y alcance]".
* **Alcance y Aplicabilidad:** A que partes del sistema aplica esta decision de forma obligatoria? Es un estandar que debe seguirse en futuros desarrollos o una excepcion para un caso de uso especifico?
* **Justificacion Critica:** El motivo principal (o "killer reason") por el cual esta opcion resulto ganadora sobre las demas.
  * *Ejemplo:* "Se prioriza la **consistencia fuerte** y la integridad referencial sobre la disponibilidad extrema debido a la naturaleza critica de los datos contables, lo que invalida el uso de bases de datos NoSQL para este modulo".
* **Arquitectura Meta:** Breve descripcion de como se integra esta decision en la vision a largo plazo del sistema.

## **3. Alternativas Consideradas y Analisis Comparativo**

Breve mencion de las opciones descartadas para contextualizar la eleccion y evitar que se repitan discusiones pasadas.

* **Alternativa A: [Nombre de la Tecnologia/Patron]**
  * **Pros:** [Velocidad de desarrollo, bajo costo, soporte de comunidad].
  * **Contras:** [Escalabilidad limitada, falta de soporte para transacciones ACID].
  * **Motivo del Rechazo:** [Ej. "Aunque era mas barato, no cumplia con los requisitos de latencia p99 requeridos"].
* **Alternativa B: [Nombre de la Tecnologia/Patron]**
  * **Pros:** [Rendimiento extremo, integracion nativa con el stack].
  * **Contras:** [Alta curva de aprendizaje, requiere gestionar infraestructura propia].
  * **Motivo del Rechazo:** [Ej. "El equipo de ingenieria no cuenta con experiencia en Rust y los tiempos de entrega no permiten la capacitacion"].

## **4. Consecuencias y Compromisos (Trade-offs)**

Toda decision de arquitectura es un intercambio. Esta seccion es vital para que quienes mantengan el sistema en el futuro sepan a que atenerse.

### **4.1 Impactos Positivos (Beneficios Esperados)**

* **Escalabilidad y Rendimiento:** [Ej. "Esperamos una reduccion del 40% en los tiempos de respuesta de lectura mediante el uso de replicas distribuidas"].
* **Mantenibilidad y DX:** [Ej. "El codigo sera mas modular y desacoplado, permitiendo que nuevos desarrolladores se incorporen al proyecto un 25% mas rapido"].
* **Seguridad y Cumplimiento:** [Ej. "Reduccion drastica de la superficie de ataque al delegar la gestion de secretos a HashiCorp Vault"].

### **4.2 Impactos Negativos, Riesgos y "Deuda Consentida"**

* **Complejidad Operativa:** [Ej. "Introducimos un nuevo cluster de Kafka que requiere monitoreo especializado y rotacion de certificados manual"].
* **Curva de Aprendizaje y Cultura:** [Ej. "El equipo de Backend debera cambiar su paradigma de programacion imperativa a uno basado en eventos/streams"].
* **Latencia y Overhead:** [Ej. "La introduccion de este middleware anade un overhead de red de aproximadamente 15-20ms por peticion sincronica"].

### **4.3 Acciones Derivadas e Implementacion**

* [ ] Actualizacion de scripts de infraestructura como codigo (Terraform/CloudFormation).
* [ ] Plan de migracion de datos para sistemas en caliente (Zero-downtime migration).
* [ ] Sesion de "Transferencia de Conocimiento" y actualizacion de la documentacion tecnica en la Wiki.

## **5. Validacion, Verificacion y Observabilidad**

Como auditaremos que la decision fue la correcta y que se esta cumpliendo lo prometido?

* **Metricas de Control de Exito:** [Ej. "El porcentaje de mensajes perdidos debe ser estrictamente 0% segun los logs de auditoria"].
* **Observabilidad y Alertas:** [Ej. "Configurar una alerta en Grafana si el lag del consumidor de la cola supera los 5 minutos"].
* **Pruebas de Esfuerzo (Stress Testing):** [Ej. "Ejecucion de un test de carga simulando un Black Friday para verificar que la latencia no se degrade mas alla del umbral definido"].

## **6. Gobernanza y Ciclo de Vida de la Decision**

* **Politica de Revision:** Esta decision debe revisarse en [X meses] o cuando el trafico supere los [X usuarios].
* **ADR Superado por:** (Si esta decision es reemplazada en el futuro, se debe colocar aqui el enlace al nuevo ADR para mantener la trazabilidad).
* **Notas Post-Implementacion:** [Cualquier aprendizaje, incidente o ajuste realizado durante el despliegue real].
* **Documentacion Relacionada:** [Enlace a Swagger, Diagramas de Arquitectura en Miro o Repositorios de Codigo].

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

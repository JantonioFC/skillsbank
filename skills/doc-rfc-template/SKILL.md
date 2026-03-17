---
id: doc-rfc-template
name: doc-rfc-template
description: Genera documentos RFC (Request for Comments) para propuestas técnicas.
category: documentacion-de-codigo
risk: safe
source: personal
date_added: '2026-03-11'
---

# doc-rfc-template

Genera un RFC (Request for Comments) técnico completo cuando el usuario necesita proponer y documentar un cambio arquitectónico o técnico significativo.

## Cuándo usar esta skill
- Cuando el usuario necesita escribir una propuesta técnica formal (RFC) para un cambio de arquitectura, migración o decisión técnica importante
- Cuando se requiere documentar alternativas evaluadas, trade-offs, plan de implementación y estrategia de rollout para un cambio técnico
- Cuando el equipo necesita un documento estructurado para revisión técnica colaborativa antes de implementar un cambio de alto impacto

## Instrucciones
1. Analizar el contexto del proyecto actual (stack, arquitectura, equipo)
2. Rellenar la plantilla adaptándola al contexto específico
3. Usar español para el contenido, manteniendo términos técnicos en inglés donde corresponda
4. No dejar secciones vacías — si algo no aplica, indicar "N/A" con justificación
5. Preguntar al usuario si hay secciones que requieren decisiones pendientes

## Plantilla

# **RFC: \[Título Descriptivo de la Propuesta Técnica\]**

**Autor(es):** \[Nombre del proponente / Equipo\]

**Estado:** \[Borrador / En Revisión / Aprobado / Rechazado / Deprecado\]

**Fecha de Creación:** \[Fecha\]

**Fecha de Última Actualización:** \[Fecha\]

**Referencia a Épica/Historias:** \[Enlace a US-XXX o Épica-XXX\]

**Nivel de Impacto:** \[Bajo / Medio / Alto / Crítico\]

## **1\. Resumen Ejecutivo (Abstract)**

Una descripción concisa (uno o dos párrafos) del cambio técnico propuesto. Debe responder rápidamente a tres preguntas clave:

1. **¿Qué vamos a cambiar?** (Ej. Migración de arquitectura monolítica a microservicios para el módulo de pagos).
2. **¿Por qué ahora?** (Ej. El sistema actual no escala ante picos de demanda superiores a 500 RPM).
3. **¿Cuál es el beneficio técnico inmediato?** (Ej. Reducción del radio de explosión de fallos y despliegues independientes).

Este resumen es vital para que los *stakeholders* técnicos y de producto entiendan la magnitud y urgencia del impacto sin necesidad de leer la totalidad de las especificaciones técnicas.

## **2\. Contexto y Motivación**

Explica el trasfondo detallado que nos ha llevado a esta propuesta. Esta sección justifica la inversión de tiempo y recursos.

* **Problema Técnico Detallado:** Describe la limitación actual con datos específicos. (Ej: "La latencia de escritura en la DB principal promedia los 800ms debido a la contención de bloqueos durante el cierre de facturación").
* **Análisis de Deuda Técnica:** ¿Estamos resolviendo un problema estructural o simplemente aplicando un parche? Explica cómo este cambio reduce la fricción para futuros desarrollos.
* **Oportunidad y Tendencias:** ¿Qué nueva tecnología, patrón de diseño o actualización de librería nos permite dar este salto? (Ej. "La adopción de Kafka nos permitirá pasar de un procesamiento sincrónico a uno basado en eventos").
* **Evidencia Empírica:** Incluye enlaces a dashboards de telemetría, logs de errores críticos o informes de auditoría que prueben que el sistema actual es insuficiente.

## **3\. Objetivos (Metas y No-Metas)**

Es fundamental delimitar qué intenta resolver esta RFC y qué queda explícitamente fuera de su alcance para evitar el "scope creep".

* **Metas (Goals \- Qué SI queremos lograr):**
  * \[Ej: Reducir el tiempo de respuesta de la API P95 en un 30% en condiciones de carga máxima\].
  * \[Ej: Lograr una cobertura de tests de integración del 90% en el nuevo servicio\].
  * \[Ej: Desacoplar el dominio de Inventario del dominio de Ventas\].
* **No-Metas (Non-Goals \- Qué NO vamos a tocar):**
  * \[Ej: Esta RFC no contempla la migración de la base de datos de producción a la nube; eso será un proyecto independiente\].
  * \[Ej: No se modificará la lógica de la interfaz de usuario (Frontend) en esta iteración técnica\].
  * \[Ej: No se optimizarán los microservicios que no estén directamente involucrados en el flujo de pagos\].

## **4\. Propuesta de Solución Detallada**

Esta es la sección técnica central del documento. Debe ser lo suficientemente descriptiva para que un desarrollador ajeno al proyecto pueda entender la implementación.

### **4.1 Arquitectura y Diagramas**

Visualiza la solución para facilitar la comprensión cognitiva.

* **Diagrama de Componentes:**
* **Descripción de la Topología:** Explica cómo interactúan los nuevos servicios con la infraestructura existente.
* **Flujo de Datos y Secuencia:** ¿Cómo viaja una petición desde el Gateway hasta el almacenamiento? Detalla las transacciones y estados intermedios.

### **4.2 Cambios en el Esquema de Datos y Persistencia**

Si hay cambios en la base de datos o en la forma de almacenar información, descríbelos aquí.

* **Modelado de Datos:** Describe nuevas tablas, colecciones o esquemas de mensajes (Protobuf/Avro).
* **Estrategia de Migración de Datos:** ¿Cómo moveremos los datos de la estructura antigua a la nueva? (Ej. Proceso de doble escritura, migración por lotes nocturna).
* **Downtime Estimado:** ¿Requiere el sistema una ventana de mantenimiento o se puede realizar en caliente (*Zero Downtime*)?

### **4.3 Especificaciones de API / Contratos de Interfaz**

* **Nuevos Endpoints:** POST /api/v2/process-transaction
* **Definición de Payloads:** Detalla campos obligatorios, opcionales y tipos de datos.
* **Retrocompatibilidad:** ¿Cómo manejaremos a los clientes que siguen usando la versión antigua? (Ej. Uso de adaptadores o encabezados de versión).

## **5\. Alternativas Consideradas**

Un diseño técnico profesional requiere evaluar y descartar otros caminos. Esto demuestra que la solución elegida no fue arbitraria.

* **Opción A (La elegida):** Resumen de ventajas competitivas (costo, velocidad de desarrollo, escalabilidad).
* **Opción B (Tecnología alternativa):** ¿Por qué no usamos \[Tecnología X\]? (Ej: "Aunque Redis es más rápido, necesitamos la persistencia garantizada de PostgreSQL para este caso de uso").
* **Opción C (The "Do Nothing" approach):** ¿Qué pasaría si no hacemos nada? Calcula el riesgo de inacción (Ej. "En seis meses el sistema colapsará ante el crecimiento proyectado").

## **6\. Impacto y Trade-offs (Compromisos)**

Toda decisión técnica tiene un precio. La honestidad técnica sobre lo que sacrificamos es fundamental.

* **Rendimiento vs. Consumo:** ¿Ganamos velocidad a costa de usar más RAM o CPU?
* **Complejidad Operativa:** ¿Requiere este cambio que el equipo de DevOps aprenda una nueva herramienta de orquestación?
* **Developer Experience (DX):** ¿Hará esto que el desarrollo local sea más lento o más difícil de depurar?
* **Costos de Infraestructura:** ¿Cómo afectará esto a la factura mensual de AWS/GCP/Azure?

## **7\. Plan de Implementación y Rollout (Estrategia de Despliegue)**

¿Cómo vamos a llevar esto a la realidad sin poner en riesgo el negocio?

1. **Fase 1 (Desarrollo y Staging):** Implementación de la lógica núcleo y validación en entornos controlados.
2. **Fase 2 (Shadowing / Dark Launch):** Enviar tráfico real al nuevo sistema pero sin usar su respuesta para el usuario final. Esto permite validar el comportamiento con carga real.
3. **Fase 3 (Canary Release / Feature Flags):** Despliegue gradual. Primero al 5% de usuarios, luego al 25%, hasta llegar al 100%.
4. **Fase 4 (Monitorización y Cleanup):** Una vez estable, eliminar el código legado y los recursos (instancias, colas) que ya no se necesiten.

## **8\. Estrategia de Testing y Observabilidad**

Un cambio no está terminado hasta que podemos medir que funciona correctamente.

* **Nivel de Pruebas:** Detalla planes para Unit Tests, Integration Tests y End-to-End (E2E).
* **Métricas de Observabilidad:** ¿Qué métricas personalizadas (Custom Metrics) vamos a emitir? (Ej. Tasa de error de la nueva función Lambda).
* **Alertas de Salud:** ¿Cuándo debe sonar el teléfono del equipo de guardia? Define los umbrales de alerta.
* **Protocolo de Rollback:** Si el despliegue falla en el 50%, ¿cuánto tiempo tardamos en volver a la versión anterior? Describe el proceso manual o automático.

## **9\. Seguridad y Gobernanza**

* **Autenticación y Autorización:** ¿Cómo se protegen los nuevos endpoints? (Ej. OAuth2, mTLS).
* **Privacidad de Datos (GDPR/Compliance):** ¿Estamos almacenando datos sensibles (PII)? ¿Cómo se anonimizan o encriptan?
* **Análisis de Vulnerabilidades:** ¿Se ha realizado un escaneo de dependencias para evitar ataques de cadena de suministro?

## **10\. Preguntas Abiertas e Incertidumbres**

Lista de dudas que el autor tiene y sobre las que espera que los revisores comenten específicamente.

* *¿Deberíamos usar un clúster dedicado para esta base de datos o compartir el existente?*
* *¿Cómo afectará el aumento de la latencia de red si movemos este servicio a una región diferente?*

## **11\. Apéndices y Referencias**

* \[Enlace a Documentación Oficial de la tecnología elegida\].
* \[Enlace a Código de prueba o Proof of Concept (PoC)\].
* \[Enlace a ADRs relacionados\].

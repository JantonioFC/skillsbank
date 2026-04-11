---
id: doc-prd-template
name: doc-prd-template
description: |-
  Genera documentos PRD (Product Requirements Document) para requisitos de producto.
category: documentacion-de-codigo
risk: safe
source: personal
date_added: '2026-03-11'
license: MIT
---
# doc-prd-template

Genera un PRD (Documento de Requisitos de Producto) completo cuando el usuario necesita definir los requisitos y estrategia de un producto o funcionalidad.

## Cuándo usar esta skill
- Cuando el usuario necesita crear un documento de requisitos de producto para una nueva funcionalidad o proyecto
- Cuando se requiere formalizar la visión, objetivos, personas, requisitos funcionales y no funcionales de un producto
- Cuando el equipo necesita un documento estructurado para alinear stakeholders técnicos y de negocio antes del desarrollo

## Instrucciones
1. Analizar el contexto del proyecto actual (stack, arquitectura, equipo)
2. Rellenar la plantilla adaptándola al contexto específico
3. Usar español para el contenido, manteniendo términos técnicos en inglés donde corresponda
4. No dejar secciones vacías — si algo no aplica, indicar "N/A" con justificación
5. Preguntar al usuario si hay secciones que requieren decisiones pendientes

## Plantilla

# **PRD: \[Nombre del Proyecto o Funcionalidad\]**

**Estado:** \[Borrador / En Revisión / Aprobado / En Desarrollo / Lanzado\]

**Dueño del Producto:** \[Nombre del responsable\]

**Líder Técnico:** \[Nombre del responsable\]

**Fecha de última actualización:** \[Fecha\]

**App ID / Identificador de Proyecto:** \[ID único para referencia en código o IA\]

## **1\. Resumen Ejecutivo**

Proporciona una visión general de alto nivel que cualquier miembro del equipo pueda entender en menos de dos minutos.

* **Visión del Producto:** Describe el estado futuro deseado tras el lanzamiento.
* **Propuesta de Valor:** ¿Cuál es el beneficio diferencial? (Ej. "Reducir el tiempo de despliegue en un 40% mediante automatización de agentes").
* **Público Objetivo:** Define brevemente quiénes son los beneficiarios primarios y secundarios.
* **Contexto de Mercado:** Breve mención a la competencia o soluciones actuales internas que este proyecto reemplaza o mejora.

## **2\. Definición y Análisis del Problema**

Describe con profundidad el "dolor" o la brecha que este proyecto intenta cerrar.

* **Estado Actual:** Detalla el flujo de trabajo hoy. ¿Qué herramientas se usan? ¿Dónde están los cuellos de botella?
* **Impacto de No Resolverlo:** Analiza las consecuencias de mantener el *status quo* (Ej. pérdida de ingresos, frustración del equipo, deuda técnica acumulada).
* **Evidencia:** Incluye citas de usuarios, capturas de errores frecuentes o datos estadísticos que validen la urgencia.
* **Análisis de Causas Raíz:** ¿Por qué existe este problema? (Limitaciones técnicas, falta de procesos, herramientas obsoletas).

## **3\. Objetivos Estratégicos y KPIs (Indicadores Clave de Desempeño)**

Define cómo mediremos el éxito de forma cuantitativa y cualitativa. Los objetivos deben seguir la metodología **SMART**.

| Objetivo | Métrica de Éxito (KPI) | Línea Base (Hoy) | Meta (Paso Final) |
| :---- | :---- | :---- | :---- |
| **Optimizar Retención** | Churn Rate mensual | 12% | Menos del 7% |
| **Rendimiento UI** | Tiempo de carga (LCP) | 3.5s | Menos de 1.2s |
| **Eficiencia Dev** | Ciclo de vida de PRs | 48h | Menos de 12h |

* **Estrategia de Seguimiento:** ¿Cómo extraeremos estos datos? (Ej. "Uso de telemetría de Google Analytics", "Consultas directas a la réplica de lectura de base de datos").

## **4\. User Personas (Perfiles de Usuario)**

Describe con detalle a quienes interactuarán con el sistema para que el diseño sea empático.

* **\[Perfil 1: El Administrador\]:** \* **Contexto:** Responsable de la configuración global.
  * **Necesidad:** Control total, logs detallados y capacidad de rollback.
  * **Competencia Técnica:** Alta. Prefiere CLIs o dashboards densos en información.
* **\[Perfil 2: El Usuario Final\]:** \* **Contexto:** Realiza la tarea principal del negocio (Ej. comprar, reportar).
  * **Necesidad:** Rapidez, mínima fricción y feedback visual claro.
  * **Competencia Técnica:** Media-Baja. Valora la intuición y la ayuda contextual.

## **5\. Requisitos Funcionales (Alcance Detallado)**

Lista de funcionalidades priorizadas mediante el método **MoSCoW** (Must have, Should have, Could have, Won't have).

### **P0: Críticos (Imprescindibles para el Lanzamiento)**

* **RF.01:** Autenticación robusta mediante SSO (SAML/OIDC).
* **RF.02:** Interfaz de tablero con filtrado dinámico por fecha y categoría.
* **RF.03:** Capacidad de exportación de datos en formato JSON y CSV.

### **P1: Importantes (Añaden valor significativo)**

* **RF.04:** Sistema de notificaciones *push* para cambios de estado críticos.
* **RF.05:** Integración con herramientas de terceros (Notion/Slack) vía Webhooks.

### **Fuera de Alcance (Out of Scope)**

* *Módulo de pagos internacionales (se tratará en la Fase 2).*
* *Soporte para navegadores heredados (IE11).*

## **6\. Requisitos No Funcionales (Calidad y Operaciones)**

Atributos transversales que aseguran la robustez y profesionalismo de la solución.

* **Escalabilidad:** El sistema debe escalar horizontalmente de forma automática al superar el 70% de uso de CPU.
* **Observabilidad:** Implementación de trazabilidad distribuida. Cada petición debe tener un correlation-id único persistido en logs.
* **Seguridad:** Encriptación de datos sensibles mediante AES-256. Rotación automática de secretos cada 90 días.
* **Mantenibilidad:** El código debe mantener un índice de complejidad ciclomática bajo y una cobertura de tests mínima del 85%.
* **Resiliencia:** Implementación de patrones *Circuit Breaker* para todas las llamadas a servicios externos.

## **7\. Experiencia de Usuario (UX) e Interacción**

* **Principios de Diseño:** Definir el lenguaje visual (Ej. "Diseño atómico", "Accesibilidad primero").
* **Arquitectura de Información:** Mapa del sitio o estructura jerárquica de navegación.
* **User Journeys Críticos:** Enlace a diagramas que muestren el camino del usuario desde el inicio hasta la conversión.
* **Mockups / Wireframes:** Enlaces a archivos de diseño (Figma, Sketch) con comentarios sobre micro-interacciones.

## **8\. Riesgos, Supuestos y Estrategias de Mitigación**

Anticiparse a los problemas es parte de la ingeniería de excelencia.

* **Riesgo:** La API del proveedor externo no es estable.
  * **Mitigación:** Implementar una capa de caché agresiva y un modo de "funcionamiento degradado" que use datos locales.
* **Supuesto:** Contamos con que el equipo de Infraestructura tendrá listo el entorno de Staging para la semana 4\.
* **Dependencia:** Aprobación del equipo legal para el manejo de datos en la región EU.

## **9\. Criterios de Gating y Calidad para el Lanzamiento**

Condiciones innegociables para dar el "Go" a producción.

1. **Seguridad:** Escaneo de vulnerabilidades (SAST/DAST) completado con 0 hallazgos críticos.
2. **QA:** Todos los tests de regresión automatizados en verde.
3. **Performance:** Prueba de carga superada con 5000 peticiones por segundo y latencia p95 \< 200ms.
4. **Documentación:** Manual de usuario y documentación técnica (Swagger/Wiki) actualizada al 100%.

## **10\. Plan de Comunicación y Rollout**

* **Estrategia de Lanzamiento:** (Ej. "Canary Release" al 5% de usuarios, luego incremento gradual).
* **Canales de Soporte:** ¿Dónde reportan bugs los usuarios? (Ej. Canal de Slack \#soporte-proyecto).
* **Ciclo de Feedback:** Planificación de la primera reunión de revisión post-lanzamiento (Retro).

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

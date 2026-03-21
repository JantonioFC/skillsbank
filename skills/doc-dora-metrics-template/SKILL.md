---
id: doc-dora-metrics-template
name: doc-dora-metrics-template
description: Genera reportes de métricas DORA y salud del ecosistema de desarrollo.
category: documentacion-de-codigo
risk: safe
source: personal
date_added: '2026-03-11'
license: MIT
---



# doc-dora-metrics-template

Genera un reporte de métricas DORA y salud de ingeniería cuando el usuario necesita evaluar el rendimiento de su equipo y sistemas.

## Cuándo usar esta skill
- Cuando el usuario necesita generar un reporte de métricas DORA (Deployment Frequency, Lead Time, Change Failure Rate, TTRS)
- Cuando se requiere evaluar la salud del sistema incluyendo calidad de código, deuda técnica y observabilidad
- Cuando el equipo necesita documentar incidentes, cuellos de botella y estrategias de mejora para el próximo periodo

## Instrucciones
1. Analizar el contexto del proyecto actual (stack, arquitectura, equipo)
2. Rellenar la plantilla adaptándola al contexto específico
3. Usar español para el contenido, manteniendo términos técnicos en inglés donde corresponda
4. No dejar secciones vacías — si algo no aplica, indicar "N/A" con justificación
5. Preguntar al usuario si hay secciones que requieren decisiones pendientes

## Plantilla

# **Reporte de Métricas DORA y Salud de Ingeniería**

**Proyecto / Servicio:** \[Nombre del Proyecto / Identificador del Microservicio\]

**Periodo del Reporte:** \[Ej. Q1 2026 / Marzo 2026\]

**Responsable del Reporte:** \[Nombre del Tech Lead / Orquestador de Ingeniería\]

**Estado General del Ecosistema:** \[Saludable / En Riesgo / Crítico\]

## **1\. Resumen de Rendimiento Estratégico (Métricas DORA)**

Las métricas DORA son los pilares fundamentales para medir la velocidad de entrega y la estabilidad del sistema. Este apartado evalúa la madurez del ciclo de vida de desarrollo de software (SDLC).

| Métrica | Definición y Relevancia | Resultado Actual | Categoría de Desempeño |
| :---- | :---- | :---- | :---- |
| **Deployment Frequency (DF)** | **Velocidad:** Frecuencia de despliegues exitosos en producción. Un DF alto indica procesos de automatización robustos. | \[Ej. 12 veces/día\] | \[Elite / Alto / Medio\] |
| **Lead Time for Changes (LTTC)** | **Agilidad:** Tiempo desde el primer commit hasta que el código genera valor en producción. Mide la eficiencia del pipeline. | \[Ej. 4.5 horas\] | \[Elite / Alto / Medio\] |
| **Change Failure Rate (CFR)** | **Calidad:** Porcentaje de despliegues que resultan en fallos críticos, degradación o requieren rollback inmediato. | \[Ej. 1.2%\] | \[Elite / Alto / Medio\] |
| **Time to Restore Service (TTRS)** | **Resiliencia:** Tiempo medio que el equipo tarda en recuperarse de un incidente en producción tras su detección. | \[Ej. 28 min\] | \[Elite / Alto / Medio\] |

### **Análisis de Tendencias DORA**

* **Progreso vs Periodo Anterior:** \[Ej. El LTTC se redujo un 15% gracias a la paralelización de tests de integración\].
* **Implicaciones:** Una mejora en la frecuencia de despliegue sin un aumento en el CFR sugiere que nuestra automatización de QA está escalando correctamente.

## **2\. Indicadores de Calidad del Código y Deuda Técnica**

Métricas estáticas y dinámicas que garantizan la mantenibilidad a largo plazo y reducen la fricción para futuros desarrollos.

* **Cobertura de Tests (Code Coverage):** \[% Actual\] (Meta: \>85%).
  * *Nota:* No solo buscamos cobertura de líneas, sino cobertura de ramas lógicas en módulos críticos identificados en los ADRs.
* **Complejidad Ciclomática Media:** \[Valor\] (Meta: \<10 por función).
  * *Explicación:* Un valor alto indica funciones difíciles de testear y propensas a errores ocultos.
* **Code Churn (Rotación de Código):** \[% de archivos modificados frecuentemente\].
  * *Implicación:* Una alta rotación en archivos específicos suele indicar falta de modularidad o requisitos volátiles.
* **Deuda Técnica Identificada (Technical Debt):** \[Horas estimadas de refactorización / Story Points acumulados\].
  * *Categorización:* \[Crítica (Seguridad) / Operativa (Rendimiento) / Estética (Linter)\].
* **Vulnerabilidades de Seguridad (Ciberseguridad):**
  * **SAST (Estático):** \[Críticas: 0, Altas: X, Medias: Y\].
  * **SCA (Dependencias):** \[Ej. 2 librerías obsoletas con CVEs conocidos\].

## **3\. Salud del Sistema, Observabilidad y SRE**

Métricas de rendimiento operativo que afectan directamente la experiencia del usuario final. Basado en los "Four Golden Signals".

* **Disponibilidad (Uptime / SLA):** \[% Actual\] (Meta: 99.95%).
* **Latencia de Respuesta (P50, P95, P99):**
  * **P50 (Promedio):** \[ms\]
  * **P95 (Casos lentos):** \[ms\] (Meta: \<200ms).
  * **P99 (Casos críticos):** \[ms\]
* **Tasa de Errores (Error Rate):** \[% de peticiones fallidas (4xx/5xx)\].
* **Saturación y Consumo de Recursos:**
  * **CPU / Memoria:** \[% promedio de uso de clusters\].
  * **I/O de Disco y Red:** \[Velocidad de transferencia y latencia de DB\].
* **Estado de los SLOs (Service Level Objectives):** \[Ej. Cumpliendo el SLO de latencia en el 98% del tiempo\].

## **4\. Análisis de Cuellos de Botella y Gestión de Incidentes**

Espacio para el análisis narrativo y cualitativo de los bloqueos que impiden un flujo de trabajo óptimo.

### **4.1 Principales Bloqueos Operativos**

* **Bloqueo A:** \[Ej. Tiempo excesivo en revisiones de código manuales (PR Reviews) debido a desalineación horaria\].
* **Bloqueo B:** \[Ej. Inestabilidad en el entorno de Staging por colisión de datos de subagentes\].

### **4.2 Post-Mortem de Incidentes Críticos (Blameless Culture)**

* **Incidente \[ID-00X\]: \[Título del Incidente\]**
  * **Impacto:** \[Ej. 15% de los usuarios no pudieron finalizar pagos durante 20 minutos\].
  * **Causa Raíz (Root Cause):** \[Ej. Desajuste en el TTL de la caché de Redis tras un despliegue de configuración\].
  * **Acción Correctiva (Preventiva):** \[Ej. Implementación de validación sintáctica de archivos de configuración en el pipeline de CI\].
  * **Lecciones Aprendidas:** \[Ej. Necesidad de alertas predictivas sobre el consumo de memoria en Redis\].

## **5\. Estrategia de Mejora e Iniciativas (Próximo Periodo)**

Acciones concretas diseñadas para elevar el nivel de madurez de ingeniería basándose en los datos presentados.

1. \[ \] **Optimización del Pipeline de CI/CD:** Implementar cacheo de capas de Docker para reducir el LTTC en un 10%.
2. \[ \] **Campaña de Refactorización Crítica:** Atacar los 5 módulos con mayor complejidad ciclomática para reducir la tasa de regresiones.
3. \[ \] **Shift-Left Security:** Integrar escaneos de seguridad automáticos en cada commit para detectar secretos y vulnerabilidades antes de Staging.
4. \[ \] **Automatización de Observabilidad:** Configurar alertas de anomalías basadas en IA para detectar desviaciones en la latencia P99 antes de que afecten al SLA.

## **6\. Conclusiones y Visión del Tech Lead**

Resumen interpretativo sobre la evolución del equipo. ¿Estamos construyendo el software correcto de la manera correcta?

* **Evolución del Equipo:** \[Ej. El equipo ha adoptado con éxito el flujo de subagentes, liberando tiempo para diseño arquitectónico\].
* **Necesidades de Recursos:** \[Ej. Se requiere una actualización en la infraestructura de bases de datos para soportar el nuevo volumen de lectura esperado en el Q2\].
* **Mensaje Final:** Reflexión sobre la cultura de ingeniería y el alineamiento con el **PRD** original.

## **7\. Referencias, Dashboards y Trazabilidad**

* \[Enlace a Dashboard de Grafana / Datadog con métricas de tiempo real\].
* \[Enlace a Reporte de Cobertura de Código y Calidad Estática (SonarQube)\].
* \[Enlace a Repositorio de ADRs (Architectural Decision Records) del periodo\].
* \[Enlace a Historial de RFCs revisadas\].

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

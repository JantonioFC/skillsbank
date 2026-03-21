---
id: doc-infra-cicd-template
name: doc-infra-cicd-template
description: Genera especificaciones de infraestructura y pipelines CI/CD.
category: documentacion-de-codigo
risk: safe
source: personal
date_added: '2026-03-11'
license: MIT
---



# doc-infra-cicd-template

Genera una especificacion de infraestructura y pipeline CI/CD cuando el usuario necesita documentar la configuracion de entornos, despliegues o pipelines.

## Cuando usar esta skill
- Cuando el usuario necesita documentar la estrategia de entornos, redes y seguridad de un proyecto
- Cuando se requiere definir un pipeline de CI/CD con sus fases de integracion y despliegue continuo
- Cuando se necesita especificar estrategias de despliegue seguro, IaC, gestion de secretos u observabilidad

## Instrucciones
1. Analizar el contexto del proyecto actual (stack, arquitectura, equipo)
2. Rellenar la plantilla adaptandola al contexto especifico
3. Usar espanol para el contenido, manteniendo terminos tecnicos en ingles donde corresponda
4. No dejar secciones vacias — si algo no aplica, indicar "N/A" con justificacion
5. Preguntar al usuario si hay secciones que requieren decisiones pendientes

## Plantilla

# **Plantilla: Especificacion de Infraestructura y Pipeline CI/CD**

**Proyecto:** [Nombre del Proyecto]

**Referencia RFC:** [Enlace a la propuesta tecnica - plantilla_rfc.md]

**Estado:** [Borrador / Definido / Implementado / Auditado]

**Responsable DevOps:** [Nombre del ingeniero / Agente de Infraestructura]

**Fecha de Revision:** [Fecha Actual]

## **1. Estrategia de Entornos y Aislamiento Multinivel**

Esta seccion define la topologia, el proposito y las restricciones de los entornos necesarios para el ciclo de vida del software. La premisa fundamental es la **Paridad de Entornos**: cada etapa debe ser una replica funcional lo mas exacta posible del entorno productivo para mitigar el riesgo de errores imprevistos derivados de la deriva de configuracion ("Configuration Drift").

### **1.1 Definicion y Proposito Detallado de los Entornos**

* **Local (Dev):** Entorno de desarrollo individual. Se basa obligatoriamente en contenedores (Docker/Podman) y docker-compose para garantizar que el runtime, las versiones de base de datos y las dependencias de sistema sean identicas entre todos los desarrolladores. Esto elimina el clasico problema de "en mi maquina funciona".
* **Sandbox / Feature Environments (Ephemeral):** Entornos creados dinamicamente mediante el pipeline (ej. usando Kubernetes Namespaces o Vercel Previews) para cada rama de funcionalidad (*branch*). Permiten la validacion aislada y el QA temprano antes de la integracion en la rama principal. Se destruyen automaticamente al cerrar el Pull Request para optimizar costos.
* **Staging / Pre-Prod (QA):** Replica exacta de produccion en terminos de arquitectura de red, tamano de instancias y cuotas de recursos. Utiliza datos anonimizados o sinteticos mediante procesos de *masking* para garantizar la privacidad mientras se permiten pruebas de carga, pruebas de penetracion y la validacion final de los criterios BDD.
* **Produccion (Prod):** Entorno de mision critica donde reside el valor de negocio. Acceso restringido bajo el principio de **Privilegio Minimo** (Least Privilege). Implementa alta disponibilidad multizona (Multi-AZ), autoreparacion de nodos y monitorizacion proactiva con alertas inteligentes.

### **1.2 Aislamiento de Red y Seguridad Perimetral**

* **VPC y Segmentacion de Capas:** Uso de Virtual Private Clouds con segmentacion estricta:
  * **Subredes Publicas:** Solo para balanceadores de carga (ALB/NLB) y Gateways de aplicaciones.
  * **Subredes Privadas:** Para la logica de negocio (App Tier). Sin acceso directo desde Internet.
  * **Subredes de Datos:** Exclusivas para bases de datos y sistemas de cache, con acceso restringido unicamente desde la capa de aplicacion.
* **Zero Trust Architecture:** Implementacion de Service Meshes (ej. Istio, Linkerd) para mTLS (Mutual TLS) obligatorio entre microservicios, asegurando que cada comunicacion interna este cifrada e identificada.
* **Estrategia de Egreso:** Uso de NAT Gateways y firewalls de capa 7 para restringir que los servicios internos solo se comuniquen con dominios externos autorizados (lista blanca), mitigando riesgos de exfiltracion de datos.

## **2. Definicion del Pipeline de CI/CD: La Tuberia de Entrega Continua**

El pipeline es el motor de confianza que garantiza que solo el codigo que supera todos los umbrales de calidad tecnica y de seguridad llegue a manos del usuario de forma automatica y predecible.

### **2.1 Fase de Integracion Continua (CI): Validacion y Construccion**

Ejecucion disparada por cada *Commit* o *Pull Request*:

1. **Analisis Estatico y Calidad (Linting/SAST):** Verificacion de estandares de estilo y deteccion de vulnerabilidades en el codigo fuente (ej. SonarQube, Snyk). No se permiten "smells" de severidad alta ni brechas de seguridad conocidas.
2. **Secret Scanning:** Escaneo preventivo de la historia del commit para detectar tokens de nube, llaves de API o certificados (ej. Gitleaks, TruffleHog). Un hallazgo bloquea inmediatamente el build.
3. **Software Composition Analysis (SCA):** Analisis de la cadena de suministro de software para detectar librerias de terceros con vulnerabilidades (CVEs) o licencias incompatibles.
4. **Pruebas Unitarias y TDD:** Ejecucion de la suite definida en plantilla_tdd_unit_testing.md. Se requiere un paso de exito del 100% y cumplimiento de la cuota de cobertura minima.
5. **Build de Artefactos Inmutables:** Creacion de imagenes de contenedor (Docker) etiquetadas con el hash del commit (SHA). Una vez generada, la imagen se firma digitalmente y no se modifica; solo se promociona entre entornos.

### **2.2 Fase de Despliegue Continuo (CD) y Orquestacion**

1. **Promocion Automatica a Staging:** Tras el merge exitoso en la rama main.
2. **Pruebas de Integracion y Humo (Smoke Tests):** Validacion automatizada de las rutas criticas del sistema (ej. login, checkout, salud de la base de datos) inmediatamente despues del despliegue en el entorno de pruebas.
3. **Infrastructure Drift Detection:** Antes de aplicar cambios, el pipeline verifica si la infraestructura real ha sido modificada manualmente, forzando la reconciliacion con el codigo (GitOps).
4. **Aprobacion Manual (Gatekeeping):** El paso a Produccion requiere una firma digital de al menos dos responsables (Tech Lead y QA) basada en el exito de las pruebas en Staging.

## **3. Estrategias Avanzadas de Despliegue Seguro**

El objetivo primordial es reducir el "Radio de Explosion" (*Blast Radius*) de cualquier fallo en una nueva version, garantizando la continuidad del negocio.

* **Blue-Green Deployment:** Se mantienen dos entornos identicos. El trafico se conmuta al 100% mediante el balanceador de carga solo cuando el nuevo entorno ("Green") ha pasado todas las pruebas de salud. Permite un *rollback* instantaneo si se detecta una degradacion.
* **Canary Release:** El trafico se desvia gradualmente hacia la nueva version (ej. 1%, 5%, 25%, 100%). Se monitorean metricas de negocio y errores en tiempo real; si la tasa de error 5xx aumenta, el *rollback* se dispara automaticamente.
* **Feature Flags (Toggles):** Permite desacoplar el despliegue del codigo de la activacion de la funcionalidad. El codigo vive en produccion pero permanece inactivo hasta que el Product Owner decide encenderlo para un segmento de usuarios.
* **Estrategia de Base de Datos (Expand & Contract):** Implementacion de migraciones de esquema compatibles hacia atras. La base de datos siempre debe soportar la version de codigo N y N-1 simultaneamente para permitir reversiones de codigo sin romper la persistencia.

## **4. Infraestructura como Codigo (IaC) y GitOps**

La infraestructura se trata con la misma rigurosidad, versionado y procesos de revision que el codigo de la aplicacion.

* **Estado Declarativo (Declarative State):** Uso de herramientas como Terraform, Pulumi o Crossplane para definir recursos. El archivo de estado (*state file*) debe estar en un almacenamiento remoto seguro con bloqueo de escritura (*state locking*).
* **GitOps como Unica Fuente de Verdad:** Cualquier cambio en la nube debe realizarse a traves de un Pull Request en el repositorio de infraestructura. Se prohiben terminantemente los cambios manuales por consola ("ClickOps").
* **Inmutabilidad de Infraestructura:** No se reparan servidores ni configuraciones en vivo; se destruyen y se vuelven a crear a partir de la nueva definicion de codigo.

## **5. Gobernanza de Secretos y Configuracion en Runtime**

* **Separacion de Configuracion y Secretos:** Los parametros de entorno (nombres de colas, URLs) viven en el codigo o ConfigMaps; las credenciales sensibles viven en una boveda cifrada.
* **Inyeccion Dinamica:** Uso de proveedores de secretos (AWS Secrets Manager, HashiCorp Vault) que inyectan las credenciales directamente en la memoria del proceso o mediante volumenes efimeros en Kubernetes. Nunca se persisten en archivos .env ni en variables de entorno permanentes.
* **Rotacion Automatica de Credenciales:** Configuracion de politicas para que las contrasenas de base de datos y llaves de acceso roten cada 30-90 dias sin intervencion humana ni reinicios forzados.

## **6. Observabilidad Total: Los Tres Pilares Post-Despliegue**

Un sistema no se considera "desplegado" hasta que es plenamente observable y medible.

* **Metricas (Metricas de Salud):** Implementacion de los *Four Golden Signals*:
  * **Latencia:** Tiempo que tarda en procesar una peticion.
  * **Trafico:** Demanda real sobre el sistema.
  * **Errores:** Tasa de peticiones fallidas explicitas o implicitas.
  * **Saturacion:** Que tan "llenos" estan los recursos (CPU, Memoria, IOPS).
* **Logs Estructurados y Centralizados:** Recoleccion de logs en formato JSON para facilitar su indexacion y busqueda. Cada log debe incluir un correlation-id para trazabilidad.
* **Trazabilidad Distribuida (Distributed Tracing):** Uso de OpenTelemetry para seguir el camino de una peticion a traves de multiples microservicios, identificando cuellos de botella exactos.
* **SLOs y SLIs (Service Level Objectives):** Definicion clara de que constituye un sistema "sano". Si el presupuesto de error (*Error Budget*) se agota, el pipeline de CD se bloquea para priorizar la estabilidad sobre las nuevas funciones.

## **7. Protocolo de Rollback Automatico y Contingencia**

Plan de accion ante la deteccion de anomalias post-despliegue que superen los umbrales de tolerancia.

1. **Deteccion Basada en Umbrales:** Si el *error rate* aumenta un 10% respecto a la linea base o la latencia P95 sube de 500ms, el sistema inicia el retorno a la version anterior de forma autonoma.
2. **Procedimiento de Datos:** Las migraciones deben ser idempotentes y reversibles. En caso de cambios destructivos en el esquema, debe existir un proceso de restauracion de *snapshots* probado y documentado.
3. **Comunicacion de Incidente:** Notificacion automatica a canales de operaciones (Slack/PagerDuty) detallando el motivo del rollback y la version afectada para el analisis post-mortem.

## **8. Guia de Automatizacion para la IA (Agent-DevOps)**

Directrices criticas para que los agentes de IA mantengan la integridad y seguridad del sistema:

1. **Idempotencia Obligatoria:** Todos los scripts de configuracion (Ansible, Terraform) deben poder ejecutarse N veces produciendo el mismo resultado final sin efectos secundarios.
2. **Principio de Inmutabilidad:** No instales paquetes en servidores en ejecucion; genera una nueva imagen de contenedor o una nueva AMI (Amazon Machine Image).
3. **Seguridad por Defecto:** Cada nuevo recurso (Bucket S3, Base de Datos RDS) debe crearse con cifrado en reposo activado y sin acceso publico de forma predeterminada.
4. **Etiquetado y Control de Costos:** Cada recurso debe incluir etiquetas (tags) obligatorias de: Project, Environment, Owner y CostCenter para auditoria y optimizacion financiera automatica.

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

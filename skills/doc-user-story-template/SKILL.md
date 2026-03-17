---
id: doc-user-story-template
name: doc-user-story-template
description: Genera historias de usuario estructuradas con criterios de aceptación.
category: documentacion-de-codigo
risk: safe
source: personal
date_added: '2026-03-11'
---


# doc-user-story-template

Genera Historias de Usuario (User Stories) con criterios de aceptacion cuando el usuario necesita definir requisitos desde la perspectiva del usuario final.

## Cuando usar esta skill
- Cuando el usuario necesita escribir historias de usuario con formato COMO/QUIERO/PARA y criterios de aceptacion formales
- Cuando se requiere documentar requisitos funcionales con escenarios de aceptacion en formato Dado/Cuando/Entonces
- Cuando se necesita definir una historia con analisis INVEST, detalles tecnicos, riesgos y criterios DoR/DoD

## Instrucciones
1. Analizar el contexto del proyecto actual (stack, arquitectura, equipo)
2. Rellenar la plantilla adaptandola al contexto especifico
3. Usar espanol para el contenido, manteniendo terminos tecnicos en ingles donde corresponda
4. No dejar secciones vacias — si algo no aplica, indicar "N/A" con justificacion
5. Preguntar al usuario si hay secciones que requieren decisiones pendientes

## Plantilla

# **Plantilla: Historias de Usuario (User Stories)**

**Proyecto:** [Nombre del Proyecto]

**Referencia PRD / Epica:** [Enlace al Documento de Requisitos o Identificador de la Epica]

**Estado Actual:** [Backlog / En Refinamiento / Lista para Dev / En Desarrollo / QA / Terminada / Bloqueada]

## **1. Identificacion y Clasificacion de la Historia**

* **ID Unico:** US-[Numero Correlativo] (Ej: US-101)
* **Titulo Descriptivo:** [Accion clara + Objeto sobre el que recae]. *Evitar titulos vagos como "Login", preferir "Autenticacion de usuario mediante proveedor externo".*
* **Prioridad de Negocio:** [Critica (P0) / Alta (P1) / Media (P2) / Deseable (P3)]. *Basado en el valor que aporta al usuario final.*
* **Estimacion de Esfuerzo:** [Puntos de Historia (Fibonacci) / Horas Reales / T-Shirt Size]. *La estimacion debe reflejar la complejidad, la incertidumbre y el esfuerzo requerido.*
* **Etiquetas / Modulos:** [Ej: Auth, Frontend, Database, Billing].

## **2. Descripcion de la Historia (El Corazon del Valor)**

Utiliza el formato narrativo estandar para asegurar que el equipo entienda quien es el beneficiario y cual es el resultado esperado.

**COMO** [Rol del usuario / Persona definida en el PRD]

**QUIERO** [Realizar una accion especifica o disponer de una funcionalidad]

**PARA** [Obtener un beneficio tangible, resolver un punto de dolor o generar valor de negocio]

### **Analisis de Valor (INVEST)**

Para que esta historia sea de alta calidad, debe cumplir con los criterios **INVEST**:

* **Independiente:** Se puede desarrollar sin depender de otras historias no terminadas?
* **Negociable:** Permite el dialogo sobre como implementarla o es un contrato cerrado?
* **Valiosa:** El "Para..." justifica el costo de desarrollo?
* **Estimable:** El equipo tiene suficiente informacion para ponerle un peso?
* **Small (Pequena):** Se puede completar en un solo sprint/ciclo?
* **Testable:** Existen criterios claros para decir "funciona"?
* **Contexto Adicional y Justificacion:** [Explica el "porque" profundo. Es una regulacion legal? Es una peticion frecuente en soporte? Que sucede si no la hacemos ahora?].

## **3. Criterios de Aceptacion (AC) - Especificacion Ejecutable**

Define los limites de la historia de forma inequivoca. Estos criterios se transformaran en el plan de pruebas del equipo de QA y en las instrucciones para la IA.

### **Escenario 1: [Camino Feliz / Happy Path Principal]**

* **DADO QUE** [El estado inicial del sistema, ej: "el usuario esta en la pagina de recuperacion"]
* **CUANDO** [El usuario realiza la accion, ej: "introduce un email valido y pulsa enviar"]
* **ENTONCES** [Resultado observable, ej: "el sistema envia un token y muestra mensaje de exito"]
* **Y** [Condicion adicional, ej: "el token expira en exactamente 15 minutos"]

### **Escenario 2: [Manejo de Errores / Edge Cases]**

* **DADO QUE** [Condicion de fallo, ej: "el email introducido no existe en la base de datos"]
* **CUANDO** [El usuario pulsa el boton de accion]
* **ENTONCES** [Resultado de seguridad/UX, ej: "el sistema muestra el mismo mensaje de exito por seguridad pero no envia nada"]

### **Escenario 3: [Criterios No Funcionales Especificos]**

* **DADO QUE** [Contexto de carga]
* **CUANDO** [Se procesa la solicitud]
* **ENTONCES** [Metrica de rendimiento, ej: "la respuesta de la API no debe superar los 200ms"]

## **4. Detalles Tecnicos, Diseno y Contratos de Datos**

Especificaciones granulares para el equipo de implementacion y subagentes de codificacion.

* **UI/UX e Interaccion:** [Enlace a Figma/Sketch]. *Nota: Ver seccion de micro-interacciones para estados de carga y errores.*
* **Esquema de Datos / Contrato API:**
  * **Endpoint:** PUT /api/v1/user/profile
  * **Payload de Entrada:** { "id": UUID, "bio": String(max 500), "avatar_url": URL }
  * **Codigos de Respuesta:** 200 OK, 400 Bad Request, 401 Unauthorized.
* **Logica de Negocio Compleja:** [Detalla algoritmos. Ej: "El calculo del descuento sigue la formula X basada en la antiguedad del usuario"].
* **Seguridad:** [Ej: El endpoint debe requerir el scope user:write y validar el JWT].

## **5. Riesgos, Dependencias y Bloqueos**

* **Bloqueado por:** [ID de US o Tarea tecnica previa necesaria].
* **Dependencias de Infraestructura:** [Ej: Necesitamos habilitar el bucket de S3 antes de implementar la subida de archivos].
* **Riesgos Identificados:** [Ej: Posible colision de datos si dos usuarios editan el perfil simultaneamente. Se requiere manejo de concurrencia optimista].

## **6. Gobernanza de Calidad: DoR & DoD**

### **Definition of Ready (DoR) - Filtro de Entrada**

* [ ] La historia es pequena y respeta el principio **INVEST**.
* [ ] El valor de negocio esta validado por el Product Owner.
* [ ] Los disenos estan finalizados y son accesibles para el equipo.
* [ ] El equipo tecnico ha realizado el "grooming" y no tiene dudas sobre la implementacion.

### **Definition of Done (DoD) - Filtro de Salida**

* [ ] El codigo ha pasado el analisis estatico (Linting) y revisiones de seguridad.
* [ ] Todos los Criterios de Aceptacion (AC) han sido validados con tests automatizados.
* [ ] La cobertura de tests unitarios e integracion es igual o superior al 85%.
* [ ] La documentacion del codigo y los endpoints (Swagger) esta actualizada.
* [ ] El cambio ha sido desplegado exitosamente en el entorno de Staging/QA.
* [ ] Se han verificado criterios de accesibilidad (A11y) y rendimiento basico.

## **7. Notas de Colaboracion y Trazabilidad**

* **Log de Decisiones:** [Espacio para anotar por que se cambio un criterio de aceptacion durante el desarrollo].
* **Historial de Cambios:**
  * *YYYY-MM-DD:* [Descripcion del cambio] - [Autor].
* **Post-Mortem / Lecciones Aprendidas:** [Opcional: Notas tras el despliegue sobre dificultades encontradas].

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

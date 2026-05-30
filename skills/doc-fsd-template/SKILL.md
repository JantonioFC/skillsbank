---
id: doc-fsd-template
name: doc-fsd-template
description: Genera documentos FSD (Functional Specification Document) con especificaciones
  funcionales detalladas.
category: documentacion-de-codigo
risk: safe
source: personal
date_added: '2026-03-11'
license: MIT
---
# doc-fsd-template

Genera una Especificacion Funcional Detallada (FSD) cuando el usuario necesita documentar el comportamiento exacto y la logica de un sistema o modulo.

## Cuando usar esta skill
- Cuando el usuario necesita crear un documento que detalle la logica exacta, reglas de validacion y respuestas del sistema ante cada interaccion
- Cuando se requiere un puente operativo entre la vision de negocio (PRD) y la arquitectura tecnica (RFC) para eliminar ambiguedad en la fase de construccion
- Cuando se necesita especificar modulos, maquinas de estado, contratos de datos o casos de borde de una funcionalidad

## Instrucciones
1. Analizar el contexto del proyecto actual (stack, arquitectura, equipo)
2. Rellenar la plantilla adaptandola al contexto especifico
3. Usar espanol para el contenido, manteniendo terminos tecnicos en ingles donde corresponda
4. No dejar secciones vacias — si algo no aplica, indicar "N/A" con justificacion
5. Preguntar al usuario si hay secciones que requieren decisiones pendientes

## Plantilla

# **FSD: Especificacion Funcional Detallada**

**Proyecto:** [Nombre del Proyecto]

**Referencia PRD:** [Enlace a plantilla_prd.md]

**Referencia RFC:** [Enlace a plantilla_rfc.md]

**Version:** [X.X.X]

**Estado:** [Borrador / Validado / En Implementacion]

**Ultima Revision:** [Fecha]

## **1. Alcance y Objetivos de la Especificacion**

Este documento constituye la "Fuente Unica de la Verdad" (SSOT) sobre el comportamiento esperado del sistema. Mientras que el PRD define la vision de negocio y la RFC propone una arquitectura tecnica, la FSD actua como el puente operativo, detallando la logica exacta, las reglas de validacion y las respuestas del sistema ante cada interaccion.

* **Objetivo Primario:** Eliminar la ambiguedad en la fase de construccion, reduciendo el ciclo de feedback entre desarrollo y producto.
* **Mitigacion de Riesgos:** Identificar conflictos logicos o dependencias no resueltas antes de la escritura del codigo.
* **Audiencia:** Desarrolladores, Ingenieros de QA, Disenadores de UX y Agentes de IA (quienes usaran este documento como su manual de instrucciones de codificacion).

### **1.1 No-Objetivos (Fuera de Alcance Funcional)**

Es tan importante definir lo que el sistema hace como lo que **no** hace en esta fase:

* [Ej. No se contempla la integracion con sistemas de lealtad en esta iteracion].
* [Ej. No se requiere soporte para dispositivos moviles con resolucion inferior a 320px].

## **2. Arquitectura Funcional y Flujos de Usuario**

Describe la jerarquia de funciones y la topologia de la experiencia del usuario o del flujo sistemico.

### **2.1 Mapa de Funcionalidades (Feature Map)**

Desglose jerarquico de los modulos. Se debe representar visualmente como se agrupan las capacidades (ej. Gestion de Usuarios > Perfiles > Preferencias de Privacidad).

### **2.2 Diagramas de Flujo de Datos (DFD) y Navegacion**

Representacion visual del movimiento de la informacion. Se recomienda distinguir entre:

* **Nivel 0:** Flujo macro entre el usuario y el sistema global.
* **Nivel 1:** Interacciones detalladas entre microservicios o modulos internos.

## **3. Especificacion Detallada de Modulos**

Cada componente debe describirse con un nivel de detalle que permita su implementacion inmediata.

### **3.1 Modulo: [Nombre del Modulo - Ej. Motor de Pagos Sincronico]**

* **Descripcion Operativa:** Define la logica de procesamiento para transacciones en tiempo real.
* **Entradas (Inputs):**
  * Atributos: [Ej. card_token, transaction_amount, currency_code].
  * Origen: [Ej. Formulario de Checkout / API Externa].
* **Procesamiento y Reglas de Negocio:**
  1. **Validacion de Idempotencia:** El sistema debe verificar el request_id para evitar cobros duplicados en reintentos.
  2. **Validacion Sintactica:** Comprobar que el monto sea positivo y la moneda este soportada.
  3. **Logica de Redondeo:** Aplicar redondeo simetrico segun el estandar bancario definido en el ADR-004.
  4. **Verificacion de Fraude:** Consulta sincronica al servicio de riesgo con un timeout de 2s.
* **Efectos Secundarios (Side Effects):** [Ej. Emision de evento PAYMENT_SUCCESS, actualizacion de inventario].
* **Salidas (Outputs):** [Ej. transaction_id, codigo de respuesta de pasarela, factura en formato PDF].

## **4. Maquinas de Estado e Interacciones Criticas**

Para sistemas transaccionales o complejos, los estados son la salvaguarda contra la corrupcion de datos.

### **4.1 Ciclo de Vida y Transiciones**

* **Definicion de Estados:**
  * **CREADO:** El objeto existe pero no ha sido procesado.
  * **PENDIENTE:** En espera de confirmacion de un tercero (webhook).
  * **FALLIDO:** Estado terminal tras agotar reintentos.
* **Matriz de Transiciones Prohibidas:** [Ej. Un objeto en estado 'COMPLETADO' nunca puede volver a 'PENDIENTE'].

### **4.2 Logica de Timeouts y Caducidad**

Detallar que sucede cuando un proceso queda en el limbo (Ej. "Si una orden permanece en 'PENDIENTE' mas de 15 minutos, disparar el worker de cancelacion automatica").

## **5. Contratos de Datos y Definicion de Interfaces**

Especificacion tecnica de la comunicacion inter-modulos.

### **5.1 Especificacion de la Interfaz (API/Eventos)**

* **Contrato de Entrada:** Esquema JSON/Protobuf detallado con tipos de datos y restricciones (min/max, regex).
* **Encabezados Requeridos (Headers):** [Ej. Authorization: Bearer, X-Correlation-ID].
* **Politicas de Rate Limiting Funcional:** Cuantas veces puede un usuario intentar esta accion por minuto antes de bloquear la funcionalidad?

## **6. Gestion de Casos de Borde (Edge Cases) y Resiliencia**

Esta seccion es el "seguro de vida" del sistema ante fallos imprevistos.

### **6.1 Escenarios de Error y Recuperacion**

* **Fallo de Dependencia Critica:** Si el servicio de impuestos no responde, el sistema debe usar una tabla de tasas "fallback" preconfigurada y marcar la transaccion como "requiere auditoria".
* **Manejo de Concurrencia (Race Conditions):** Implementar bloqueo optimista usando un campo version_id. Si dos agentes intentan editar el mismo registro, el segundo debe recibir un error 409 (Conflict).
* **Degradacion Elegante (Graceful Degradation):** Si el motor de busqueda avanzado falla, el sistema debe ofrecer una busqueda simple por palabra clave sin filtros.

## **7. Requisitos No Funcionales (Especificacion Tecnica)**

* **Rendimiento Percibido:** El tiempo de respuesta de la UI debe ser inferior a 200ms para acciones de escritura (confirmacion inmediata visual).
* **Trazabilidad y Observabilidad:** Cada transaccion debe inyectar el trace_id en todos los logs de los microservicios involucrados.
* **Seguridad Funcional:** Los datos sensibles (PAN de tarjeta) no deben ser visibles ni siquiera en los logs de depuracion (Mascara de datos).

## **8. Internacionalizacion, Localizacion y Contexto Global**

* **Soporte de Idiomas:** Estrategia de carga dinamica de etiquetas. Soporte para idiomas RTL (derecha a izquierda) si aplica.
* **Manejo de Husos Horarios (Timezones):** Persistencia obligatoria en UTC. Visualizacion basada en el offset del cliente, exceptuando fechas legales (que se rigen por la sede de la empresa).
* **Formato de Valores:** Comas para decimales o puntos segun el pais detectado en el perfil del usuario.

## **9. Criterios de Validacion (Gating Funcional y UAT)**

Define cuando una funcionalidad se considera "lista para el usuario".

* [ ] **Validacion de Datos:** El sistema rechaza correctamente payloads incompletos.
* [ ] **Escenario de Reintento:** Se verifica que el *exponential backoff* funciona tras un error 503.
* [ ] **Integridad de Datos:** Tras una cancelacion, los saldos en la DB coinciden exactamente con el estado inicial.
* [ ] **Aceptacion de UX:** El flujo de navegacion coincide al 100% con los mockups aprobados.

## **10. Apendices y Referencias Tecnicas**

* **Glosario de Dominio:** Definicion de conceptos de negocio (Ej. Que es un "Usuario Premium" vs un "Usuario Activo"?).
* **Librerias y SDKs:** Versiones especificas de dependencias mencionadas en la RFC que tienen impacto funcional.
* **Historial de Cambios Funcionales:** Registro de modificaciones en la logica que afectan al desarrollo en curso.

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

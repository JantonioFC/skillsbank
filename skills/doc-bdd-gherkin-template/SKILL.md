---
id: doc-bdd-gherkin-template
name: doc-bdd-gherkin-template
description: Genera especificaciones BDD en formato Gherkin para definir comportamiento
  esperado del sistema.
category: documentacion-de-codigo
risk: safe
source: personal
date_added: '2026-03-11'
license: MIT
---
# doc-bdd-gherkin-template

Genera una especificacion BDD con escenarios Gherkin cuando el usuario necesita definir comportamiento esperado del sistema.

## Cuando usar esta skill
- Cuando el usuario necesita escribir especificaciones de comportamiento (BDD) o escenarios Gherkin para una funcionalidad
- Cuando se requiere definir criterios de aceptacion formales con formato Dado/Cuando/Entonces
- Cuando se necesita crear pruebas basadas en datos (Scenario Outlines) o documentar casos de borde

## Instrucciones
1. Analizar el contexto del proyecto actual (stack, arquitectura, equipo)
2. Rellenar la plantilla adaptandola al contexto especifico
3. Usar espanol para el contenido, manteniendo terminos tecnicos en ingles donde corresponda
4. No dejar secciones vacias — si algo no aplica, indicar "N/A" con justificacion
5. Preguntar al usuario si hay secciones que requieren decisiones pendientes

## Plantilla

# **Plantilla: Especificacion BDD (Escenarios Gherkin)**

**Proyecto:** [Nombre del Proyecto]

**Referencia FSD:** [Enlace a la Especificacion Funcional Detallada - plantilla_fsd.md]

**Referencia US:** [ID de la Historia de Usuario vinculada, ej. US-123]

**Estado:** [Borrador / Refinado / En Automatizacion / Automatizado]

**Version:** [X.X.X]

## **1. Definicion de la Funcionalidad (Feature)**

Esta seccion define el "contrato" de comportamiento. Describe la capacidad del sistema de forma narrativa, centrada exclusivamente en el valor que recibe el usuario o el negocio, evitando detalles tecnicos de implementacion en este nivel.

**Funcionalidad:** [Titulo de la funcionalidad - Ej. Validacion y Aplicacion de Cupones de Descuento]

**COMO** [Rol del usuario, ej. Cliente Registrado]

**QUIERO** [Accion tecnica, ej. ingresar un codigo promocional en mi carrito]

**PARA** [Beneficio de negocio, ej. obtener un descuento en el precio final de mi compra]

### **1.1 Reglas de Negocio (Business Rules)**

Las reglas de negocio son las restricciones logicas que gobiernan la funcionalidad. Listarlas aqui ayuda a los desarrolladores y a la IA a entender los limites del sistema antes de leer los escenarios.

* **Regla 1 (Vigencia):** Un cupon solo es aplicable si la fecha actual se encuentra dentro del rango fecha_inicio y fecha_fin.
* **Regla 2 (Limites):** El descuento total aplicado no puede superar el 50% del subtotal del carrito para evitar perdidas operativas.
* **Regla 3 (Unicidad):** No se pueden combinar dos cupones de la misma categoria en una sola transaccion, a menos que se especifique explicitamente como "Acumulable".
* **Regla 4 (Monto Minimo):** Algunos cupones requieren un subtotal_minimo antes de poder ser activados.

## **2. Contexto General (Background)**

El bloque Background define el estado inicial del sistema que es comun a todos los escenarios de este archivo. Se utiliza para evitar la repeticion de los mismos pasos de configuracion en cada escenario individual, manteniendo la especificacion limpia y legible.

**Contexto:**

* **DADO QUE** el sistema tiene cargado el catalogo de productos actualizado.
* **Y** el usuario ha iniciado sesion con una cuenta valida y activa.
* **Y** el carrito de compras contiene al menos un articulo que no este en oferta previa.
* **Y** el servicio de validacion de pagos esta en estado "Disponible".

## **3. Escenarios de Comportamiento (Scenarios)**

Los escenarios deben describir el comportamiento desde la perspectiva del usuario, utilizando el formato **Dado/Cuando/Entonces**.

### **Escenario 1: Aplicacion exitosa de un cupon porcentual (Camino Feliz)**

Este escenario valida que el flujo principal de exito funciona perfectamente cuando se cumplen todas las condiciones ideales.

* **DADO QUE** existe un cupon activo llamado "PROMO10" con un 10% de descuento de tipo porcentual.
* **Y** el cupon tiene un limite de uso de 1 vez por usuario.
* **CUANDO** el usuario ingresa el codigo "PROMO10" en el campo de cupones de la pantalla de Checkout.
* **Y** pulsa el boton "Aplicar Cupon".
* **ENTONCES** el sistema debe aplicar una deduccion del 10% sobre el subtotal del carrito.
* **Y** el desglose de precios debe mostrar la linea "-$ [valor_descuento] (PROMO10)".
* **Y** debe mostrar el mensaje de confirmacion: "Felicidades! Tu descuento del 10% ha sido aplicado".

### **Escenario 2: Intento de uso de un cupon expirado (Manejo de Error de Negocio)**

Este escenario valida que el sistema impida acciones que violen las reglas de negocio y proporcione retroalimentacion util.

* **DADO QUE** existe un cupon llamado "VERANO2023" cuya fecha de expiracion fue hace mas de 30 dias.
* **CUANDO** el usuario intenta aplicar el codigo "VERANO2023".
* **ENTONCES** el sistema no debe realizar ninguna modificacion en el total del carrito.
* **Y** el campo de entrada debe resaltarse en color rojo de error.
* **Y** debe mostrar el mensaje de error: "Lo sentimos, este codigo promocional ya no es valido".

### **Escenario 3: Aplicacion de cupon con monto minimo no alcanzado**

* **DADO QUE** existe un cupon "MIN50" que otorga $10 de descuento para compras mayores a $50.
* **Y** el carrito del usuario tiene un subtotal de $35.
* **CUANDO** el usuario aplica el cupon "MIN50".
* **ENTONCES** el sistema debe rechazar el cupon.
* **Y** debe mostrar el mensaje: "Faltan $15 mas en tu carrito para poder usar este cupon".

## **4. Pruebas Basadas en Datos (Scenario Outlines)**

El Scenario Outline permite ejecutar la misma logica de prueba contra multiples conjuntos de datos. Es ideal para validar tablas de limites, categorias o reglas complejas sin escribir diez escenarios casi identicos.

**Esquema del Escenario: Validacion de limites de descuento por categoria de producto**

* **DADO QUE** el usuario tiene productos de la categoria "<categoria>" en su carrito.
* **Y** el subtotal de esos productos es de "<monto_base>".
* **CUANDO** se intenta aplicar un cupon global del "<descuento>".
* **ENTONCES** el estado resultante debe ser "<resultado>".
* **Y** el total final debe ser "<total_final>".

| categoria | monto_base | descuento | resultado | total_final | motivo |
| :---- | :---- | :---- | :---- | :---- | :---- |
| Electronica | $100.00 | 10% | Aceptado | $90.00 | Dentro del margen permitido |
| Electronica | $100.00 | 60% | Rechazado | $100.00 | Supera el limite de categoria |
| Ropa | $50.00 | 50% | Aceptado | $25.00 | Limite maximo exacto |
| Libros | $20.00 | 20% | Aceptado | $16.00 | Categoria sin restricciones |
| Perecederos | $10.00 | 5% | Rechazado | $10.00 | Categoria excluida de promociones |

## **5. Casos de Borde y Condiciones de Error Tecnicos**

Estos escenarios estan disenados para probar la resiliencia del software ante fallos de infraestructura o situaciones tecnicas extremas (Edge Cases).

### **Escenario: Perdida de conexion con el microservicio de validacion**

Este escenario asegura que el sistema falle con gracia y no deje la interfaz bloqueada o en un estado inconsistente.

* **DADO QUE** el servicio externo de validacion de cupones (API) devuelve un error de timeout o 503.
* **CUANDO** el usuario solicita aplicar un cupon legitimo.
* **ENTONCES** el sistema debe realizar hasta 2 reintentos automaticos de forma silenciosa.
* **Y** si persiste el fallo, debe informar al usuario mediante un modal: "Estamos experimentando dificultades tecnicas. No podemos validar tu cupon en este momento. Por favor, intentalo de nuevo en unos minutos".
* **Y** debe registrar el error en el sistema de logs con el correlation_id de la sesion.

## **6. Etiquetas y Metadatos (Tags)**

Las etiquetas permiten filtrar la ejecucion de pruebas. Una buena estrategia de tags facilita el CI/CD (Integracion Continua).

* @regresion: Escenarios vitales que deben ejecutarse en cada despliegue para evitar regresiones.
* @humo (Smoke Test): Pruebas rapidas de conectividad y flujos basicos.
* @ui: Escenarios que requieren un navegador y validacion de elementos visuales (lento).
* @api: Escenarios que pueden validarse directamente mediante llamadas a servicios (rapido).
* @critico: Escenarios que afectan directamente a la facturacion o seguridad.
* @modulo_checkout: Identificador del area funcional para pruebas focalizadas.

## **7. Guia de Implementacion para Desarrolladores e IA**

Instrucciones criticas para transformar este lenguaje natural en codigo de automatizacion (Step Definitions).

* **Mapeo de Parametros:** Utilizar expresiones regulares o parametros de Cucumber para capturar valores dinamicos como "PROMO10" o 10%.
* **Idempotencia y Estado:** Cada escenario debe ser independiente. Si un test crea un cupon en la DB, el paso de limpieza (After) debe eliminarlo para no afectar ejecuciones posteriores.
* **Selectores de UI:** En escenarios @ui, evitar selectores fragiles (Xpath). Utilizar data-testid (ej. [data-testid="coupon-message"]) para validar los mensajes de exito o error.
* **Manejo de Tiempo:** Para cupones expirados, inyectar un servicio de fecha en el sistema de pruebas para simular que "hoy" es una fecha futura, en lugar de esperar a que el tiempo real pase.

## **8. Buenas Practicas para Gherkin (IA & Human Friendly)**

Para que un agente de IA procese correctamente este documento, sigue estas reglas:

1. **Enfoque Unico:** Cada escenario debe probar una unica cosa o un unico flujo logico.
2. **Tercera Persona:** Escribir siempre desde la perspectiva del sistema o del usuario ("El usuario ingresa", "El sistema muestra").
3. **Sin Logica Tecnica:** Evita decir "El usuario hace clic en el boton con ID #btn-apply". Di "El usuario pulsa el boton Aplicar". El "como" tecnico vive en el codigo, el "que" funcional vive aqui.
4. **Uso de 'Y':** Utiliza 'Y' para encadenar condiciones (Given/DADO QUE) o acciones (Then/ENTONCES) sin repetir la palabra clave principal.

## **9. Criterios de Definicion de "Hecho" (DoD) para BDD**

Este documento se considera finalizado solo cuando se marcan todos los puntos:

* [ ] Todos los escenarios han sido revisados y firmados por el Product Owner y el Tech Lead.
* [ ] Los escenarios cubren la totalidad de las reglas de negocio descritas en la FSD.
* [ ] La IA ha generado y validado los esqueletos de codigo (step definitions) correspondientes.
* [ ] Se han incluido escenarios para los 3 flujos: Camino Feliz (Exito), Casos de Borde (Limites) y Errores Tecnicos (Resiliencia).
* [ ] Las etiquetas @tags estan correctamente aplicadas para el pipeline de CI/CD.

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

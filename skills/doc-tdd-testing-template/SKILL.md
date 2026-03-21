---
id: doc-tdd-testing-template
name: doc-tdd-testing-template
description: Genera planes de pruebas unitarias y TDD para el proyecto.
category: documentacion-de-codigo
risk: safe
source: personal
date_added: '2026-03-11'
license: MIT
---



# doc-tdd-testing-template

Genera un plan de pruebas unitarias y estrategia TDD completo cuando el usuario necesita definir su enfoque de testing.

## Cuándo usar esta skill
- Cuando el usuario necesita crear un plan de pruebas unitarias para un proyecto nuevo o existente
- Cuando se requiere definir una estrategia TDD (Test-Driven Development) con objetivos de cobertura y herramientas
- Cuando el equipo necesita documentar su filosofía de testing, técnicas de mocking y automatización del pipeline de pruebas

## Instrucciones
1. Analizar el contexto del proyecto actual (stack, arquitectura, equipo)
2. Rellenar la plantilla adaptándola al contexto específico
3. Usar español para el contenido, manteniendo términos técnicos en inglés donde corresponda
4. No dejar secciones vacías — si algo no aplica, indicar "N/A" con justificación
5. Preguntar al usuario si hay secciones que requieren decisiones pendientes

## Plantilla

# **Plantilla: Plan de Pruebas Unitarias y Estrategia TDD**

**Proyecto:** \[Nombre del Proyecto\]

**Referencia FSD:** \[Enlace a la Especificación Funcional Detallada \- plantilla\_fsd.md\]

**Referencia BDD:** \[Enlace a los Escenarios Gherkin \- plantilla\_bdd\_gherkin.md\]

**Estado:** \[Borrador / Definido / En Ejecución / Auditoría de Calidad\]

**Arquitecto de Pruebas:** \[Nombre del responsable\]

## **1\. Filosofía de Pruebas y Metodología TDD**

Este documento rige la creación de pruebas de bajo nivel antes y durante el proceso de codificación. La adopción de TDD no es solo una técnica de testeo, sino una disciplina de diseño que garantiza que el código sea modular, testeable y alineado estrictamente con los requerimientos.

### **1.1 El Ciclo de Vida "Red-Green-Refactor"**

El desarrollo debe seguir estrictamente estas tres fases iterativas:

1. **Red (Fallo):** Escribir un test unitario que falle para una unidad lógica mínima antes de que el código exista. Esto valida que el test es capaz de detectar la ausencia de la funcionalidad.
2. **Green (Paso):** Escribir el código estrictamente necesario para que el test pase. Se debe priorizar la simplicidad sobre la elegancia en este punto.
3. **Refactor (Optimización):** Limpiar el código recién escrito, eliminando duplicidad y mejorando la legibilidad, siempre garantizando que los tests permanezcan en verde.

### **1.2 Las Tres Leyes del TDD (Uncle Bob)**

* No se permite escribir código de producción sin antes escribir un test unitario que falle.
* No se permite escribir más de un test unitario del que sea suficiente para fallar (y no compilar es fallar).
* No se permite escribir más código de producción del que sea suficiente para pasar el test que falla actualmente.

### **1.3 Principio de Aislamiento**

Las pruebas unitarias deben ser **deterministas y aisladas**. No deben depender de factores externos como:

* Bases de datos reales o sistemas de archivos.
* Llamadas a red o APIs de terceros.
* Estado global compartido o variables de entorno volátiles.

## **2\. Objetivos de Cobertura, Calidad y Mantenibilidad**

Definimos los umbrales de calidad que el software debe superar para ser considerado apto para el despliegue.

* **Cobertura de Líneas (Line Coverage):** Mínimo \[85%\]. La cobertura es una métrica de riesgo: lo que no está cubierto es un lugar donde los bugs pueden esconderse.
* **Cobertura de Ramas (Branch Coverage):** Mínimo \[90%\]. Es vital para asegurar que todos los caminos lógicos (if/else, switch, catch) han sido validados.
* **Complejidad Ciclomática:** Máximo \[10\] por función. Funciones con alta complejidad deben ser refactorizadas en unidades más pequeñas.
* **Mutation Testing (Opcional pero recomendado):** Utilizar herramientas como Stryker o PIT para validar la calidad de los tests. Si al "mutar" el código de producción el test sigue pasando, el test es débil y debe mejorarse.

## **3\. Identificación de Unidades Críticas a Probar**

Lista priorizada de módulos que requieren una cobertura exhaustiva debido a su impacto en el negocio o la seguridad.

| Módulo | Función / Clase | Tipo de Prueba | Impacto en Negocio | Prioridad |
| :---- | :---- | :---- | :---- | :---- |
| **Módulo Pagos** | calculateTax() | Unitaria / Matemática | Crítico (Legal/Financiero) | P0 |
| **Auth Service** | validateToken() | Unitaria / Seguridad | Crítico (Acceso) | P0 |
| **Data Parser** | sanitizeHTML() | Unitaria / Seguridad | Alto (XSS Prevention) | P1 |
| **Logic Core** | applyDiscount() | Unitaria / Lógica | Medio (Margen) | P1 |

## **4\. Estrategia de Simulación y Dobles de Prueba (Mocking)**

Para mantener la velocidad de ejecución y el aislamiento, se utilizarán "Dobles de Prueba" siguiendo la clasificación de Martin Fowler:

* **Stubs:** Proporcionan respuestas enlatadas a las llamadas realizadas durante el test.
* **Mocks:** Objetos pre-programados con expectativas que forman una especificación de las llamadas que se espera que reciban.
* **Spies:** Stubs que también registran información sobre cómo fueron llamados (parámetros, número de veces).

### **4.1 Inyección de Dependencias**

El código debe estar diseñado para permitir la inyección de dependencias (DI). Si una clase instancia sus propias dependencias, no es testeable de forma aislada.

* **Servicios Externos:** Todas las llamadas a Stripe, AWS S3 o servicios de correo deben ser sustituidas por Mocks.
* **Persistencia:** Se utilizarán repositorios en memoria (In-memory DB) para simular el comportamiento de la base de datos sin latencia de I/O.
* **Tiempo y Determinismo:** Se debe inyectar un TimeProvider para probar lógica de expiración, evitando el uso de DateTime.Now o similar dentro del código de negocio.

## **5\. Casos de Prueba Unitarios y Técnicas de Diseño**

Desglose de escenarios técnicos obligatorios para cada unidad de código.

### **5.1 Partición de Equivalencia y Valores Límite**

No probamos todos los números, probamos las fronteras:

* **Valores Nulos/Vacíos:** ¿Cómo reacciona la función ante null, undefined o ""?
* **Límites Superiores e Inferiores:** Si un descuento es de 0% a 100%, probamos \-1, 0, 1, 99, 100 y 101\.
* **Tipos de Datos Inesperados:** Manejo de desbordamientos (overflow) o formatos de cadena inválidos.

### **5.2 Pruebas Negativas y Manejo de Excepciones**

Un test exitoso también es aquel que confirma que el sistema falla cuando debe fallar.

* **Excepciones Esperadas:** Validar que se lanza la excepción correcta ante una entrada inválida.
* **Propagación de Errores:** Asegurar que los errores de los servicios inyectados son capturados y transformados correctamente por la lógica de negocio.

## **6\. Herramientas, Frameworks y Ecosistema de Calidad**

* **Lenguaje de Desarrollo:** \[Ej. TypeScript / Go\].
* **Framework de Testing:** \[Ej. Jest / Go Testing\].
* **Librería de Dobles (Mocking):** \[Ej. Sinon.js / GoMock\].
* **Análisis Estático (Linting):** \[Ej. ESLint / Staticcheck\].
* **Visualización de Cobertura:** \[Ej. Codecov / SonarQube\].

## **7\. Automatización del Pipeline y "Developer Experience" (DX)**

Las pruebas deben ser parte integral del flujo diario, no una tarea de último minuto.

* **Pre-Commit Hooks:** Uso de herramientas como husky para ejecutar los tests de los archivos modificados antes de permitir el commit.
* **Integración Continua (CI):** El pipeline debe ejecutar la suite completa en cada Pull Request. Un solo test fallido bloquea el proceso de integración.
* **Tiempo de Ejecución:** La suite unitaria debe completarse en menos de \[2 minutos\]. Si tarda más, se debe optimizar el uso de mocks o paralelizar la ejecución.
* **Gestión de "Flaky Tests":** Cualquier test que falle de forma aleatoria debe ser marcado, investigado y corregido inmediatamente. Los tests inestables destruyen la confianza en el pipeline.

## **8\. Guía para la IA y Generación Automática de Tests**

Instrucciones específicas para que los agentes (Agent-Coder / Agent-Tester) generen código de alta calidad.

1. **Patrón AAA (Arrange, Act, Assert):**
   * **Arrange:** Configurar el estado inicial y los mocks.
   * **Act:** Ejecutar la función o método bajo prueba.
   * **Assert:** Verificar los resultados y las interacciones con los mocks.
2. **Nombramiento Semántico:** El nombre del test debe ser una oración clara: should\_return\_error\_when\_discount\_exceeds\_total().
3. **Un solo Assert lógico:** Cada test debe validar un único concepto para facilitar la depuración cuando falle.
4. **Independencia de Datos:** No asumas que la base de datos tiene datos previos. Crea tus propios datos dentro del bloque *Arrange*.

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

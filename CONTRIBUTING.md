# 🤝 Guía de Contribución - Pokémon Esmeralda

¡Gracias por tu interés en contribuir al proyecto Pokémon Esmeralda! Esta guía te ayudará a entender cómo puedes colaborar de manera efectiva.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Cómo Contribuir](#cómo-contribuir)
- [Configuración del Entorno de Desarrollo](#configuración-del-entorno-de-desarrollo)
- [Estándares de Código](#estándares-de-código)
- [Proceso de Pull Request](#proceso-de-pull-request)
- [Reportar Bugs](#reportar-bugs)
- [Sugerir Mejoras](#sugerir-mejoras)

## 📜 Código de Conducta

Este proyecto se adhiere a un código de conducta. Al participar, se espera que mantengas este código. Por favor reporta comportamientos inaceptables.

## 🚀 Cómo Contribuir

### Tipos de Contribuciones Bienvenidas

- 🐛 **Corrección de bugs**
- ✨ **Nuevas características**
- 📚 **Mejoras en documentación**
- 🎨 **Mejoras en la interfaz**
- ⚡ **Optimizaciones de rendimiento**
- 🧪 **Pruebas unitarias**
- 🌐 **Traducciones**

## 🛠️ Configuración del Entorno de Desarrollo

### 1. Fork y Clona el Repositorio

```bash
# Fork el repositorio en GitHub, luego clona tu fork
git clone https://github.com/TU-USUARIO/Pokemon-Esmeralda.git
cd Pokemon-Esmeralda

# Añade el repositorio original como upstream
git remote add upstream https://github.com/USUARIO-ORIGINAL/Pokemon-Esmeralda.git
```

### 2. Configura el Entorno Virtual

```bash
# Crea un entorno virtual
python -m venv venv

# Activa el entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instala las dependencias
pip install -r requirements.txt
```

### 3. Verifica que Todo Funcione

```bash
cd "Pokemon Esmeralda - consola"
python Main.py
```

## 📝 Estándares de Código

### Estilo de Código Python

- Sigue las convenciones de [PEP 8](https://pep8.org/)
- Usa nombres descriptivos para variables y funciones
- Añade docstrings a todas las clases y funciones públicas
- Mantén las líneas de código bajo 100 caracteres cuando sea posible

### Ejemplo de Docstring

```python
def crear_pokemon(nombre, nivel, tipo):
    """
    Crea una nueva instancia de Pokémon.
    
    Args:
        nombre (str): El nombre del Pokémon
        nivel (int): El nivel inicial del Pokémon
        tipo (str): El tipo principal del Pokémon
    
    Returns:
        Pokemon: Una nueva instancia de Pokémon
    
    Raises:
        ValueError: Si el nivel es menor a 1 o mayor a 100
    """
    pass
```

### Estructura de Archivos

- Mantén la estructura existente del proyecto
- Nuevas características deben ir en módulos separados cuando sea apropiado
- Actualiza los imports necesarios

## 🔄 Proceso de Pull Request

### 1. Crea una Rama para tu Feature

```bash
# Asegúrate de estar en la rama main y actualizada
git checkout main
git pull upstream main

# Crea una nueva rama
git checkout -b feature/nombre-descriptivo
# o para bugs:
git checkout -b bugfix/descripcion-del-bug
```

### 2. Realiza tus Cambios

- Haz commits pequeños y frecuentes
- Usa mensajes de commit descriptivos
- Prueba tus cambios antes de hacer commit

### 3. Formato de Mensajes de Commit

```
tipo(alcance): descripción breve

Descripción más detallada si es necesaria.

- Cambio específico 1
- Cambio específico 2

Fixes #123
```

**Tipos de commit:**
- `feat`: Nueva característica
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Cambios de formato (espacios, comas, etc.)
- `refactor`: Refactorización de código
- `test`: Añadir o modificar pruebas
- `chore`: Tareas de mantenimiento

### 4. Envía tu Pull Request

```bash
# Push a tu fork
git push origin feature/nombre-descriptivo

# Crea el Pull Request en GitHub
```

### 5. Descripción del Pull Request

Incluye en tu PR:

- **Descripción clara** de los cambios realizados
- **Motivación** para el cambio
- **Capturas de pantalla** si hay cambios visuales
- **Lista de verificación** de lo que has probado
- **Issues relacionados** (si los hay)

## 🐛 Reportar Bugs

### Antes de Reportar

1. Verifica que estás usando la última versión
2. Busca en issues existentes para evitar duplicados
3. Reproduce el bug de manera consistente

### Información a Incluir

- **Descripción clara** del problema
- **Pasos para reproducir** el bug
- **Comportamiento esperado** vs **comportamiento actual**
- **Entorno**: SO, versión de Python, etc.
- **Capturas de pantalla** o logs si son relevantes

### Plantilla de Bug Report

```markdown
## Descripción del Bug
Una descripción clara y concisa del problema.

## Pasos para Reproducir
1. Ve a '...'
2. Haz clic en '...'
3. Desplázate hacia '...'
4. Ve el error

## Comportamiento Esperado
Descripción clara de lo que esperabas que pasara.

## Capturas de Pantalla
Si es aplicable, añade capturas para explicar el problema.

## Entorno
- OS: [ej. Windows 10]
- Python: [ej. 3.9.0]
- Versión del juego: [ej. 1.0.0]

## Información Adicional
Cualquier otro contexto sobre el problema.
```

## 💡 Sugerir Mejoras

### Tipos de Sugerencias

- Nuevas características del juego
- Mejoras en la jugabilidad
- Optimizaciones de rendimiento
- Mejoras en la interfaz de usuario

### Plantilla de Feature Request

```markdown
## Resumen de la Característica
Descripción breve de la nueva característica.

## Motivación
¿Por qué sería útil esta característica?

## Descripción Detallada
Descripción completa de cómo funcionaría.

## Alternativas Consideradas
Otras soluciones que has considerado.

## Información Adicional
Cualquier otro contexto, capturas, mockups, etc.
```

## 🧪 Pruebas

### Ejecutar Pruebas

```bash
# Cuando implementemos pruebas unitarias
python -m pytest tests/

# Pruebas manuales
python Main.py
```

### Escribir Pruebas

- Añade pruebas para nuevas características
- Asegúrate de que las pruebas existentes sigan pasando
- Incluye casos edge y manejo de errores

## 📚 Documentación

### Actualizar Documentación

- Actualiza el README.md si es necesario
- Añade docstrings a nuevas funciones/clases
- Actualiza comentarios en el código

## ❓ ¿Necesitas Ayuda?

- Abre un issue con la etiqueta "question"
- Revisa la documentación existente
- Contacta a los mantenedores del proyecto

## 🎉 Reconocimientos

Todos los contribuidores serán reconocidos en el proyecto. ¡Gracias por hacer que Pokémon Esmeralda sea mejor!

---

**¡Esperamos tus contribuciones! 🚀**
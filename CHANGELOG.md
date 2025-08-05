# 📋 Changelog - Pokémon Esmeralda

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Sin Lanzar]

### Añadido
- Documentación completa del proyecto
- Archivos de configuración para desarrollo
- Guías de contribución

### Cambiado
- Estructura de archivos mejorada

### Corregido
- Pendiente

## [1.0.0] - 2024-01-XX

### Añadido
- Sistema de batalla por turnos completo
- Exploración de mapas con diferentes áreas (Bosque, Pueblo, Playa)
- Sistema de captura de Pokémon salvajes
- Interfaz de usuario con emojis y caracteres ASCII
- Base de datos SQLite para almacenar información de Pokémon
- Sistema de entrenadores NPCs
- Tienda Pokémon para comprar objetos
- Centro Pokémon para curar Pokémon
- Sistema de inventario (Mochila)
- Pokédex con información de Pokémon
- Sistema de movimientos y estados de Pokémon
- Controles WASD para navegación
- Encuentros aleatorios en zonas específicas

### Características Principales
- **Pokémon Iniciales Disponibles**: Gengar, Rowlet, Bulbasaur, Milotic, Garchomp, Sprigatito
- **Áreas Explorables**: Bosque Verde, Pueblo, Playa
- **Sistema de Combate**: Turnos, tipos de Pokémon, efectividad
- **Objetivo**: Derrotar a 7 campeones regionales y al campeón mundial Lionel

### Tecnologías
- Python 3.x
- SQLite3 para base de datos
- readchar para captura de teclas
- Módulos estándar: os, random, math, time, enum

### Estructura del Proyecto
- `Main.py`: Punto de entrada del juego
- `Pokemon.py`: Clase Pokémon y mecánicas
- `Entrenador.py`: Sistema de entrenadores
- `Algoritmo_De_Batalla.py`: Lógica de combate
- `Area.py`: Definición de mapas y áreas
- `Mochila.py`: Sistema de inventario
- `Movimiento.py`: Movimientos de Pokémon
- `Estado.py`: Estados y efectos
- `Pokedex.py`: Enciclopedia de Pokémon
- `Estrucutra.py`: Tiendas y centros Pokémon
- `data.py`: Utilidades y datos del juego

---

## Tipos de Cambios

- `Añadido` para nuevas características
- `Cambiado` para cambios en funcionalidades existentes
- `Obsoleto` para características que serán removidas
- `Removido` para características removidas
- `Corregido` para corrección de bugs
- `Seguridad` para vulnerabilidades

## Formato de Versiones

Este proyecto usa [Semantic Versioning](https://semver.org/):

- **MAJOR**: Cambios incompatibles en la API
- **MINOR**: Funcionalidades añadidas de manera compatible
- **PATCH**: Correcciones de bugs compatibles

Ejemplo: `1.2.3`
- `1` = Versión mayor
- `2` = Versión menor  
- `3` = Parche
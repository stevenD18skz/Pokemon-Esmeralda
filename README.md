# 🎮 Pokémon Esmeralda - Juego de Consola

Un juego de Pokémon desarrollado en Python que simula la experiencia clásica de los juegos de la franquicia, implementado completamente en consola con una interfaz de texto enriquecida.

## 📋 Descripción

Pokémon Esmeralda es un juego de rol por turnos donde el jugador asume el papel de un entrenador Pokémon que debe enfrentarse a los mejores campeones de cada región. El objetivo principal es convertirse en el campeón mundial derrotando a todos los líderes de gimnasio y campeones regionales.

### 🎯 Características Principales

- **Sistema de Batalla Completo**: Combates por turnos con mecánicas clásicas de Pokémon
- **Exploración de Mapas**: Navega por diferentes áreas como bosques, pueblos y playas
- **Captura de Pokémon**: Encuentra y captura Pokémon salvajes en diferentes zonas
- **Sistema de Entrenadores**: Enfrenta a entrenadores NPCs y campeones regionales
- **Tienda Pokémon**: Compra objetos y mejoras para tu equipo
- **Centro Pokémon**: Cura a tus Pokémon después de las batallas
- **Base de Datos SQLite**: Almacenamiento persistente de datos de Pokémon
- **Interfaz Visual ASCII**: Representación gráfica usando emojis y caracteres especiales

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/Pokemon-Esmeralda.git
   cd Pokemon-Esmeralda
   ```

2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta el juego**:
   ```bash
   cd "Pokemon Esmeralda - consola"
   python Main.py
   ```

## 🎮 Cómo Jugar

### Controles Básicos
- **W**: Mover hacia arriba
- **S**: Mover hacia abajo  
- **A**: Mover hacia la izquierda
- **D**: Mover hacia la derecha

### Elementos del Mapa
- 🟩 Terreno normal
- 🌳 Árboles (obstáculos)
- 🌱 Arbustos (zona de encuentros Pokémon)
- 🌊 Agua
- 🚪 Puertas/Transiciones entre áreas
- 🏠 Casas
- 🏪 Tienda Pokémon
- 🏥 Centro Pokémon
- 🙎 Entrenadores NPCs
- 👤 Tu personaje

### Mecánicas del Juego

1. **Exploración**: Muévete por el mundo usando las teclas WASD
2. **Encuentros Pokémon**: Camina por arbustos para encontrar Pokémon salvajes
3. **Batallas**: Sistema de combate por turnos con diferentes movimientos
4. **Captura**: Debilita a los Pokémon salvajes para capturarlos
5. **Gestión de Equipo**: Administra tu equipo de hasta 6 Pokémon
6. **Compras**: Visita tiendas para comprar objetos útiles

## 📁 Estructura del Proyecto

```
Pokemon-Esmeralda/
├── Pokemon Esmeralda - consola/
│   ├── Main.py                 # Punto de entrada del juego
│   ├── Pokemon.py              # Clase Pokemon y mecánicas relacionadas
│   ├── Entrenador.py           # Clase Entrenador (jugador y NPCs)
│   ├── Algoritmo_De_Batalla.py # Sistema de combate
│   ├── Area.py                 # Definición de mapas y áreas
│   ├── Mochila.py              # Sistema de inventario
│   ├── Movimiento.py           # Movimientos de Pokémon
│   ├── Estado.py               # Estados de Pokémon y efectos
│   ├── Pokedex.py              # Enciclopedia de Pokémon
│   ├── Estrucutra.py           # Estructuras del juego (tiendas, centros)
│   ├── data.py                 # Utilidades y datos del juego
│   └── data_base/
│       ├── pokemonRojoFuego.db # Base de datos SQLite
│       └── z-base de datos pokemon Sqlite3.txt
├── .gitignore
├── requirements.txt
└── README.md
```

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**: Lenguaje de programación principal
- **SQLite3**: Base de datos para almacenar información de Pokémon
- **readchar**: Librería para captura de teclas en tiempo real
- **Módulos estándar**: os, random, math, time, enum

## 🎯 Objetivos del Juego

1. **Objetivo Principal**: Derrotar a todos los campeones regionales
2. **Campeones a Enfrentar**:
   - Campeón de Kanto: Azul
   - Campeones de otras regiones
   - Campeona de Teselia: Iris
   - Campeón Mundial: Lionel (jefe final)

## 🔧 Desarrollo y Contribución

### Estado del Proyecto
- ✅ Sistema de batalla básico implementado
- ✅ Exploración de mapas funcional
- ✅ Sistema de captura de Pokémon
- ✅ Interfaz de usuario básica
- 🔄 Sistema de entrenadores (en desarrollo)
- 🔄 Balanceo de dificultad (en desarrollo)

### Para Desarrolladores

Si quieres contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Añadir nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crea un Pull Request

## 📝 Notas del Desarrollador

Este proyecto es una implementación educativa y de entretenimiento que recrea las mecánicas básicas de los juegos Pokémon. No tiene afiliación oficial con The Pokémon Company o Nintendo.

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🐛 Reportar Problemas

Si encuentras algún bug o tienes sugerencias, por favor crea un issue en el repositorio de GitHub.

---

**¡Disfruta tu aventura Pokémon! 🎮✨**

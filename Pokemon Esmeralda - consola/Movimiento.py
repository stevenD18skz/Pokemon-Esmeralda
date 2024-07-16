from Estado import *



class Movimiento:
    """
    Representa un movimiento en el juego Pokémon, incluyendo sus características y efectos.

    Atributos:
    ----------
    nombre : str
        El nombre del movimiento.
    tipo : str
        El tipo del movimiento (por ejemplo, "Fuego", "Agua").
    clase : str
        La clase del movimiento (por ejemplo, "Físico", "Especial").
    potencia : int
        La potencia del movimiento.
    precision : int
        La precisión del movimiento.
    pp : int
        Los puntos de poder (PP) actuales del movimiento.
    Mpp : int
        Los puntos de poder (PP) máximos del movimiento.
    probabilidadDelEfecto : int
        La probabilidad de que el efecto secundario ocurra.
    EfectoSecundario : Efecto
        El efecto secundario del movimiento.

    Métodos:
    --------
    __init__(self, nombre, tipo, clase, potencia, precision, pp, probabilidadDelEfecto, EfectoSecundario):
        Inicializa una nueva instancia del movimiento.

    mostrar_informacion(self):
        Devuelve una cadena con la información del movimiento.

    get_nombre(self):
        Devuelve el nombre del movimiento.

    get_tipo(self):
        Devuelve el tipo del movimiento.

    get_clase(self):
        Devuelve la clase del movimiento.

    get_potencia(self):
        Devuelve la potencia del movimiento.

    get_precision(self):
        Devuelve la precisión del movimiento.

    get_pp(self):
        Devuelve los puntos de poder (PP) actuales del movimiento.

    set_pp(self, nuevo_pp):
        Establece los puntos de poder (PP) actuales del movimiento.

    get_mpp(self):
        Devuelve los puntos de poder (PP) máximos del movimiento.

    get_efecto_secundario(self):
        Devuelve el efecto secundario del movimiento.

    get_probabilidad_del_efecto(self):
        Devuelve la probabilidad de que ocurra el efecto secundario.
    """

    def __init__(self, nombre, tipo, clase, potencia, precision, pp, probabilidad_del_efecto, efecto_secundario):
        """
        Inicializa una nueva instancia del movimiento.

        Parámetros:
        -----------
        nombre : str
            El nombre del movimiento.
        tipo : str
            El tipo del movimiento (por ejemplo, "Fuego", "Agua").
        clase : str
            La clase del movimiento (por ejemplo, "Físico", "Especial").
        potencia : int
            La potencia del movimiento.
        precision : int
            La precisión del movimiento.
        pp : int
            Los puntos de poder (PP) actuales del movimiento.
        probabilidad_del_efecto : int
            La probabilidad de que el efecto secundario ocurra.
        efecto_secundario : Efecto
            El efecto secundario del movimiento.
        """
        self.nombre = nombre
        self.tipo = tipo
        self.clase = clase
        self.potencia = potencia
        self.precision = precision
        self.pp = pp
        self.Mpp = pp
        self.efecto_secundario = efecto_secundario
        self.probabilidad_del_efecto = probabilidad_del_efecto

    def mostrar_informacion(self):
        """
        Devuelve una cadena con la información del movimiento.

        Returns:
        --------
        str
            Una cadena que contiene la información del movimiento.
        """
        txt = []
        txt.append("◤────────────────────────────────────◥")
        txt.append(f"🌀El ataque {self.nombre} tiene las características:🌀")
        txt.append("┌────────────────────────────────────┐")
        txt.append(f"│   Tipo: {self.tipo}  |")
        txt.append(f"│   Clase: {self.clase}  |")
        txt.append(f"│   Potencia: {str(self.potencia)}  |")
        txt.append(f"│   Precisión: {str(self.precision)}  |")
        txt.append(f"│   PP: {str(self.pp)}  |")
        txt.append(f"│   Efecto secundario: {self.efecto_secundario.getNombre()} ({str(self.probabilidad_del_efecto)})  |")
        txt.append("└────────────────────────────────────┘")
        txt.append("◣────────────────────────────────────◢")
        
        return "\n".join(txt)

    def getNombre(self):
        """
        Devuelve el nombre del movimiento.

        Returns:
        --------
        str
            El nombre del movimiento.
        """
        return self.nombre

    def getTipo(self):
        """
        Devuelve el tipo del movimiento.

        Returns:
        --------
        str
            El tipo del movimiento.
        """
        return self.tipo

    def getClase(self):
        """
        Devuelve la clase del movimiento.

        Returns:
        --------
        str
            La clase del movimiento.
        """
        return self.clase

    def getPotencia(self):
        """
        Devuelve la potencia del movimiento.

        Returns:
        --------
        int
            La potencia del movimiento.
        """
        return self.potencia

    def getPrecision(self):
        """
        Devuelve la precisión del movimiento.

        Returns:
        --------
        int
            La precisión del movimiento.
        """
        return self.precision

    def getPP(self):
        """
        Devuelve los puntos de poder (PP) actuales del movimiento.

        Returns:
        --------
        int
            Los puntos de poder (PP) actuales del movimiento.
        """
        return self.pp
    
    def setPP(self, nuevo_pp):
        """
        Establece los puntos de poder (PP) actuales del movimiento.

        Parámetros:
        -----------
        nuevo_pp : int
            Los nuevos puntos de poder (PP) actuales del movimiento.
        """
        self.pp = nuevo_pp

    def getMPP(self):
        """
        Devuelve los puntos de poder (PP) máximos del movimiento.

        Returns:
        --------
        int
            Los puntos de poder (PP) máximos del movimiento.
        """
        return self.Mpp

    def getEfectoSecundario(self):
        """
        Devuelve el efecto secundario del movimiento.

        Returns:
        --------
        Efecto
            El efecto secundario del movimiento.
        """
        return self.efecto_secundario

    def getProbabilidadDelEfecto(self):
        """
        Devuelve la probabilidad de que ocurra el efecto secundario.

        Returns:
        --------
        int
            La probabilidad de que ocurra el efecto secundario.
        """
        return self.probabilidad_del_efecto

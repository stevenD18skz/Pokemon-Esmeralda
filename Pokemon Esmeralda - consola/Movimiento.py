from Estado import *
#OPCION 3





class Movimiento:#✔✔✔
    def __init__(self, nombre, tipo, clase, potencia, precision, pp, probabilidadDelEfecto, EfectoSecundario):#✔✔✔
        self.nombre = nombre
        self.tipo = tipo
        self.clase = clase
        
        self.potencia = potencia
        self.precision = precision
        self.pp = pp
        self.Mpp = pp

        self.EfectoSecundario = EfectoSecundario
        self.probabilidadDelEfecto = probabilidadDelEfecto


        
    def mostrar_informacion(self):#✔✔✔
        # Imprimimos el menú con los datos del ataque
        print("◤────────────────────────────────────◥")
        print(f"🌀El ataque {self.nombre} tiene las características:🌀")
        print("┌────────────────────────────────────┐")
        print(f"│   Tipo: {self.tipo}  |")
        print(f"│   Clase: {self.clase}  |")
        print(f"│   Potencia: {str(self.potencia)}  |")
        print(f"│   Precisión: {str(self.precision)}  |")
        print(f"│   PP: {str(self.pp)}  |")
        print(f"│   Efecto secundario: {self.EfectoSecundario.getNombre()} ({str(self.probabilidadDelEfecto)})  |")
        print("└────────────────────────────────────┘")
        print(f"◣────────────────────────────────────◢")



    def getNombre(self):
        return self.nombre

    def getTipo(self):
        return self.tipo

    def getClase(self):
        return self.clase

    def getPotencia(self):
        return self.potencia

    def getPrecicion(self):
        return self.precision

    def getPP(self):
        return self.pp
    def setPP(self, nuevoPP):
        self.pp = nuevoPP

    def getMPP(self):
        return self.Mpp

    def getEfectoSecundario(self):
        return self.EfectoSecundario

    def getprobabilidadDelEfecto(self):
        return self.probabilidadDelEfecto
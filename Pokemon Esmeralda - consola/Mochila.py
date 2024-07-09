import os
from Estado import *
#OPCION 3





class Medicina:#✔✔✔
    def __init__(self, nombre, tipo, precio_compra, precio_venta, curar, purificar):
        self.nombre = nombre
        self.tipo = tipo
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta
        self.curar = curar
        self.purificar = purificar



    def mostrar_informacion(self):#✔✔✔
        print("+" + "-" * 30 + "+")
        print("|   Información del objeto   |")
        print("+" + "-" * 30 + "+")
        print(f"| Nombre: {self.nombre}")
        print(f"| Tipo: {self.tipo}")
        print(f"| Precio de compra: {self.precio_compra} monedas")
        print(f"| Precio de venta: {self.precio_venta} monedas")
        print(f"| Capacidad de curar: {self.curar} puntos")
        print(f"| Capacidad de purificar: {self.purificar} puntos")
        print("+" + "-" * 30 + "+")



    def curarPsPokemon(self, pokeASanar):#✔✔✔
        if pokeASanar.getPs() == pokeASanar.getMps():#si el pokemon tiene los ps al maximo
            print("❌❌❌", self.nombre, "no tendra ningun efecto en", pokeASanar.getNombre(), "❌❌❌")

        elif pokeASanar.getPs() + self.curar > pokeASanar.getMps() or self.curar == 100:#para sanar los ps del pokemon al maximo
            restored_ps = pokeASanar.getMps() - pokeASanar.getPs()
            print("💊💊💊los ps de", pokeASanar.getNombre(), "han sido restaurados", restored_ps, "puntos, su vida queda en", pokeASanar.getMps(), "💊💊💊")
            pokeASanar.setPs(pokeASanar.getMps())

        else:#para sanar al pokemon solo lo que cura la pocion
            pokeASanar.setPs(pokeASanar.getPs() + self.curar)
            print("💊💊💊los ps de", pokeASanar.getNombre(), "hah sido restaurados", self.curar, "puntos, su vida queda en", pokeASanar.getPs(), "💊💊💊")




    def curarEstados(self, pokeASanar):#✔✔✔
        if pokeASanar.getEstado().getNombre() == self.purificar or self.purificar == "ALL":
            print("\n\n🍞🍞🍞El estado de", pokeASanar.getNombre(), "ah sido purificado🍞🍞🍞")
            consulta_estado = f"""
               SELECT * FROM estado WHERE id_estado = 1"""
            cursor.execute(consulta_estado)
            estado_consultado = cursor.fetchall()[0][1:]
            pokeASanar.setEstado(Estado(*estado_consultado))

        else:
            print("❌❌❌", self.nombre, "no tendra ningun efecto en", pokeASanar.getNombre(), "❌❌❌")




    def sanarPokemon(self, pokeSanado):#✔✔✔
        if self.tipo == "Pocion":
            self.curarPsPokemon(pokeSanado)

        if self.tipo == "Restaurador de estado":
            self.curarEstados(pokeSanado) 



    def getNombre(self):
        return self.nombre

    def getTipo(self):
        return self.tipo

    def getPrecioCompra(self):
        return self.precio_compra

    def getPrecioVenta(self):
        return self.precio_venta





class PokeBalls:
    def __init__(self, nombre, tipo, precio_compra, precio_venta, ratio):
        self.nombre = nombre
        self.tipo = tipo
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta
        self.ratio = ratio



    def getNombre(self):
        return self.nombre

    def getTipo(self):
        return self.tipo

    def getPrecioCompra(self):
        return self.precio_compra

    def getPrecioVenta(self):
        return self.precio_venta

    def getRatio(self):
        return self.ratio






def crearItem(itemDeseado):
    consulta_tipo = f"""
        SELECT tipo
        FROM (
            SELECT nombre, tipo FROM medicina
            UNION ALL
            SELECT nombre, tipo FROM pokeBall
            ) AS UnionResult
        WHERE nombre = '{itemDeseado}';
    """
    cursor.execute(consulta_tipo)
    tipoDelObjeto = cursor.fetchall()[0][0]
    tabla = "medicina"
    if tipoDelObjeto == "pokéball":
        tabla = "pokeBall"
    consulta_item = f"SELECT * FROM {tabla} WHERE nombre = '{itemDeseado}'"
    cursor.execute(consulta_item)
    datosItem = cursor.fetchall()[0]
    opciones = {
        "medicina":Medicina,
        "pokeBall":PokeBalls,
    }
    item = opciones[tabla](*datosItem[1:])
    return item






class Mochila:
    def __init__(self):
        self.bolsilloDeMedicina = [[crearItem("Poción"),30], [crearItem("Limonada"),30]]
        self.bolsilloDePokeBalls = [[crearItem("Ultraball"),20]]


        self.bolsilloAbierto = self.bolsilloDeMedicina


    def mostrar_bolsillo(self):
        print(f"   🔴⭕>>>>>> ------ del jugador<<<<<<⭕🔴")
        for objeto in range(len(self.bolsilloAbierto)):
            nombre = self.bolsilloAbierto[objeto][0].getNombre()
            cantidad = self.bolsilloAbierto[objeto][1]
            formatted_cant = "".ljust(15 - len(nombre))  # Ajustar el ancho según tus necesidades
            print(f"            {objeto+1}. {nombre}    {formatted_cant}    cant: {cantidad}")


    def guardar_objeto(self, obj_a_guardar, cant):
        self.bolsilloAbierto = self.bolsilloDeMedicina
        if obj_a_guardar.getTipo() == "pokéball":
            self.bolsilloAbierto = self.bolsilloDePokeBalls

        for add in range(len(self.bolsilloAbierto)):
            if self.bolsilloAbierto[add][0].getNombre() == obj_a_guardar.getNombre():
                self.bolsilloAbierto[add][1] += cant
                return f"Las {cant} {obj_a_guardar.getNombre()} han sido añadidas a tu bolsa, tienes en total {self.bolsilloAbierto[add][1]}"
                
        
        #si es un objeto que no habia antes
        self.bolsilloAbierto.insert(0, [obj_a_guardar, cant])
        return f"has adquirido un nuevo objeto\nLas {cant} {obj_a_guardar.getNombre()} han sido añadidas a tu bolsa, tienes en total {self.bolsilloAbierto[0][1]}"




    def usar_objeto(self, objUsado, cantidad):
        for x in self.bolsilloAbierto:
            if x[0] == objUsado:
                x[1] -= cantidad
    



    def tirar(self, objetoAtirar, cantidad):
        #list(map(lambda x: print(x), self.bolsilloAbierto))
        for objeto in self.bolsilloAbierto:
            if objeto[0] == objetoAtirar:
                objeto[1] -= cantidad


        





    def abrir_mochila(self):
        while True:
            #os.system('cls' if os.name == 'nt' else 'clear')
            print("╔════════════════════════════════════════════════════════╗")
            print("║                        BOLSA                           ║")
            print("╠════════════════════════════════════════════════════════╣")
            self.mostrar_bolsillo()
            print(f"\n  ◆ M.Medicinas        ◆ P.Pokeballs        ◆ S.Salir")
            print("╚════════════════════════════════════════════════════════╝")
            eleccion = input("== ")

            if eleccion.upper() == "M":
                self.bolsilloAbierto = self.bolsilloDeMedicina

            elif eleccion.upper() == "P":
                self.bolsilloAbierto = self.bolsilloDePokeBalls

            elif eleccion.upper() == "S":
                return None

            elif int(eleccion) >= 1 or int(eleccion) < len(self.bolsilloAbierto[0]):
                item = self.bolsilloAbierto[int(eleccion)-1][0]
                return item

            else:
                print("❌❌❌Escoge una Opcion valida porfavor❌❌❌")
        

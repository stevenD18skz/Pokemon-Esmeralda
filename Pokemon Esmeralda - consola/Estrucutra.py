from Mochila import *
from Entrenador import *
from data import interfaz_usuario


class Estructura:
    def __init__(self, nombre, tipo_estructura, posicion_entrada_area, representacion_mapa='E'):
        """
        Inicializa una estructura genérica.

        Args:
            nombre (str): Nombre de la estructura (ej: "Tienda Pokémon", "Centro Pokémon").
            tipo_estructura (str): Un identificador del tipo (ej: "tienda", "centro_pk", "casa").
            posicion_entrada_area (tuple): Coordenadas (fila, columna) de la entrada de esta
                                           estructura en el mapa del área que la contiene.
            representacion_mapa (str): Carácter que representa la entrada de esta estructura
                                       en el mapa del área.
        """
        self.nombre = nombre
        self.tipo_estructura = tipo_estructura
        self.posicion_entrada_area = posicion_entrada_area  # Donde se encuentra en el mapa del área
        self.representacion_mapa = representacion_mapa      # Cómo se dibuja en el mapa del área

    def interactuar(self, jugador, area_actual):
        """
        Acción por defecto al interactuar con la estructura desde fuera (ej: leer un cartel).
        Debería ser sobrescrita por clases hijas para comportamientos específicos.
        """
        print(f"Estás frente a {self.nombre}.")
        # Podrías tener un input genérico aquí o simplemente un mensaje.

    def entrar(self, jugador, area_actual):
        """
        Acción por defecto al intentar entrar en la estructura.
        Debería ser sobrescrita si la estructura tiene un interior explorable o un menú.
        """
        print(f"Intentas entrar a {self.nombre}, pero parece genérico por ahora.")
        # Aquí es donde el juego cambiaría de contexto al interior de la estructura.
        return None # O un nuevo estado/mapa si se entra.

    def __str__(self):
        return f"{self.nombre} ({self.tipo_estructura}) en {self.posicion_entrada_area}"



#CLASE COMPLETA
class Tienda(Estructura):
    def __init__(self):
        """
        Representa una tienda Pokémon donde los clientes pueden comprar y vender objetos.

        Attributes:
            nombre (str): El nombre de la tienda.
            cliente (Cliente): El cliente actual en la tienda.
            inventario (list): La lista de objetos disponibles en la tienda.

        Methods:
            mostrar_inventario():
                Muestra el inventario de la tienda.
            comprar():
                Permite al cliente comprar objetos de la tienda.
            verificar_disponibilidad(objeto, cantidad):
                Verifica si hay suficiente cantidad de un objeto en la mochila del cliente.
            vender():
                Permite al cliente vender objetos a la tienda.
            salir():
                Muestra un mensaje de despedida y finaliza la interacción.
            recibir_jugador(cliente):
                Inicializa la interacción con un nuevo cliente.
        """
        self.nombre = "Tienda Pokemon"
        self.cliente = None
        self.inventario = self.cargar_inventario()
        self.posicion_entrada_area = (9,7)  # Donde se encuentra en el mapa del área
        self.mapa_layout_str =  """
mmmmmmmmmmmmmmmmmmmm
m000s00000000000000m
m00ts00000000000000m
m000s00000000000000m
m000s00000000000000m
m000s00000000000000m
m000s00000000000000m
mmmmmmmmm9mmmmmmmmmm
"""





    def interfaz_tienda(self, *mensaje, is_input=False, validacion=None, mensaje_raise=""):
        """
        Función auxiliar para llamar a self.interfaz_tienda con el display preestablecido para batallas.

        Parámetros:
        -----------
        mensaje : str
            El mensaje principal que se mostrará al usuario.

        is_input : bool, opcional
            Indica si se espera una entrada del usuario.

        validacion : function, opcional
            Una función que toma la entrada del usuario como argumento y devuelve True si la entrada es válida, 
            o False si no lo es.

        mensaje_raise : str, opcional
            El mensaje que se mostrará si la validación de la entrada falla.
        """
        return interfaz_usuario(
            *mensaje,
            display=self.mostrar_inventario(),
            is_input=is_input,
            validacion=validacion,
            mensaje_raise=mensaje_raise
        )



    def cargar_inventario(self):
        """
        Carga el inventario de la tienda desde la base de datos.
        
        Returns:
            list: Lista de objetos disponibles en la tienda.
        """
        CONSULTA_INVENTARIO = """
            SELECT nombre, precio_compra, precio_venta FROM pokeball 
            UNION 
            SELECT nombre, precio_compra, precio_venta FROM Medicina
        """
        cursor.execute(CONSULTA_INVENTARIO)
        return cursor.fetchall()



    def mostrar_inventario(self):
        """
        Devuelve una cadena con el inventario de la tienda con los nombres y precios de los objetos.
        """
        txt = []
        txt.append("         🌟 Inventorio Mágico 🌟           \n")
        txt.append("════════════════════════════════════════════\n")
        for i, objeto in enumerate(self.inventario, start=1):
            txt.append(f"🔮 {i}. {objeto[0]:<20} 💰 {objeto[1]:>5} monedas\n")
        txt.append("════════════════════════════════════════════\n")
        txt.append("┌────────────────────────┐\n")
        txt.append(f"|    Dinero: {self.cliente.getDinero()}    \n")
        txt.append("└────────────────────────┘\n")
        
        return "\n".join(txt)



    def comprar(self):
        """
        Permite al cliente comprar objetos de la tienda.

        Este método guía al usuario a través del proceso de compra de un objeto en la tienda.
        Incluye la selección del objeto, la cantidad deseada, y la confirmación de la compra.
        Si el cliente no tiene suficiente dinero, la compra no se realiza.

        Pasos:
        ------
        1. Elegir Producto:
            - El usuario selecciona el producto que desea comprar del inventario.
            - Si el usuario decide cancelar la compra, puede hacerlo ingresando 'x'.

        2. Elegir Cantidad:
            - Una vez seleccionado el producto, el usuario indica cuántas unidades desea comprar.
            - La cantidad debe ser un número entero positivo.

        3. Confirmar Compra:
            - El usuario confirma la compra.
            - Las opciones disponibles son:
                'y' - Sí, realizar la compra.
                'n' - No, cambiar la cantidad.
                'p' - Cambiar el producto.
                'x' - Cancelar la compra.

        Retornos:
        ---------
        bool
            False si la compra fue cancelada o no se pudo realizar debido a fondos insuficientes.
            True si la compra fue realizada exitosamente.

        Manejo de Excepciones:
        ----------------------
        ValueError:
            Si ocurre un ValueError durante la ejecución, se muestra un mensaje de error y se solicita una nueva entrada.
        
        KeyboardInterrupt:
            Si el usuario interrumpe la ejecución con un comando especial (por ejemplo, Ctrl+C), se muestra un mensaje 
            de cancelación y se solicita una nueva entrada.
        
        Exception:
            Cualquier otra excepción se captura y se muestra un mensaje de error inesperado, retornando False.

        Ejemplos de Uso:
        ----------------
        tienda = Tienda()
        tienda.recibir_jugador(cliente)
        tienda.comprar()
        """
        def elegir_producto():
            mensaje = f"¿Qué producto quieres llevarte?\n(x para salir)"
            eleccion = self.interfaz_tienda(
                mensaje,
                is_input=True,
                validacion=lambda x: x.lower() == "x" or (x.isdigit() and 1 <= int(x) <= len(self.inventario)),
                mensaje_raise=f"Escoge un item válido por favor .(1 - {len(self.inventario)})"
            )
            if eleccion.lower() == "x":
                return "salir"

            return int(eleccion) - 1

        def elegir_cantidad():
            mensaje = f"{item_comprado.getNombre()}?, buena elección\n¿Cuántas quieres llevarte?"
            cantidad = self.interfaz_tienda(
                mensaje,
                is_input=True,
                validacion=lambda x: x.isdigit() and int(x) > 0,
                mensaje_raise="Ingresa el numero de producto que quieres comprar"
            )
            return int(cantidad)

        def confirmar_compra():
            total = item_comprado.getPrecioCompra()*cantidad
            mensaje = f"Sería un total de {total}. ¿Deseas realizar la compra?\n(y. Sí n. Cambiar cantidad p. Cambiar producto x. Salir)"
            eleccion = self.interfaz_tienda(
                mensaje,
                is_input=True,
                validacion=lambda x: x.lower() in ["y", "n", "p", "x"],
                mensaje_raise="Ingresa una opción válida (y, n, p, x)"
            )
            return eleccion.lower()

        estado = "producto"
        item_comprado = None
        cantidad = None

        while estado != "salir":
            if estado == "producto":
                eleccion = elegir_producto()
                if eleccion == "salir":
                    estado = "salir"
                    return False

                item_comprado = crearItem(self.inventario[eleccion][0])
                estado = "cantidad"

            elif estado == "cantidad":
                cantidad = elegir_cantidad()
                estado = "confirmar"

            elif estado == "confirmar":
                eleccion = confirmar_compra()

                if eleccion == "y":  # Realiza la compra
                    if self.cliente.getDinero() >= item_comprado.getPrecioCompra() * cantidad:
                        self.cliente.setDinero(self.cliente.getDinero() - item_comprado.getPrecioCompra() * cantidad)
                        self.interfaz_tienda(*self.cliente.getMochila().guardar_objeto(item_comprado, cantidad))

                        estado, eleccion, cantidad = "producto", None, None
                                
                    else:
                        self.interfaz_tienda(f"No tienes suficiente dinero")
                        estado = "cantidad"

                elif eleccion == "n":
                    estado = "cantidad"

                elif eleccion == "p":
                    estado = "producto"

                elif eleccion == "x":
                    self.interfaz_tienda(f"Compra cancelada.")
                    estado = "salir"



    def verificar_disponibilidad(self, objeto, cantidad):
        """
        Verifica si hay suficiente cantidad de un objeto en la mochila del cliente.

        Args:
            objeto (str): El nombre del objeto a verificar.
            cantidad (int): La cantidad del objeto a verificar.

        Returns:
            bool: True si hay suficiente cantidad, False de lo contrario.
        """
        for item, cantidad_disponible in self.cliente.getMochila().bolsilloAbierto:
            if item == objeto:
                return cantidad_disponible >= cantidad
        return True



    def vender(self):
        """
        Permite al cliente vender objetos a la tienda.
        """
        objeto = self.cliente.getMochila().sacar_objeto()
        if objeto is None:
            self.interfaz_tienda("NO SELECCIONASTE NINGIN OBJETO")
            return
        
        while True:
            cantidad = self.interfaz_tienda(
                f"¿Cuántos {objeto.getNombre()} quieres vender?\n('x' para salir)",
                is_input=True,
                validacion=lambda x: x.lower() == "x" or (x.isdigit() and int(x) > 0),
                mensaje_raise="Ingresa una cantidad válida."
            )

            if cantidad.lower() == "x":
                return False

            cantidad = int(cantidad)
            if cantidad <= 0 or not self.verificar_disponibilidad(objeto, cantidad):
                self.interfaz_tienda(f"No tienes suficientes {objeto.getNombre()} para vender")
                continue
    
            break

        # Consulta de precio y cálculo de oferta
        consultar_precio = f"""
            SELECT precio_venta 
            FROM pokeball 
            WHERE nombre = '{objeto.getNombre()}'
            UNION 
            SELECT precio_venta 
            FROM Medicina 
            WHERE nombre = '{objeto.getNombre()}'
        """
        precio = cursor.execute(consultar_precio).fetchone()[0]
        oferta = precio * cantidad

        # Realizar la venta y actualizar el dinero del cliente
        self.cliente.getMochila().tirar(objeto, cantidad)
        self.cliente.setDinero(self.cliente.getDinero() + oferta)

        # Mostrar mensaje de confirmación al usuario
        self.interfaz_tienda(f"Has vendido {cantidad} {objeto.getNombre()}(s), has ganado {oferta}$")

        return False
    


    def salir(self):
        """
        Muestra un mensaje de despedida y finaliza la interacción.
        """
        self.interfaz_tienda("Hasta la próxima, vuelve pronto")
        return True



    def recibir_jugador(self, cliente):
        """
        Inicializa la interacción con un nuevo cliente.

        Args:
            cliente (Cliente): El cliente que entra a la tienda.
        """
        self.cliente = cliente
        self.interfaz_tienda(f"Bienvenido a la tienda, {cliente.getNombre()}.\n¡Podrías echar un vistazo a nuestro inventario!")
        opciones = {
            "c": self.comprar,
            "v": self.vender,
            "x": self.salir
        }
        
        while True:
            accion_tienda = self.interfaz_tienda(
                "¿En qué puedo ayudarte?\nC. Comprar\nV. Vender\nX. Salir",
                is_input=True,
                validacion=lambda x: x.lower() in ["c","v","x"],
                mensaje_raise="Entrada no válida. Por favor, elige una opción válida (C, V o X)."
            )

            if opciones[accion_tienda.lower()]():
                return
            


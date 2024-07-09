from Mochila import *
from Entrenador import *
from data import mensaje_game, mensajes_exterior
#OPCION 3



class Tienda:
	def __init__(self):
		self.nombre = "Tienda Pokemon"
		self.cliente = None
		self.inventario = []

		consulta = "SELECT nombre, precio_compra, precio_venta FROM pokeball UNION SELECT nombre, precio_compra, precio_venta FROM Medicina"
		cursor.execute(consulta)
		objetos_para_tienda = cursor.fetchall()

		for objeto in objetos_para_tienda:
			self.inventario.append(objeto)




	def mostrar_inventario(self):#✔✔✔
		print("		 🌟 Inventorio Mágico 🌟")
		print("════════════════════════════════════════════")
		for i, objeto in enumerate(self.inventario, start=1):
			print(f"🔮 {i}. {objeto[0]:<20} 💰 {objeto[1]:>5} monedas")
		print("════════════════════════════════════════════")
		print("┌────────────────────────┐")
		print(f"|   Diner: {self.cliente.getDinero()}   ")
		print("└────────────────────────┘")



	def comprar(self):#✔✔✔
		while True:
			eleccion = int(input(f"{mensaje_game("Que producto quieres llevarte?", self.mostrar_inventario, isInput=True)}\n==")) - 1
			
			if eleccion > 0 or eleccion < len(self.inventario):
				item_comprado = crearItem(self.inventario[eleccion][0])

				cantidad = int(input(f"{mensaje_game(f"{self.inventario[eleccion][0]}?, buena eleccion\nCuantas quieres llevarte", self.mostrar_inventario, isInput=True)}\n=="))


				confirmacion = int(input(f"{mensaje_game(f"Seria un total de {item_comprado.getPrecioCompra()*cantidad}, estas seguro?\n1.Si\n2.No", self.mostrar_inventario, isInput=True)}\n=="))

				if not (confirmacion-1):
					if self.cliente.getDinero() >= item_comprado.getPrecioCompra()*cantidad:
						self.cliente.setDinero(self.cliente.getDinero()-item_comprado.getPrecioCompra()*cantidad)
						mensaje_game(self.cliente.getMochila().guardar_objeto(item_comprado, cantidad), self.mostrar_inventario)

					else:
						mensaje_game("No tienes suficiente dinero", self.mostrar_inventario)

			else:
				mensaje_game("Escoge una un item valido porfavor", self.mostrar_inventario)

			break
		return False



	def verificar_disponibilidad(self, objeto, cantidad):
		for item, cantidad_disponible in self.cliente.getMochila().bolsilloAbierto:
			if item == objeto:
				return cantidad_disponible >= cantidad
		return False

	def vender(self):#✔✔✔
		objeto = self.cliente.getMochila().abrir_mochila()

		while True:
			cantidad = input(f"{mensaje_game(f"cuantos {objeto.getNombre()} quiere vender\nx.Salir", self.mostrar_inventario, isInput=True)}\n== ")

			if cantidad.lower() == "x":
				return
			
			if self.verificar_disponibilidad(self, objeto, int(cantidad)):
				break
			else:
				mensaje_game(f"no tienen sufucientes {objeto.getNombre()} para vender", self.mostrar_inventario)


		consultar_precio = f"SELECT nombre, precio_compra, precio_venta FROM pokeball UNION SELECT nombre, precio_compra, precio_venta FROM Medicina WHERE nombre = '{objeto.getNombre()}'"
		precio = cursor.execute(consultar_precio).fetchall()[0][2]
		oferta = int(precio)*int(cantidad)
		self.cliente.getMochila().tirar(objeto, int(cantidad))
		mensaje_game(f"has vendido {int(cantidad)} {objeto.getNombre()}, toma tu dinero, {oferta}$", self.mostrar_inventario)
		self.cliente.setDinero(self.cliente.getDinero() + oferta)
		return False



	def salir(self):#✔✔✔
		mensaje_game("Hasta la proxima, vuelve pronto", self.mostrar_inventario)
		return True



	def recibir_jugador(self, cliente):#✔✔✔
		self.cliente = cliente
		mensaje_game(f"Bienvenido a la tienda {cliente.getNombre()}.\n¡Podrias Echar un vistazo a nuestro inventario!", self.mostrar_inventario)
		while True:
			opciones = {
				1:self.comprar,
				2:self.vender,
				3:self.salir
			}
			opcion_elegida = int(input(f"{mensaje_game("¿En que puedo ayudarte?\n1.Comprar\n2.Vender\n3.Salir", self.mostrar_inventario, isInput=True)}\n=="))
			if opcion_elegida in opciones:
				if opciones[opcion_elegida]():
					return
				

	
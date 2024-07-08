from Mochila import *
from Entrenador import *
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



	def comprar(self):#✔✔✔
		while True:
			self.mostrar_inventario()
			eleccion = int(input("Que producto quieres llevarte?\n=="))
			
			if eleccion > 0 or eleccion < len(self.inventario):
				item_comprado = crearItem(self.inventario[eleccion][0])

				cantidad = int(input(f"{self.inventario[eleccion][0]}?, buena eleccion\nCuantas quieres llevarte\n=="))
				print(f"{self.inventario[eleccion-1][0]}?, buena eleccion\nCuantas quieres llevarte\n==")
				cantidad = 54


				if self.cliente.getDinero() >= item_comprado.getPrecioCompra()*cantidad:
					self.cliente.setDinero(self.cliente.getDinero()-item_comprado.getPrecioCompra()*cantidad)
					self.cliente.getBolsa().guardar_objeto(item_comprado, cantidad)

				else:
					print("No tienes suficiente dinero")

			else:
				print("Escoge una un item valido porfavor")

			break
		return False



	def vender(self):#✔✔✔
		objeto = self.cliente.getMochila().abrir_mochila()
		print("cuantos de este elemento quiere vender")
		cantidad = int(input("== "))
		consultar_precio = f"SELECT nombre, precio_compra, precio_venta FROM pokeball UNION SELECT nombre, precio_compra, precio_venta FROM Medicina WHERE nombre = '{objeto.getNombre()}'"
		precio = cursor.execute(consultar_precio).fetchall()[0][2]
		oferta = int(precio)*cantidad
		self.cliente.getMochila().tirar(objeto, cantidad)
		print(f"has vendido {cantidad} {objeto.getNombre()}, toma tu dinero, {oferta}$")
		self.cliente.setDinero(self.cliente.getDinero() + oferta)
		return False



	def salir(self):#✔✔✔
		print("Hasta la proxima, vuelve pronto")
		return True



	def recibir_jugador(self, cliente):#✔✔✔
		self.cliente = cliente
		print(f"Bienvenido a la tienda {cliente.getNombre()}.\n¡Podrias Echar un vistazo a nuestro inventario!")
		while True:
			opciones = {
				1:self.comprar,
				2:self.vender,
				3:self.salir
			}
			opcion_elegida = int(input("¿En que puedo ayudarte?\n1.Comprar\n2.Vender\n3.Salir\n=="))
			if opcion_elegida in opciones:
				if opciones[opcion_elegida]():
					return
class Cliente:
    
    def __init__(self,nombre,mail,ID_usuario,pais,productos=None,ya_realizo_compra=False):
        self.nombre = nombre
        self.mail = mail
        self.ID_usuario = ID_usuario
        self.pais = pais
        self.ya_realizo_compra = ya_realizo_compra

        if productos != None:
            self.productos = productos
        else: 
            self.productos = []

    def __str__(self):
        return f"Cliente {self.nombre}, ID de usuario {self.ID_usuario}"

    def busca(self,producto):
        historial_de_busquedas = open(f"historial{self.ID_usuario}.txt", 'a+')
        historial_de_busquedas.write(f"{producto}")
        historial_de_busquedas.close()

    def compra(self,producto):
        self.productos.append(producto)
        self.ya_realizo_compra = True
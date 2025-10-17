import firebase_admin
from firebase_admin import credentials, db

# conexion con firebase usando las credenciales descargadas
cred = credentials.Certificate(
    "C:/Users/Mi PC/Documents/P.O.O Juan camilo/parcial1-40967-firebase-adminsdk-fbsvc-8ff832549a.json"
)
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://parcial1-40967-default-rtdb.firebaseio.com/"
})
class Libro:
    def __init__(self, titulo, autor, categoria, disponible=True):
        # atributos protegidos con un solo guion bajo
        self._titulo = titulo
        self._autor = autor
        self._categoria = categoria
        self._disponible = disponible

    def get_titulo(self):
        return self._titulo

    def get_autor(self):
        return self._autor

    def get_categoria(self):
        return self._categoria

    def esta_disponible(self):
        return self._disponible

    def prestar(self):
        if self._disponible:
            self._disponible = False
            return True
        return False

    def devolver(self):
        self._disponible = True

    def __str__(self):
        estado = "Disponible" if self._disponible else "Prestado"
        return f"{self._titulo} - {self._autor} ({self._categoria}) - {estado}"


class Usuario:
    def __init__(self, nombre, codigo):
        self._nombre = nombre
        self._codigo = codigo
        self._prestamos = []

    def get_nombre(self):
        return self._nombre

    def get_codigo(self):
        return self._codigo

    def prestar_libro(self, libro: Libro):
        # este metodo presta un libro y actualiza firebase
        if libro.prestar():
            self._prestamos.append(libro)
            print(f"{self._nombre} presto el libro: {libro.get_titulo()}")
            ref = db.reference("libros")  # conexion con firebase
            libros = ref.get()
            for key, value in libros.items():
                # se usa lower para comparar textos sin importar mayusculas o minusculas
                if value["titulo"].lower() == libro.get_titulo().lower():
                    ref.child(key).update({"disponible": False})
        else:
            print(f"el libro {libro.get_titulo()} no esta disponible")

    def devolver_libro(self, libro: Libro):
        # este metodo devuelve un libro y actualiza firebase
        if libro in self._prestamos:
            libro.devolver()
            self._prestamos.remove(libro)
            print(f"{self._nombre} devolvio el libro: {libro.get_titulo()}")
            ref = db.reference("libros")  # conexion con firebase
            libros = ref.get()
            for key, value in libros.items():
                # se usa lower para comparar textos sin importar mayusculas o minusculas
                if value["titulo"].lower() == libro.get_titulo().lower():
                    ref.child(key).update({"disponible": True})
        else:
            print(f"{self._nombre} no tiene prestado el libro {libro.get_titulo()}")

    def __str__(self):
        return f"Usuario: {self._nombre} (Codigo: {self._codigo})"


class Biblioteca:
    def __init__(self, nombre):
        self._nombre = nombre
        self._libros = []
        self._usuarios = []
        self._ref = db.reference(f"bibliotecas/{nombre}")  # conexion con firebase

    def registrar_libro(self, titulo, autor, categoria):
        libro = Libro(titulo, autor, categoria)
        self._libros.append(libro)
        libro_data = {
            "titulo": titulo,
            "autor": autor,
            "categoria": categoria,
            "disponible": True
        }
        self._ref.child("libros").push(libro_data)
        print("libro registrado y guardado en firebase")

    def registrar_usuario(self, nombre, codigo):
        usuario = Usuario(nombre, codigo)
        self._usuarios.append(usuario)
        usuario_data = {
            "nombre": nombre,
            "codigo": codigo
        }
        self._ref.child("usuarios").push(usuario_data)
        print("usuario registrado y guardado en firebase")

    def cargar_datos(self):
        # este metodo carga los datos guardados en firebase al iniciar el programa
        datos = self._ref.get()
        if datos:
            if "libros" in datos:
                for _, v in datos["libros"].items():
                    libro = Libro(v["titulo"], v["autor"], v["categoria"], v["disponible"])
                    self._libros.append(libro)
            if "usuarios" in datos:
                for _, v in datos["usuarios"].items():
                    usuario = Usuario(v["nombre"], v["codigo"])
                    self._usuarios.append(usuario)

    def buscar_libro(self, titulo):
        for libro in self._libros:
            # se usa lower para comparar textos sin importar mayusculas o minusculas
            if libro.get_titulo().lower() == titulo.lower():
                return libro
        return None

    def buscar_usuario(self, codigo):
        for usuario in self._usuarios:
            if usuario.get_codigo() == codigo:
                return usuario
        return None

    def mostrar_libros(self):
        print("\nCatalogo de libros")
        for libro in self._libros:
            print(libro)

    def mostrar_usuarios(self):
        print("\nLista de usuarios")
        for usuario in self._usuarios:
            print(usuario)

    def menu(self):
        # este metodo contiene el menu principal y sus funciones
        while True:
            print("\nMenu Biblioteca")
            print("1. Registrar libro")
            print("2. Registrar usuario")
            print("3. Mostrar catalogo de libros")
            print("4. Mostrar lista de usuarios")
            print("5. Prestar libro")
            print("6. Devolver libro")
            print("7. Salir")

            opcion = input("Seleccione una opcion: ")

            if opcion == "1":
                titulo = input("Titulo del libro: ")
                autor = input("Autor: ")
                categoria = input("Categoria: ")
                self.registrar_libro(titulo, autor, categoria)
            elif opcion == "2":
                nombre = input("Nombre del usuario: ")
                codigo = input("Codigo del usuario: ")
                self.registrar_usuario(nombre, codigo)
            elif opcion == "3":
                self.mostrar_libros()
            elif opcion == "4":
                self.mostrar_usuarios()
            elif opcion == "5":
                codigo = input("Codigo del usuario: ")
                titulo = input("Titulo del libro a prestar: ")
                usuario = self.buscar_usuario(codigo)
                libro = self.buscar_libro(titulo)
                if usuario and libro:
                    usuario.prestar_libro(libro)
                else:
                    print("usuario o libro no encontrado")
            elif opcion == "6":
                codigo = input("Codigo del usuario: ")
                titulo = input("Titulo del libro a devolver: ")
                usuario = self.buscar_usuario(codigo)
                libro = self.buscar_libro(titulo)
                if usuario and libro:
                    usuario.devolver_libro(libro)
                else:
                    print("usuario o libro no encontrado")
            elif opcion == "7":
                print("saliendo del sistema...")
                break
            else:
                print("opcion no valida, intente de nuevo")


# programa principal
if __name__ == "__main__":
    biblioteca = Biblioteca("Biblioteca_UNAL")
    biblioteca.cargar_datos()
    biblioteca.menu()

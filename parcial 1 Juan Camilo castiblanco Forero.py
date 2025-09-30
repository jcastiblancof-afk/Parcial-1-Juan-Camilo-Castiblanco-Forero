#Juan Camilo Castiblanco Forero
# Esta clase se refiere a  un libro en la biblioteca
class Libro:
    def __init__(self, titulo, autor, categoria):
        # Sus atributos son del tipo privados (usando __) para proteger la información y que solo se permita su acceso o su modificación por medio de metodos. solo accesibles solo dentro de la clase
        self.__titulo = titulo         # Título del libro
        self.__autor = autor          # Autor del libro
        self.__categoria = categoria  # Categoria del libro
        self.__disponible = True      # Indica si el libro está disponible (True se coloca por defecto en el caso de que el libro sea nuevo)

    # Mestos son los metodos para acceder a los atributos privados indicados por "__"
    def get_titulo(self):
        return self.__titulo
    
    def get_autor(self):
        return self.__autor
    
    def get_categoria(self):
        return self.__categoria
    
    def esta_disponible(self):
        return self.__disponible

      # este metodo sirve para prestar el libro osea que cambia el estado a no disponible si está disponible
    def prestar(self):
        if self.__disponible:
            self.__disponible = False
            return True
        return False
    
    # este metodo sirve para devolver el libro osea que lo marca como disponible
    def devolver(self):
        self.__disponible = True
        # Representacion en texto del libro, mostrando su estado
    def __str__(self):
        estado = "Disponible" if self.__disponible else "Prestado"
        return f"{self.__titulo} - {self.__autor} ({self.__categoria}) - {estado}"

# esta clase representa un usuario de la biblioteca, sus atributos tambien deben ser privados para proteger la informacion personal y los prestamos.
class Usuario:
    def __init__(self, nombre, codigo):
        self.__nombre = nombre           # Nombre del usuario 
        self.__codigo = codigo           # Un codigo unico para el usuario 
        self.__prestamos = []            # Lista de sus libros prestados 

    # estos metodos sirve para acceder a los atributos privados
    def get_nombre(self):
        return self.__nombre
    
    def get_codigo(self):
        return self.__codigo

    # este metodo es para prestar un libro lo que quiere decir que lo agrega a la lista de prestamos del usuario si se encuentra disponible
    def prestar_libro(self, libro: Libro):
        if libro.prestar():
            self.__prestamos.append(libro)
            print(f"{self.__nombre} ha prestado el libro: {libro.get_titulo()}")
        else:
            print(f"El libro {libro.get_titulo()} no se encuentra disponible.")

    # este metodo es para devolver un libro osea que lo elimina de la lista de préstamos
    def devolver_libro(self, libro: Libro):
        if libro in self.__prestamos:
            libro.devolver()
            self.__prestamos.remove(libro)
            print(f"{self.__nombre} ya devolvio el libro: {libro.get_titulo()}")
        else:
            print(f"{self.__nombre} no tiene prestado el libro {libro.get_titulo()}")

    # Representación en texto del usuario
    def __str__(self):
        return f"Usuario: {self.__nombre} (Codigo: {self.__codigo})"

# esta clase debe administrar los libros y los usuarios, sus atributos tambien son privados para evitar modificaciones externas.
class Biblioteca:
    def __init__(self, nombre):
        self.__nombre = nombre      # Nombre de la biblioteca
        self.__libros = []          # Lista de libros 
        self.__usuarios = []        # Lista de usuarios (todas privadas)

    # este metodo registra un libro nuevo que queda por defecto disponible 
    def registrar_libro(self, titulo, autor, categoria):
        libro = Libro(titulo, autor, categoria)
        self.__libros.append(libro)

    # este metodo registra un usuario nuevo
    def registrar_usuario(self, nombre, codigo):
        usuario = Usuario(nombre, codigo)
        self.__usuarios.append(usuario)

    # este metodo sirve para buscar un libro por su titulo si no existe en el registro no muestra nada
    def buscar_libro(self, titulo):
        for libro in self.__libros:
            if libro.get_titulo().lower() == titulo.lower():
                return libro
        return None

    # este nos permite buscar un usuario por medio de su codigo unico 
    def buscar_usuario(self, codigo):
        for usuario in self.__usuarios:
            if usuario.get_codigo() == codigo:
                return usuario
        return None

    # aqui mostramos todos los libros que han sido registrados 
    def mostrar_libros(self):
        print("\nCatalogo de Libros")
        for libro in self.__libros:
            print(libro)

    # aqui mostramos todos los usuarios que han sido registrados
    def mostrar_usuarios(self):
        print("\nLista de Usuarios")
        for usuario in self.__usuarios:
            print(usuario)

# Aquí se muestra todos los procesos anteriores: 1.se crean libros y usuarios 2.se realizan préstamos y devoluciones  3.se muestra el catálogo actualizado.
if __name__ == "__main__":
    biblioteca = Biblioteca("Biblioteca UNAL")

    # Bucle principal que muestra un menu y ejecuta la opción seleccionada por el usuario
    while True:
        print("\nMenu Biblioteca")  # Título 
        print("1. Registrar libro")  # Opcion para registrar un libro nuevo
        print("2. Registrar usuario")  # Opcion para registrar un usuario nuevo
        print("3. Mostrar catalogo de libros")  # Opcion para mostrar todos los libros
        print("4. Mostrar lista de usuarios")  # Opcion para mostrar todos los usuarios
        print("5. Prestar libro")  # Opcion para prestar un libro a un usuario
        print("6. Devolver libro")  # Opcion para devolver un libro
        print("7. Salir")  # Opcion para salir 
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            # Registrar un libro nuevo
            titulo = input("Título del libro: ")
            autor = input("Autor del libro: ")
            categoria = input("Categoria del libro: ")
            biblioteca.registrar_libro(titulo, autor, categoria)
            print("Libro registrado correctamente.")
        elif opcion == "2":
            # Registrar un usuario nuevo
            nombre = input("Nombre del usuario: ")
            codigo = input("Codigo del usuario: ")
            biblioteca.registrar_usuario(nombre, codigo)
            print("Usuario registrado correctamente.")
        elif opcion == "3":
            # Mostrar todos los libros
            biblioteca.mostrar_libros()
        elif opcion == "4":
            # Mostrar todos los usuarios
            biblioteca.mostrar_usuarios()
        elif opcion == "5":
            # Prestar un libro a un usuario
            codigo = input("Codigo del usuario: ")
            titulo = input("Titulo del libro a prestar: ")
            usuario = biblioteca.buscar_usuario(codigo)
            libro = biblioteca.buscar_libro(titulo)
            if usuario and libro:
                usuario.prestar_libro(libro)
            else:
                print("Usuario o libro no encontrado.")
        elif opcion == "6":
            # Devolver un libro
            codigo = input("Codigo del usuario: ")
            titulo = input("Titulo del libro a devolver: ")
            usuario = biblioteca.buscar_usuario(codigo)
            libro = biblioteca.buscar_libro(titulo)
            if usuario and libro:
                usuario.devolver_libro(libro)
            else:
                print("Usuario o libro no encontrado.")
        elif opcion == "7":
            # Salir 
            print("Saliendo del sistema...")
            break
        else:
            # Opción inválida
            print("Opcion no valida. Intente de nuevo.")
            #todo haciendo uso de lo anterior, las clases, los atributos y las funciones para cada segmento del codigo.
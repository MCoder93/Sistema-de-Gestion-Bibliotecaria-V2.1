# 🐺 Programación en Python

"""
Sistema de Gestión Bibliotecaria con CRUD Completo
Autor: Marcos Soto Z. / MCode-DevOps93
Descripción: Sistema completo para gestionar libros, usuarios y préstamos
con funcionalidades CRUD completas y persistencia en archivos .txt
"""


from datetime import datetime
import os

# ==================== CONFIGURACIÓN GLOBAL ====================
# Directorios para almacenar datos
CARPETA_LIBROS = 'biblioteca/libros/'
CARPETA_USUARIOS = 'biblioteca/usuarios/'
CARPETA_PRESTAMOS = 'biblioteca/prestamos/'
CARPETA_SAVE = 'SAVE/'
EXTENSION = '.txt'


# ==================== CLASE LIBRO ====================
class Libro:
    """
    Clase que representa un libro de la biblioteca
    """
    def __init__(self, id_libro, titulo, autor, editorial, fecha_publicacion, isbn):
        self.id_libro = id_libro
        self.titulo = titulo
        self.autor = autor
        self.editorial = editorial
        self.fecha_publicacion = fecha_publicacion
        self.isbn = isbn
        self.disponible = True

    def __str__(self):
        estado = "Disponible" if self.disponible else "Prestado"
        return f"[{self.id_libro}] {self.titulo} - {self.autor} - {self.editorial} ({self.fecha_publicacion}) [{estado}]"


# ==================== CLASE USUARIO ====================
class Usuario:
    """
    Clase que representa un usuario de la biblioteca
    """
    def __init__(self, id_usuario, nombre, rut, correo, telefono, direccion):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.rut = rut
        self.correo = correo
        self.telefono = telefono
        self.direccion = direccion
        self.prestamos = []

    def __str__(self):
        return f"[{self.id_usuario}] {self.nombre} - RUT: {self.rut} - Tel: {self.telefono} - Préstamos: {len(self.prestamos)}"


# ==================== CLASE PRESTAMO ====================
class Prestamo:
    """
    Clase que representa un préstamo de libro
    """
    def __init__(self, usuario, libro):
        self.usuario = usuario
        self.libro = libro
        self.fecha_prestamo = datetime.now()
        self.fecha_devolucion = None
        self.estado_devolucion = None

    def __str__(self):
        fecha_p = self.fecha_prestamo.strftime("%d/%m/%Y %H:%M")
        if self.fecha_devolucion:
            fecha_d = self.fecha_devolucion.strftime("%d/%m/%Y %H:%M")
            estado_texto = f"✅ Devuelto: {fecha_d}"
            if self.estado_devolucion:
                estado_texto += f" | Estado: {self.estado_devolucion}"
        else:
            estado_texto = "📖 Activo"
        return f"{self.usuario.nombre} → {self.libro.titulo} | Préstamo: {fecha_p} | {estado_texto}"


# ==================== CLASE BIBLIOTECA ====================
class Biblioteca:
    """
    Clase principal que gestiona la biblioteca completa
    """
    def __init__(self):
        self.libros = {}
        self.usuarios = {}
        self.prestamos = []
        self.cargar_datos()

    # ==================== CRUD DE LIBROS ====================

    def agregar_libro(self, id_libro, titulo, autor, editorial, fecha_publicacion, isbn):
        """
        Crear - Agrega un nuevo libro a la biblioteca
        """
        if id_libro in self.libros:
            print("❌ El ID del libro ya existe.")
            return False
        else:
            self.libros[id_libro] = Libro(id_libro, titulo, autor, editorial, fecha_publicacion, isbn)
            self.guardar_libro(id_libro, titulo, autor, editorial, fecha_publicacion, isbn)
            print("✅ Libro agregado correctamente.")
            return True

    def mostrar_libros(self):
        """
        Leer - Muestra todos los libros de la biblioteca
        """
        print("\n" + "="*90)
        print("📚 CATÁLOGO DE LIBROS")
        print("="*90)
        
        if not self.libros:
            print("No hay libros registrados.")
            return
        
        for libro in self.libros.values():
            print(libro)
            print(f"    ISBN: {libro.isbn}")
        
        print("\n" + "="*90)
        print(f"📊 Total de libros: {len(self.libros)}")
        print("="*90)

    def buscar_libro(self, id_libro):
        """
        Leer - Busca y muestra la información de un libro específico
        """
        if id_libro in self.libros:
            libro = self.libros[id_libro]
            print("\n🔍 Libro encontrado:")
            print("="*90)
            print(f"ID: {libro.id_libro}")
            print(f"Título: {libro.titulo}")
            print(f"Autor: {libro.autor}")
            print(f"Editorial: {libro.editorial}")
            print(f"Fecha de Publicación: {libro.fecha_publicacion}")
            print(f"ISBN: {libro.isbn}")
            print(f"Estado: {'Disponible' if libro.disponible else 'Prestado'}")
            print("="*90)
            return libro
        else:
            print("❌ Libro no encontrado.")
            return None

    def editar_libro(self, id_libro):
        """
        Actualizar - Permite editar los datos de un libro existente
        """
        if id_libro not in self.libros:
            print("❌ Libro no encontrado.")
            return False
        
        libro = self.libros[id_libro]
        print(f"\n📝 Editando libro: {libro.titulo}")
        print("(Presiona Enter para mantener el valor actual)")
        
        nuevo_titulo = input(f"Título [{libro.titulo}]: ").strip()
        nuevo_autor = input(f"Autor [{libro.autor}]: ").strip()
        nuevo_editorial = input(f"Editorial [{libro.editorial}]: ").strip()
        nueva_fecha_publicacion = input(f"Fecha de Publicación [{libro.fecha_publicacion}]: ").strip()
        nuevo_isbn = input(f"ISBN [{libro.isbn}]: ").strip()
        
        if nuevo_titulo:
            libro.titulo = nuevo_titulo
        if nuevo_autor:
            libro.autor = nuevo_autor
        if nuevo_editorial:
            libro.editorial = nuevo_editorial
        if nueva_fecha_publicacion:
            libro.fecha_publicacion = nueva_fecha_publicacion
        if nuevo_isbn:
            libro.isbn = nuevo_isbn
        
        self.actualizar_libro(libro)
        print("✅ Libro actualizado correctamente.")
        return True

    def eliminar_libro(self, id_libro):
        """
        Eliminar - Elimina un libro de la biblioteca
        """
        if id_libro not in self.libros:
            print("❌ Libro no encontrado.")
            return False
        
        libro = self.libros[id_libro]
        
        if not libro.disponible:
            print("⚠️ No se puede eliminar un libro que está prestado.")
            print("   Por favor, espere a que sea devuelto.")
            return False
        
        confirmacion = input(f"¿Está seguro de eliminar '{libro.titulo}'? (s/n): ").strip().lower()
        
        if confirmacion == 's':
            del self.libros[id_libro]
            try:
                os.remove(CARPETA_LIBROS + id_libro + EXTENSION)
                print("✅ Libro eliminado correctamente.")
                return True
            except OSError as e:
                print(f"⚠️ Error al eliminar el archivo: {e}")
                return False
        else:
            print("❌ Eliminación cancelada.")
            return False

    # ==================== CRUD DE USUARIOS ====================

    def registrar_usuario(self, id_usuario, nombre, rut, correo, telefono, direccion):
        """
        Crear - Registra un nuevo usuario en la biblioteca
        """
        if id_usuario in self.usuarios:
            print("❌ El ID del usuario ya existe.")
            return False
        else:
            self.usuarios[id_usuario] = Usuario(id_usuario, nombre, rut, correo, telefono, direccion)
            self.guardar_usuario(id_usuario, nombre, rut, correo, telefono, direccion)
            print("✅ Usuario registrado correctamente.")
            return True

    def mostrar_usuarios(self):
        """
        Leer - Muestra todos los usuarios registrados
        """
        print("\n" + "="*90)
        print("👥 LISTA DE USUARIOS")
        print("="*90)
        
        if not self.usuarios:
            print("No hay usuarios registrados.")
            return
        
        for usuario in self.usuarios.values():
            print(usuario)
            print(f"    Correo: {usuario.correo} | Dirección: {usuario.direccion}")
        
        print("\n" + "="*90)
        print(f"📊 Total de usuarios: {len(self.usuarios)}")
        print("="*90)

    def buscar_usuario(self, id_usuario):
        """
        Leer - Busca y muestra la información de un usuario específico
        """
        if id_usuario in self.usuarios:
            usuario = self.usuarios[id_usuario]
            print("\n🔍 Usuario encontrado:")
            print("="*90)
            print(f"ID: {usuario.id_usuario}")
            print(f"Nombre: {usuario.nombre}")
            print(f"RUT: {usuario.rut}")
            print(f"Correo: {usuario.correo}")
            print(f"Teléfono: {usuario.telefono}")
            print(f"Dirección: {usuario.direccion}")
            print(f"Préstamos activos: {len(usuario.prestamos)}")
            
            if usuario.prestamos:
                print("\nLibros prestados:")
                for prestamo in usuario.prestamos:
                    print(f"  - {prestamo.libro.titulo}")
            
            print("="*90)
            return usuario
        else:
            print("❌ Usuario no encontrado.")
            return None

    def editar_usuario(self, id_usuario):
        """
        Actualizar - Permite editar los datos de un usuario existente
        """
        if id_usuario not in self.usuarios:
            print("❌ Usuario no encontrado.")
            return False
        
        usuario = self.usuarios[id_usuario]
        print(f"\n📝 Editando usuario: {usuario.nombre}")
        print("(Presiona Enter para mantener el valor actual)")
        
        nuevo_nombre = input(f"Nombre [{usuario.nombre}]: ").strip()
        nuevo_rut = input(f"RUT [{usuario.rut}]: ").strip()
        nuevo_correo = input(f"Correo [{usuario.correo}]: ").strip()
        nuevo_telefono = input(f"Teléfono [{usuario.telefono}]: ").strip()
        nueva_direccion = input(f"Dirección [{usuario.direccion}]: ").strip()
        
        if nuevo_nombre:
            usuario.nombre = nuevo_nombre
        if nuevo_rut:
            usuario.rut = nuevo_rut
        if nuevo_correo:
            usuario.correo = nuevo_correo
        if nuevo_telefono:
            usuario.telefono = nuevo_telefono
        if nueva_direccion:
            usuario.direccion = nueva_direccion
        
        self.guardar_usuario(id_usuario, usuario.nombre, usuario.rut, usuario.correo, usuario.telefono, usuario.direccion)
        print("✅ Usuario actualizado correctamente.")
        return True

    def eliminar_usuario(self, id_usuario):
        """
        Eliminar - Elimina un usuario de la biblioteca
        """
        if id_usuario not in self.usuarios:
            print("❌ Usuario no encontrado.")
            return False
        
        usuario = self.usuarios[id_usuario]
        
        if len(usuario.prestamos) > 0:
            print("⚠️ No se puede eliminar un usuario con préstamos activos.")
            print(f"   El usuario tiene {len(usuario.prestamos)} libro(s) prestado(s).")
            return False
        
        confirmacion = input(f"¿Está seguro de eliminar a '{usuario.nombre}'? (s/n): ").strip().lower()
        
        if confirmacion == 's':
            del self.usuarios[id_usuario]
            try:
                os.remove(CARPETA_USUARIOS + id_usuario + EXTENSION)
                print("✅ Usuario eliminado correctamente.")
                return True
            except OSError as e:
                print(f"⚠️ Error al eliminar el archivo: {e}")
                return False
        else:
            print("❌ Eliminación cancelada.")
            return False

    # ==================== GESTIÓN DE PRÉSTAMOS ====================

    def prestar_libro(self, id_usuario, id_libro):
        """
        Registra un préstamo de libro a un usuario
        """
        if id_usuario not in self.usuarios:
            print("❌ Usuario no encontrado.")
            return
        if id_libro not in self.libros:
            print("❌ Libro no encontrado.")
            return

        libro = self.libros[id_libro]
        usuario = self.usuarios[id_usuario]

        if not libro.disponible:
            print("⚠️ El libro ya está prestado.")
            return

        prestamo = Prestamo(usuario, libro)
        libro.disponible = False
        usuario.prestamos.append(prestamo)
        self.prestamos.append(prestamo)
        
        self.guardar_prestamo(prestamo)
        self.actualizar_libro(libro)
        
        print("✅ Préstamo registrado con éxito.")

    def devolver_libro(self, id_libro):
        """
        Registra la devolución de un libro con su estado
        """
        if id_libro not in self.libros:
            print("❌ Libro no encontrado.")
            return

        libro = self.libros[id_libro]
        if libro.disponible:
            print("⚠️ Este libro no está prestado.")
            return

        prestamo_activo = None
        for prestamo in self.prestamos:
            if prestamo.libro.id_libro == id_libro and prestamo.fecha_devolucion is None:
                prestamo_activo = prestamo
                break
        
        if prestamo_activo:
            print("\n" + "="*90)
            print("📖 INFORMACIÓN DEL PRÉSTAMO")
            print("="*90)
            print(f"Usuario: {prestamo_activo.usuario.nombre}")
            print(f"Libro: {prestamo_activo.libro.titulo}")
            print(f"Fecha de préstamo: {prestamo_activo.fecha_prestamo.strftime('%d/%m/%Y %H:%M')}")
            print("="*90)
            
            estado_devolucion = input("\nEstado de devolución del libro: ").strip()
            if not estado_devolucion:
                estado_devolucion = "Sin observaciones"
            
            prestamo_activo.fecha_devolucion = datetime.now()
            prestamo_activo.estado_devolucion = estado_devolucion
            
            try:
                prestamo_activo.usuario.prestamos.remove(prestamo_activo)
            except ValueError:
                pass
            
            self.actualizar_prestamo(prestamo_activo)
        
        libro.disponible = True
        self.actualizar_libro(libro)
        
        print("\n" + "="*90)
        print("✅ Libro devuelto correctamente.")
        print(f"📝 Estado registrado: {estado_devolucion}")
        print("="*90)

    def mostrar_prestamos(self):
        """
        Muestra el historial de préstamos
        """
        print("\n" + "="*100)
        print("📋 HISTORIAL DE PRÉSTAMOS")
        print("="*100)
        
        if not self.prestamos:
            print("No hay préstamos registrados.")
            return
        
        for prestamo in self.prestamos:
            print(prestamo)
        
        print("\n" + "="*100)
        print(f"📊 Total de préstamos: {len(self.prestamos)}")
        prestamos_activos = sum(1 for p in self.prestamos if p.fecha_devolucion is None)
        prestamos_devueltos = sum(1 for p in self.prestamos if p.fecha_devolucion is not None)
        print(f"📖 Activos: {prestamos_activos} | ✅ Devueltos: {prestamos_devueltos}")
        print("="*100)

    def guardar_historial_prestamos(self):
        """
        Guarda el historial de préstamos en un archivo dentro de SAVE con subcarpeta por fecha
        """
        if not self.prestamos:
            print("❌ No hay préstamos registrados para guardar.")
            return
        
        try:
            if not os.path.exists(CARPETA_SAVE):
                os.makedirs(CARPETA_SAVE)
            
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            ruta_fecha = os.path.join(CARPETA_SAVE, fecha_actual)
            
            if not os.path.exists(ruta_fecha):
                os.makedirs(ruta_fecha)
            
            hora_actual = datetime.now().strftime("%H-%M-%S")
            nombre_archivo = f"historial_prestamos_{hora_actual}{EXTENSION}"
            ruta_completa = os.path.join(ruta_fecha, nombre_archivo)
            
            with open(ruta_completa, 'w', encoding='utf-8') as archivo:
                archivo.write("="*100 + "\n")
                archivo.write(f"HISTORIAL DE PRÉSTAMOS - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                archivo.write("="*100 + "\n\n")
                
                for idx, prestamo in enumerate(self.prestamos, 1):
                    archivo.write(f"--- PRÉSTAMO #{idx} ---\n")
                    archivo.write(f"Usuario ID: {prestamo.usuario.id_usuario}\n")
                    archivo.write(f"Usuario Nombre: {prestamo.usuario.nombre}\n")
                    archivo.write(f"Usuario RUT: {prestamo.usuario.rut}\n")
                    archivo.write(f"Usuario Correo: {prestamo.usuario.correo}\n")
                    archivo.write(f"Usuario Teléfono: {prestamo.usuario.telefono}\n")
                    archivo.write(f"\n")
                    archivo.write(f"Libro ID: {prestamo.libro.id_libro}\n")
                    archivo.write(f"Libro Título: {prestamo.libro.titulo}\n")
                    archivo.write(f"Libro Autor: {prestamo.libro.autor}\n")
                    archivo.write(f"Libro ISBN: {prestamo.libro.isbn}\n")
                    archivo.write(f"\n")
                    archivo.write(f"Fecha Préstamo: {prestamo.fecha_prestamo.strftime('%d/%m/%Y %H:%M:%S')}\n")
                    
                    if prestamo.fecha_devolucion:
                        archivo.write(f"Fecha Devolución: {prestamo.fecha_devolucion.strftime('%d/%m/%Y %H:%M:%S')}\n")
                        archivo.write(f"Estado Devolución: {prestamo.estado_devolucion}\n")
                    else:
                        archivo.write(f"Estado: 📖 ACTIVO\n")
                    
                    archivo.write("\n")
                
                archivo.write("="*100 + "\n")
                archivo.write(f"RESUMEN:\n")
                prestamos_activos = sum(1 for p in self.prestamos if p.fecha_devolucion is None)
                prestamos_devueltos = sum(1 for p in self.prestamos if p.fecha_devolucion is not None)
                archivo.write(f"Total de préstamos: {len(self.prestamos)}\n")
                archivo.write(f"Préstamos activos: {prestamos_activos}\n")
                archivo.write(f"Préstamos devueltos: {prestamos_devueltos}\n")
                archivo.write("="*100 + "\n")
            
            print("\n" + "="*90)
            print("✅ Historial de préstamos guardado correctamente.")
            print(f"📁 Ubicación: {ruta_completa}")
            print(f"📊 Total de préstamos guardados: {len(self.prestamos)}")
            print("="*90)
            
        except Exception as e:
            print(f"❌ Error al guardar el historial: {e}")

    def eliminar_historial_prestamos(self):
        """
        Elimina completamente el historial de préstamos
        """
        print("\n" + "="*70)
        print("⚠️  ELIMINAR HISTORIAL DE PRÉSTAMOS")
        print("="*70)
        
        if not self.prestamos:
            print("❌ No hay préstamos registrados para eliminar.")
            return
        
        total_prestamos = len(self.prestamos)
        prestamos_activos = sum(1 for p in self.prestamos if p.fecha_devolucion is None)
        
        print(f"\n📊 Total de préstamos registrados: {total_prestamos}")
        print(f"📖 Préstamos activos: {prestamos_activos}")
        print(f"✅ Préstamos devueltos: {total_prestamos - prestamos_activos}")
        
        if prestamos_activos > 0:
            print("\n⚠️  ADVERTENCIA: Hay préstamos activos.")
            print("   Si elimina el historial, se perderá el registro de estos préstamos,")
            print("   pero los libros seguirán marcados como prestados.")
        
        print("\n🗑️  Esta acción eliminará TODOS los archivos de préstamos del directorio.")
        confirmacion = input("\n¿Está seguro de eliminar TODO el historial? (s/n): ").strip().lower()
        
        if confirmacion == 's':
            try:
                archivos_eliminados = 0
                if os.path.exists(CARPETA_PRESTAMOS):
                    archivos = os.listdir(CARPETA_PRESTAMOS)
                    for archivo in archivos:
                        if archivo.endswith(EXTENSION):
                            os.remove(CARPETA_PRESTAMOS + archivo)
                            archivos_eliminados += 1
                
                self.prestamos.clear()
                
                for usuario in self.usuarios.values():
                    usuario.prestamos.clear()
                
                print(f"\n✅ Historial eliminado correctamente.")
                print(f"📁 {archivos_eliminados} archivo(s) eliminado(s) del directorio.")
                
            except Exception as e:
                print(f"\n❌ Error al eliminar el historial: {e}")
        else:
            print("\n❌ Eliminación cancelada.")

    # ==================== FUNCIONES DE PERSISTENCIA ====================

    def guardar_libro(self, id_libro, titulo, autor, editorial, fecha_publicacion, isbn):
        """Guarda un libro en archivo .txt"""
        with open(CARPETA_LIBROS + id_libro + EXTENSION, 'w', encoding='utf-8') as archivo:
            archivo.write(f'ID: {id_libro}\n')
            archivo.write(f'Título: {titulo}\n')
            archivo.write(f'Autor: {autor}\n')
            archivo.write(f'Editorial: {editorial}\n')
            archivo.write(f'Fecha Publicación: {fecha_publicacion}\n')
            archivo.write(f'ISBN: {isbn}\n')
            archivo.write(f'Disponible: True\n')

    def actualizar_libro(self, libro):
        """Actualiza el estado de disponibilidad de un libro"""
        with open(CARPETA_LIBROS + libro.id_libro + EXTENSION, 'w', encoding='utf-8') as archivo:
            archivo.write(f'ID: {libro.id_libro}\n')
            archivo.write(f'Título: {libro.titulo}\n')
            archivo.write(f'Autor: {libro.autor}\n')
            archivo.write(f'Editorial: {libro.editorial}\n')
            archivo.write(f'Fecha Publicación: {libro.fecha_publicacion}\n')
            archivo.write(f'ISBN: {libro.isbn}\n')
            archivo.write(f'Disponible: {libro.disponible}\n')

    def guardar_usuario(self, id_usuario, nombre, rut, correo, telefono, direccion):
        """Guarda un usuario en archivo .txt"""
        with open(CARPETA_USUARIOS + id_usuario + EXTENSION, 'w', encoding='utf-8') as archivo:
            archivo.write(f'ID: {id_usuario}\n')
            archivo.write(f'Nombre: {nombre}\n')
            archivo.write(f'RUT: {rut}\n')
            archivo.write(f'Correo: {correo}\n')
            archivo.write(f'Teléfono: {telefono}\n')
            archivo.write(f'Dirección: {direccion}\n')
            archivo.write(f'Fecha Registro: {datetime.now().strftime("%d/%m/%Y %H:%M")}\n')

    def guardar_prestamo(self, prestamo):
        """Guarda un préstamo en archivo .txt"""
        nombre_archivo = f'{prestamo.usuario.id_usuario}_{prestamo.libro.id_libro}_{prestamo.fecha_prestamo.strftime("%Y%m%d%H%M%S")}'
        with open(CARPETA_PRESTAMOS + nombre_archivo + EXTENSION, 'w', encoding='utf-8') as archivo:
            archivo.write(f'Usuario ID: {prestamo.usuario.id_usuario}\n')
            archivo.write(f'Usuario Nombre: {prestamo.usuario.nombre}\n')
            archivo.write(f'Libro ID: {prestamo.libro.id_libro}\n')
            archivo.write(f'Libro Título: {prestamo.libro.titulo}\n')
            archivo.write(f'Fecha Préstamo: {prestamo.fecha_prestamo.strftime("%d/%m/%Y %H:%M")}\n')
            if prestamo.fecha_devolucion:
                archivo.write(f'Fecha Devolución: {prestamo.fecha_devolucion.strftime("%d/%m/%Y %H:%M")}\n')
            if prestamo.estado_devolucion:
                archivo.write(f'Estado Devolución: {prestamo.estado_devolucion}\n')

    def actualizar_prestamo(self, prestamo):
        """Actualiza un préstamo existente en archivo .txt"""
        nombre_archivo = f'{prestamo.usuario.id_usuario}_{prestamo.libro.id_libro}_{prestamo.fecha_prestamo.strftime("%Y%m%d%H%M%S")}'
        with open(CARPETA_PRESTAMOS + nombre_archivo + EXTENSION, 'w', encoding='utf-8') as archivo:
            archivo.write(f'Usuario ID: {prestamo.usuario.id_usuario}\n')
            archivo.write(f'Usuario Nombre: {prestamo.usuario.nombre}\n')
            archivo.write(f'Libro ID: {prestamo.libro.id_libro}\n')
            archivo.write(f'Libro Título: {prestamo.libro.titulo}\n')
            archivo.write(f'Fecha Préstamo: {prestamo.fecha_prestamo.strftime("%d/%m/%Y %H:%M")}\n')
            if prestamo.fecha_devolucion:
                archivo.write(f'Fecha Devolución: {prestamo.fecha_devolucion.strftime("%d/%m/%Y %H:%M")}\n')
            if prestamo.estado_devolucion:
                archivo.write(f'Estado Devolución: {prestamo.estado_devolucion}\n')

    def cargar_datos(self):
        """Carga todos los datos desde archivos al iniciar"""
        self.cargar_libros()
        self.cargar_usuarios()
        self.cargar_prestamos()

    def cargar_libros(self):
        """Carga libros desde archivos"""
        if not os.path.exists(CARPETA_LIBROS):
            return

        archivos = os.listdir(CARPETA_LIBROS)
        for archivo in archivos:
            if archivo.endswith(EXTENSION):
                try:
                    with open(CARPETA_LIBROS + archivo, 'r', encoding='utf-8') as f:
                        lineas = f.readlines()
                        id_libro = lineas[0].split(': ')[1].strip()
                        titulo = lineas[1].split(': ')[1].strip()
                        autor = lineas[2].split(': ')[1].strip()
                        editorial = lineas[3].split(': ')[1].strip()
                        fecha_publicacion = lineas[4].split(': ')[1].strip()
                        isbn = lineas[5].split(': ')[1].strip()
                        disponible = lineas[6].split(': ')[1].strip() == 'True'
                        
                        libro = Libro(id_libro, titulo, autor, editorial, fecha_publicacion, isbn)
                        libro.disponible = disponible
                        self.libros[id_libro] = libro
                except Exception as e:
                    print(f"Error cargando libro {archivo}: {e}")

    def cargar_usuarios(self):
        """Carga usuarios desde archivos"""
        if not os.path.exists(CARPETA_USUARIOS):
            return

        archivos = os.listdir(CARPETA_USUARIOS)
        for archivo in archivos:
            if archivo.endswith(EXTENSION):
                try:
                    with open(CARPETA_USUARIOS + archivo, 'r', encoding='utf-8') as f:
                        lineas = f.readlines()
                        id_usuario = lineas[0].split(': ')[1].strip()
                        nombre = lineas[1].split(': ')[1].strip()
                        rut = lineas[2].split(': ')[1].strip()
                        correo = lineas[3].split(': ')[1].strip()
                        telefono = lineas[4].split(': ')[1].strip()
                        direccion = lineas[5].split(': ')[1].strip()
                        
                        self.usuarios[id_usuario] = Usuario(id_usuario, nombre, rut, correo, telefono, direccion)
                except Exception as e:
                    print(f"Error cargando usuario {archivo}: {e}")

    def cargar_prestamos(self):
        """Carga préstamos desde archivos"""
        if not os.path.exists(CARPETA_PRESTAMOS):
            return

        archivos = os.listdir(CARPETA_PRESTAMOS)
        for archivo in archivos:
            if archivo.endswith(EXTENSION):
                try:
                    with open(CARPETA_PRESTAMOS + archivo, 'r', encoding='utf-8') as f:
                        lineas = f.readlines()
                        id_usuario = lineas[0].split(': ')[1].strip()
                        nombre_usuario = lineas[1].split(': ')[1].strip()
                        id_libro = lineas[2].split(': ')[1].strip()
                        titulo_libro = lineas[3].split(': ')[1].strip()
                        fecha_prestamo_str = lineas[4].split(': ')[1].strip()
                        fecha_devolucion_str = None
                        estado_devolucion = None
                        
                        if len(lineas) > 5:
                            if lineas[5].startswith('Fecha Devolución:'):
                                fecha_devolucion_str = lineas[5].split(': ')[1].strip()
                        
                        if len(lineas) > 6:
                            if lineas[6].startswith('Estado Devolución:'):
                                estado_devolucion = lineas[6].split(': ')[1].strip()
                        
                        if id_usuario in self.usuarios and id_libro in self.libros:
                            usuario = self.usuarios[id_usuario]
                            libro = self.libros[id_libro]
                            prestamo = Prestamo(usuario, libro)
                            
                            prestamo.fecha_prestamo = datetime.strptime(fecha_prestamo_str, "%d/%m/%Y %H:%M")
                            
                            if fecha_devolucion_str:
                                prestamo.fecha_devolucion = datetime.strptime(fecha_devolucion_str, "%d/%m/%Y %H:%M")
                            
                            if estado_devolucion:
                                prestamo.estado_devolucion = estado_devolucion
                            
                            self.prestamos.append(prestamo)
                            
                            if not prestamo.fecha_devolucion:
                                usuario.prestamos.append(prestamo)
                except Exception as e:
                    print(f"Error cargando préstamo {archivo}: {e}")


# ==================== FUNCIONES AUXILIARES ====================

def crear_directorios():
    """Crea los directorios necesarios para almacenar datos"""
    directorios = [CARPETA_LIBROS, CARPETA_USUARIOS, CARPETA_PRESTAMOS, CARPETA_SAVE]
    for directorio in directorios:
        if not os.path.exists(directorio):
            os.makedirs(directorio)


def mostrar_menu():
    """Muestra el menú principal del sistema"""
    print("\n" + "="*70)
    print('🐺🐰 Bienvenidos a la Biblioteca WolfRabbit 🐺🐰')
    print("="*70)
    print("\n--- GESTIÓN DE LIBROS (CRUD) ---")
    print("1.  Agregar Libro")
    print("2.  Buscar Libro")
    print("3.  Editar Libro")
    print("4.  Eliminar Libro")
    print("5.  Mostrar Catálogo Completo")
    print("\n--- GESTIÓN DE USUARIOS (CRUD) ---")
    print("6.  Registrar Usuario")
    print("7.  Buscar Usuario")
    print("8.  Editar Usuario")
    print("9.  Eliminar Usuario")
    print("10. Mostrar Todos los Usuarios")
    print("\n--- GESTIÓN DE PRÉSTAMOS ---")
    print("11. Prestar Libro")
    print("12. Devolver Libro (con Estado)")
    print("13. Mostrar Historial de Préstamos")
    print("14. Guardar Historial en SAVE")
    print("15. Eliminar Historial de Préstamos")
    print("\n--- SISTEMA ---")
    print("0.  Salir del Sistema")
    print("="*70)


# ==================== FUNCIÓN PRINCIPAL ====================

def app():
    """
    Función principal que ejecuta el sistema de biblioteca
    """
    crear_directorios()
    biblio = Biblioteca()
    
    print("✅ Sistema de biblioteca iniciado correctamente.")
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\nSeleccione una opción (0-15): ").strip()
            
            # ===== GESTIÓN DE LIBROS =====
            if opcion == '1':
                print("\n--- AGREGAR LIBRO ---")
                id_libro = input("ID del libro: ").strip()
                titulo = input("Título: ").strip()
                autor = input("Autor: ").strip()
                editorial = input("Editorial: ").strip()
                fecha_publicacion = input("Fecha de Publicación (ej: 2023): ").strip()
                isbn = input("ISBN: ").strip()
                biblio.agregar_libro(id_libro, titulo, autor, editorial, fecha_publicacion, isbn)
            
            elif opcion == '2':
                print("\n--- BUSCAR LIBRO ---")
                id_libro = input("ID del libro: ").strip()
                biblio.buscar_libro(id_libro)
            
            elif opcion == '3':
                print("\n--- EDITAR LIBRO ---")
                id_libro = input("ID del libro a editar: ").strip()
                biblio.editar_libro(id_libro)
            
            elif opcion == '4':
                print("\n--- ELIMINAR LIBRO ---")
                id_libro = input("ID del libro a eliminar: ").strip()
                biblio.eliminar_libro(id_libro)
            
            elif opcion == '5':
                biblio.mostrar_libros()
            
            # ===== GESTIÓN DE USUARIOS =====
            elif opcion == '6':
                print("\n--- REGISTRAR USUARIO ---")
                id_usuario = input("ID del usuario: ").strip()
                nombre = input("Nombre completo: ").strip()
                rut = input("RUT (ej: 12.345.678-9): ").strip()
                correo = input("Correo electrónico: ").strip()
                telefono = input("Teléfono: ").strip()
                direccion = input("Dirección: ").strip()
                biblio.registrar_usuario(id_usuario, nombre, rut, correo, telefono, direccion)
            
            elif opcion == '7':
                print("\n--- BUSCAR USUARIO ---")
                id_usuario = input("ID del usuario: ").strip()
                biblio.buscar_usuario(id_usuario)
            
            elif opcion == '8':
                print("\n--- EDITAR USUARIO ---")
                id_usuario = input("ID del usuario a editar: ").strip()
                biblio.editar_usuario(id_usuario)
            
            elif opcion == '9':
                print("\n--- ELIMINAR USUARIO ---")
                id_usuario = input("ID del usuario a eliminar: ").strip()
                biblio.eliminar_usuario(id_usuario)
            
            elif opcion == '10':
                biblio.mostrar_usuarios()
            
            # ===== GESTIÓN DE PRÉSTAMOS =====
            elif opcion == '11':
                print("\n--- PRESTAR LIBRO ---")
                id_usuario = input("ID del usuario: ").strip()
                id_libro = input("ID del libro: ").strip()
                biblio.prestar_libro(id_usuario, id_libro)
            
            elif opcion == '12':
                print("\n--- DEVOLVER LIBRO ---")
                id_libro = input("ID del libro: ").strip()
                biblio.devolver_libro(id_libro)
            
            elif opcion == '13':
                biblio.mostrar_prestamos()
            
            elif opcion == '14':
                biblio.guardar_historial_prestamos()
            
            elif opcion == '15':
                biblio.eliminar_historial_prestamos()
            
            # ===== SALIR =====
            elif opcion == '0':
                print("\n" + "="*70)
                print("👋 ¡Gracias por usar el sistema de biblioteca!")
                print("📁 Todos los datos han sido guardados correctamente.")
                print("\n By: MCode-DevOps93 🐺")
                print("="*70)
                break
            
            else:
                print("❌ Opción inválida. Por favor seleccione entre 0-15.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Sistema cerrado por el usuario.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


# ==================== PUNTO DE ENTRADA ====================
if __name__ == "__main__":
    app()


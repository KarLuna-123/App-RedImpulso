import csv
import os
import hashlib
import uuid
from typing import List, Optional, Dict, Union
from datetime import datetime

DATA_FOLDER = r"C:/Users/carme/OneDrive/Documentos/Programav1"
FILES = {
    "usuarios": "usuarios.csv",
    "solicitudes": "solicitudes.csv",
    "bitacoras": "bitacoras.csv"
}

HEADERS = {
    "usuarios": ["id", "nombre", "correo", "password_hash", "tipo", "carrera"],
    "solicitudes": ["id", "titulo", "descripcion", "beneficiario_id", "estado", "estudiante_asignado_id", "postulados_ids"],
    "bitacoras": ["id", "estudiante_id", "actividad", "horas", "fecha", "completada"]
}

# SEGURIDAD
class Security:
    @staticmethod
    def hash_password(password: str) -> str:
        """Genera un hash SHA-256 para la contraseña."""
        return hashlib.sha256(password.encode()).hexdigest()

# MODELOS
class Usuario:
    def __init__(self, id: str, nombre: str, correo: str, password_hash: str, tipo: str):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.password_hash = password_hash
        self.tipo = tipo

    def verificar_password(self, password: str) -> bool:
        return self.password_hash == Security.hash_password(password)

class Estudiante(Usuario):
    def __init__(self, id: str, nombre: str, correo: str, password_hash: str, carrera: str):
        super().__init__(id, nombre, correo, password_hash, "estudiante")
        self.carrera = carrera

class Beneficiario(Usuario):
    def __init__(self, id: str, nombre: str, correo: str, password_hash: str):
        super().__init__(id, nombre, correo, password_hash, "beneficiario")

class Solicitud:
    def __init__(self, id: str, titulo: str, descripcion: str, beneficiario_id: str, 
                 estado: str = "Disponible", estudiante_asignado_id: str = "", 
                 postulados_ids: List[str] = None):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.beneficiario_id = beneficiario_id
        self.estado = estado
        self.estudiante_asignado_id = estudiante_asignado_id
        self.postulados_ids = postulados_ids if postulados_ids else []

class BitacoraEntry:
    def __init__(self, id: str, estudiante_id: str, actividad: str, horas: float, 
                 fecha: str, completada: bool = False):
        self.id = id
        self.estudiante_id = estudiante_id
        self.actividad = actividad
        self.horas = horas
        self.fecha = fecha
        self.completada = completada

# MANEJADOR DE PERSISTENCIA
class PersistenceManager:
    @staticmethod
    def initialize_files():
        """Crea los archivos CSV si no existen."""
        for key, filename in FILES.items():
            if not os.path.exists(filename):
                with open(filename, mode='w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(HEADERS[key])

    @staticmethod
    def load_users() -> List[Usuario]:
        users = []
        try:
            with open(FILES["usuarios"], mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row["tipo"] == "estudiante":
                        users.append(Estudiante(row["id"], row["nombre"], row["correo"], 
                                               row["password_hash"], row["carrera"]))
                    else:
                        users.append(Beneficiario(row["id"], row["nombre"], row["correo"], 
                                                 row["password_hash"]))
        except Exception as e:
            print(f"Error cargando usuarios: {e}")
        return users

    @staticmethod
    def save_users(users: List[Usuario]):
        with open(FILES["usuarios"], mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS["usuarios"], quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            for u in users:
                data = {
                    "id": u.id, "nombre": u.nombre, "correo": u.correo, 
                    "password_hash": u.password_hash, "tipo": u.tipo,
                    "carrera": getattr(u, "carrera", "")
                }
                writer.writerow(data)

    @staticmethod
    def load_solicitudes() -> List[Solicitud]:
        solicitudes = []
        try:
            with open(FILES["solicitudes"], mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    postulados = row["postulados_ids"].split(";") if row["postulados_ids"] else []
                    solicitudes.append(Solicitud(row["id"], row["titulo"], row["descripcion"], 
                                               row["beneficiario_id"], row["estado"], 
                                               row["estudiante_asignado_id"], postulados))
        except Exception as e:
            print(f"Error cargando solicitudes: {e}")
        return solicitudes

    @staticmethod
    def save_solicitudes(solicitudes: List[Solicitud]):
        with open(FILES["solicitudes"], mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS["solicitudes"], quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            for s in solicitudes:
                writer.writerow({
                    "id": s.id, "titulo": s.titulo, "descripcion": s.descripcion,
                    "beneficiario_id": s.beneficiario_id, "estado": s.estado,
                    "estudiante_asignado_id": s.estudiante_asignado_id,
                    "postulados_ids": ";".join(s.postulados_ids)
                })

    @staticmethod
    def load_bitacoras() -> List[BitacoraEntry]:
        bitacoras = []
        try:
            with open(FILES["bitacoras"], mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    bitacoras.append(BitacoraEntry(row["id"], row["estudiante_id"], 
                                                 row["actividad"], float(row["horas"]), 
                                                 row["fecha"], row["completada"] == "True"))
        except Exception as e:
            print(f"Error cargando bitácoras: {e}")
        return bitacoras

    @staticmethod
    def save_bitacoras(bitacoras: List[BitacoraEntry]):
        with open(FILES["bitacoras"], mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS["bitacoras"], quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            for b in bitacoras:
                writer.writerow({
                    "id": b.id, "estudiante_id": b.estudiante_id, "actividad": b.actividad,
                    "horas": b.horas, "fecha": b.fecha, "completada": str(b.completada)
                })

# SISTEMA
class Sistema:
    def __init__(self):
        PersistenceManager.initialize_files()
        self.usuarios = PersistenceManager.load_users()
        self.solicitudes = PersistenceManager.load_solicitudes()
        self.bitacoras = PersistenceManager.load_bitacoras()

    def registrar_usuario(self, nombre, correo, password, tipo, carrera="") -> bool:
        # Validar duplicados
        if any(u.correo == correo for u in self.usuarios):
            return False
        
        user_id = str(uuid.uuid4())[:8]
        pw_hash = Security.hash_password(password)
        
        if tipo == "estudiante":
            nuevo = Estudiante(user_id, nombre, correo, pw_hash, carrera)
        else:
            nuevo = Beneficiario(user_id, nombre, correo, pw_hash)
            
        self.usuarios.append(nuevo)
        PersistenceManager.save_users(self.usuarios)
        return True

    def login(self, correo, password) -> Optional[Usuario]:
        for u in self.usuarios:
            if u.correo == correo and u.verificar_password(password):
                return u
        return None

    def crear_solicitud(self, titulo, descripcion, beneficiario_id):
        sol_id = str(uuid.uuid4())[:8]
        nueva = Solicitud(sol_id, titulo, descripcion, beneficiario_id)
        self.solicitudes.append(nueva)
        PersistenceManager.save_solicitudes(self.solicitudes)

    def postular_estudiante(self, solicitud_id, estudiante_id):
        for s in self.solicitudes:
            if s.id == solicitud_id and estudiante_id not in s.postulados_ids:
                s.postulados_ids.append(estudiante_id)
                PersistenceManager.save_solicitudes(self.solicitudes)
                return True
        return False

    def asignar_estudiante(self, solicitud_id, estudiante_id):
        for s in self.solicitudes:
            if s.id == solicitud_id:
                s.estado = "Asignada"
                s.estudiante_asignado_id = estudiante_id
                PersistenceManager.save_solicitudes(self.solicitudes)
                return True
        return False

    def registrar_actividad(self, estudiante_id, actividad, horas, completada=False):
        bit_id = str(uuid.uuid4())[:8]
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        nueva = BitacoraEntry(bit_id, estudiante_id, actividad, float(horas), fecha, completada)
        self.bitacoras.append(nueva)
        PersistenceManager.save_bitacoras(self.bitacoras)

    def completar_actividad(self, bitacora_id):
        for b in self.bitacoras:
            if b.id == bitacora_id:
                b.completada = True
                PersistenceManager.save_bitacoras(self.bitacoras)
                return True
        return False

    def calcular_horas(self, estudiante_id) -> float:
        return sum(b.horas for b in self.bitacoras if b.estudiante_id == estudiante_id and b.completada)

    def obtener_solicitudes_beneficiario(self, beneficiario_id) -> List[Solicitud]:
        return [s for s in self.solicitudes if s.beneficiario_id == beneficiario_id]

    def obtener_nombre_usuario(self, user_id) -> str:
        for u in self.usuarios:
            if u.id == user_id:
                return u.nombre
        return "Desconocido"

    def obtener_contacto_usuario(self, user_id) -> str:
        for u in self.usuarios:
            if u.id == user_id:
                return u.correo
        return "No disponible"
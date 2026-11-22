import logging
from abc import abstractmethod
from modulo_base import (
    EntidadSistema,
    DatosInvalidosError,
    ServicioNoDisponibleError,
    OperacionReservaError,
)


# ==========================================
# MÓDULO 2: Clase Cliente (Encapsulación)
# ==========================================
class Cliente(EntidadSistema):
    def __init__(self, id_entidad: str, nombre: str, correo: str, telefono: str):
        super().__init__(id_entidad)
        self.__nombre = None
        self.__correo = None
        self.__telefono = None
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.validar_datos()

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            logging.error(f"Nombre inválido para cliente {self.id_entidad}: '{valor}'")
            raise DatosInvalidosError("El nombre del cliente debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str):
        if not isinstance(valor, str) or "@" not in valor or "." not in valor:
            logging.error(f"Correo inválido para cliente {self.id_entidad}: '{valor}'")
            raise DatosInvalidosError(f"Correo electrónico inválido: '{valor}'")
        self.__correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not isinstance(valor, str) or not valor.isdigit() or len(valor) < 7:
            logging.error(f"Teléfono inválido para cliente {self.id_entidad}: '{valor}'")
            raise DatosInvalidosError("El teléfono debe contener solo dígitos (mínimo 7).")
        self.__telefono = valor

    def validar_datos(self) -> bool:
        logging.info(f"Cliente {self.id_entidad} ({self.__nombre}) validado correctamente.")
        return True

    def mostrar_resumen(self) -> str:
        return f"Cliente [{self.id_entidad}] - {self.__nombre} | {self.__correo}"


# ==========================================
# MÓDULO 3: Clase Abstracta Servicio y ReservaSala
# ==========================================
class Servicio(EntidadSistema):
    def __init__(self, id_entidad: str, nombre_servicio: str, tarifa_base: float, disponible: bool = True):
        super().__init__(id_entidad)
        if tarifa_base <= 0:
            raise DatosInvalidosError("La tarifa base debe ser mayor a cero.")
        self.nombre_servicio = nombre_servicio
        self.tarifa_base = tarifa_base
        self.disponible = disponible

    @abstractmethod
    def calcular_costo(self, unidades: int, descuento: float = 0.0) -> float:
        pass

    def validar_datos(self) -> bool:
        return self.tarifa_base > 0 and bool(self.nombre_servicio.strip())


class ReservaSala(Servicio):
    def __init__(self, id_entidad: str, nombre_servicio: str, tarifa_base: float, capacidad: int, disponible: bool = True):
        super().__init__(id_entidad, nombre_servicio, tarifa_base, disponible)
        if capacidad <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser mayor a cero.")
        self.capacidad = capacidad

    def calcular_costo(self, horas: int, descuento: float = 0.0) -> float:
        """Polimorfismo + sobrecarga simulada mediante parámetro opcional descuento."""
        if horas <= 0:
            raise OperacionReservaError("Las horas de reserva de sala deben ser mayores a cero.")
        subtotal = self.tarifa_base * horas
        return subtotal * (1 - descuento)

    def mostrar_resumen(self) -> str:
        return f"Sala [{self.id_entidad}] {self.nombre_servicio} (Cap: {self.capacidad}) - ${self.tarifa_base:,.0f}/h"


# ==========================================
# MÓDULO 4: AlquilerEquipo y AsesoriaEspecializada
# ==========================================
class AlquilerEquipo(Servicio):
    def __init__(self, id_entidad: str, nombre_servicio: str, tarifa_base: float, deposito: float, disponible: bool = True):
        super().__init__(id_entidad, nombre_servicio, tarifa_base, disponible)
        self.deposito = deposito

    def calcular_costo(self, dias: int, descuento: float = 0.0) -> float:
        if dias <= 0:
            raise OperacionReservaError("Los días de alquiler deben ser mayores a cero.")
        return (self.tarifa_base * dias) * (1 - descuento) + self.deposito

    def mostrar_resumen(self) -> str:
        return f"Equipo [{self.id_entidad}] {self.nombre_servicio} - ${self.tarifa_base:,.0f}/día + Depósito ${self.deposito:,.0f}"


class AsesoriaEspecializada(Servicio):
    def __init__(self, id_entidad: str, nombre_servicio: str, tarifa_base: float, especialidad: str, disponible: bool = True):
        super().__init__(id_entidad, nombre_servicio, tarifa_base, disponible)
        self.especialidad = especialidad

    def calcular_costo(self, sesiones: int, descuento: float = 0.0) -> float:
        if sesiones <= 0:
            raise OperacionReservaError("El número de sesiones debe ser mayor a cero.")
        recargo_especialidad = 1.10
        return (self.tarifa_base * sesiones * recargo_especialidad) * (1 - descuento)

    def mostrar_resumen(self) -> str:
        return f"Asesoría [{self.id_entidad}] {self.nombre_servicio} ({self.especialidad}) - ${self.tarifa_base:,.0f}/sesión"


# ==========================================
# MÓDULO 5: Clase Reserva y 10 Simulaciones
# ==========================================
class Reserva(EntidadSistema):
    def __init__(self, id_entidad: str, cliente: Cliente, servicio: Servicio, unidades: int, descuento: float = 0.0):
        super().__init__(id_entidad)
        self.cliente = cliente
        self.servicio = servicio
        self.unidades = unidades
        self.descuento = descuento
        self.estado = "PENDIENTE"
        self.costo_total = 0.0

    def validar_datos(self) -> bool:
        if not self.servicio.disponible:
            logging.error(f"Servicio {self.servicio.id_entidad} no disponible para reserva {self.id_entidad}.")
            raise ServicioNoDisponibleError(f"El servicio '{self.servicio.nombre_servicio}' no está disponible.")
        if not (0.0 <= self.descuento <= 0.5):
            raise OperacionReservaError("El descuento debe estar entre 0% (0.0) y 50% (0.5).")
        return True

    def confirmar(self):
        try:
            self.validar_datos()
            self.costo_total = self.servicio.calcular_costo(self.unidades, self.descuento)
        except Exception as err:
            self.estado = "RECHAZADA"
            logging.error(f"Reserva {self.id_entidad} rechazada: {err}")
            raise
        else:
            self.estado = "CONFIRMADA"
            logging.info(f"Reserva {self.id_entidad} CONFIRMADA | Total: ${self.costo_total:,.2f}")
        finally:
            logging.info(f"Cierre de transacción para reserva {self.id_entidad} (Estado: {self.estado}).")

    def mostrar_resumen(self) -> str:
        return (
            f"Reserva [{self.id_entidad}] | {self.estado} | "
            f"{self.cliente.nombre} -> {self.servicio.nombre_servicio} | Total: ${self.costo_total:,.2f}"
        )


def ejecutar_simulaciones():
    print("=== INICIANDO 10 SIMULACIONES SOFTWARE FJ ===\n")
    c1 = Cliente("CLI-01", "Juan Pablo Jurado", "juan@unad.edu.co", "3001234567")
    c2 = Cliente("CLI-02", "Laura Gómez", "laura.gomez@empresa.com", "3109876543")

    sala_ok = ReservaSala("SAL-01", "Sala Conferencias A", 80000, 20, disponible=True)
    sala_off = ReservaSala("SAL-02", "Sala Mantenimiento", 60000, 10, disponible=False)
    equipo_ok = AlquilerEquipo("EQP-01", "Servidor Portátil Pro", 120000, 50000, disponible=True)
    asesoria_ok = AsesoriaEspecializada("ASE-01", "Arquitectura Cloud", 150000, "DevOps", disponible=True)

    casos = [
        # 5 CASOS VÁLIDOS
        ("Simulación 1 (Válida - Sala sin desc)", lambda: Reserva("RES-01", c1, sala_ok, 3)),
        ("Simulación 2 (Válida - Sala con 10% desc)", lambda: Reserva("RES-02", c2, sala_ok, 5, 0.10)),
        ("Simulación 3 (Válida - Alquiler Equipo)", lambda: Reserva("RES-03", c1, equipo_ok, 2)),
        ("Simulación 4 (Válida - Asesoría Cloud)", lambda: Reserva("RES-04", c2, asesoria_ok, 2, 0.15)),
        ("Simulación 5 (Válida - Equipo 1 día)", lambda: Reserva("RES-05", c2, equipo_ok, 1, 0.05)),
        # 5 CASOS INVÁLIDOS (Pruebas de excepciones)
        ("Simulación 6 (Inválida - Servicio no disponible)", lambda: Reserva("RES-06", c1, sala_off, 2)),
        ("Simulación 7 (Inválida - Unidades en cero)", lambda: Reserva("RES-07", c1, sala_ok, 0)),
        ("Simulación 8 (Inválida - Descuento > 50%)", lambda: Reserva("RES-08", c2, asesoria_ok, 1, 0.80)),
        ("Simulación 9 (Inválida - Correo sin @)", lambda: Cliente("CLI-99", "Carlos", "correo_invalido", "3001112222")),
        ("Simulación 10 (Inválida - ID vacío)", lambda: Reserva("   ", c1, equipo_ok, 1)),
    ]

    for nombre_caso, accion in casos:
        try:
            obj = accion()
            if isinstance(obj, Reserva):
                obj.confirmar()
            print(f"[OK] {nombre_caso}: {obj.mostrar_resumen()}")
        except Exception as e:
            print(f"[ERROR CONTROLADO] {nombre_caso} -> {type(e).__name__}: {e}")

    print("\n=== FIN DE SIMULACIONES. Revisa 'software_fj.log' ===")


if __name__ == "__main__":
    ejecutar_simulaciones()
import logging
from abc import ABC, abstractmethod
from datetime import datetime

# 1. Configuración estricta del sistema de Logs (Archivo físico)
logging.basicConfig(
    filename='software_fj.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

# 2. Jerarquía de Excepciones Personalizadas
class SoftwareFJError(Exception):
    """Excepción base para todas las fallas controladas del sistema Software FJ."""
    pass

class DatosInvalidosError(SoftwareFJError):
    """Se lanza cuando los parámetros de entrada o datos personales no cumplen el formato."""
    pass

class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta reservar un servicio sin disponibilidad o inactivo."""
    pass

class OperacionReservaError(SoftwareFJError):
    """Se lanza ante cálculos inconsistentes o transiciones de estado no permitidas en reservas."""
    pass

# 3. Clase Abstracta General para las Entidades del Sistema
class EntidadSistema(ABC):
    def __init__(self, id_entidad: str):
        self._id_entidad = None
        self.fecha_creacion = datetime.now()
        self._asignar_id_seguro(id_entidad)

    @property
    def id_entidad(self) -> str:
        return self._id_entidad

    def _asignar_id_seguro(self, id_entidad: str):
        """Bloque completo try / except / else / finally con encadenamiento."""
        try:
            if not isinstance(id_entidad, str) or not id_entidad.strip():
                raise ValueError("El identificador debe ser una cadena de texto no vacía.")
            id_limpio = id_entidad.strip().upper()
        except ValueError as err_original:
            logging.error(f"Fallo al validar ID '{id_entidad}': {err_original}")
            # Encadenamiento de excepciones exigido por la rúbrica
            raise DatosInvalidosError(f"ID de entidad inválido: '{id_entidad}'") from err_original
        else:
            self._id_entidad = id_limpio
            logging.info(f"Entidad inicializada correctamente con ID: {self._id_entidad}")
        finally:
            logging.info("Finalizó el proceso de verificación de identificador de entidad.")

    @abstractmethod
    def validar_datos(self) -> bool:
        """Método abstracto que obliga a las subclases a validar su integridad."""
        pass

    @abstractmethod
    def mostrar_resumen(self) -> str:
        """Método abstracto para describir la entidad."""
        pass

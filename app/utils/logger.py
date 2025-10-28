import logging
import os
from datetime import datetime


def get_logger(name: str = "app") -> logging.Logger:
    """
    Devuelve un logger configurado para toda la aplicación.
    Crea automáticamente un archivo de log por día en la carpeta /logs.

    Args:
        name (str): Nombre del módulo o componente que usa el logger.

    Returns:
        logging.Logger: Instancia lista para usar.
    """

    # Crear carpeta de logs si no existe
    os.makedirs("logs", exist_ok=True)

    # Nombre del archivo de log basado en la fecha actual
    log_filename = f"logs/app_{datetime.now().strftime('%Y-%m-%d')}.log"

    # Configuración del formato de salida
    log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Configurar logging básico (solo una vez)
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(log_filename, encoding="utf-8"),
            logging.StreamHandler()  # También muestra los logs en consola
        ]
    )

    # Crear logger con nombre del módulo
    logger = logging.getLogger(name)
    logger.propagate = False  # Evita duplicados si se llama varias veces

    return logger

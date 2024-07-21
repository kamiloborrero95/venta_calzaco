#imports
import numpy as np
import sqlalchemy
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from numpy_mask import paises, precios, mask

#consumir db
engine = create_engine("sqlite:///ventas_calzados.db")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Definir la clase Ventas
class Ventas(Base):
    __tablename__ = "ventas"  # Se debe especificar el nombre de la tabla
    id = Column(Integer, autoincrement=True, primary_key=True)
    producto_id = Column(Integer)
    pais = Column(String)
    genero = Column(String)
    talle = Column(String)
    precio = Column(String)

#functions
def read_db():
    paises_query = session.query(Ventas.pais).all()
    genero_query = session.query(Ventas.genero).all()
    talles_query = session.query(Ventas.talle).all()
    precios_query = session.query(Ventas.precio).all()
    
    paises = np.array([resultado[0] for resultado in paises_query])
    generos = np.array([resultado[0] for resultado in genero_query])
    talles = np.array([resultado[0] for resultado in talles_query])
    precios = np.array([float(resultado[0].replace('$', '')) for resultado in precios_query])

    return paises, generos, talles, precios
    
def obtener_paises_unicos(paises):
    paises_unicos = np.unique(paises)
    
    return paises_unicos

def obtener_ventas_por_pais(paises_objetivo, paises, precios):
    precios_objetivo = {}
# Iterar sobre los países objetivo
    for pais_objetivo in paises_objetivo:
        # Verificar si el país objetivo está en la lista de países
        if pais_objetivo in paises:
            # Obtener el índice del país en la lista de países
            indices = np.where(paises == pais_objetivo)[0]
            # Sumar los precios correspondientes al país
            precio_total = np.sum(precios[indices])
            # Agregar el país y su precio total correspondiente al diccionario
            precios_objetivo[pais_objetivo] = precio_total
            
    return precios_objetivo

def obtener_calzado_mas_vendido_por_pais(paises_objetivo, paises, talles):
    dict_calzado = {}
    for pais_objetivo in paises_objetivo:
        if pais_objetivo in paises:
            indices = np.where(paises==pais_objetivo)[0]
            talles_pais = talles[indices]
            valores, conteos = np.unique(talles_pais,return_counts=True)
            talle_mas_vendido = valores[np.argmax(conteos)]
            
            dict_calzado[pais_objetivo] = talle_mas_vendido
    
    return dict_calzado

def obtener_ventas_por_genero_pais(paises_objetivo, genero_objetivo, paises, generos):
    # Crear un diccionario para almacenar los resultados
    resultado = {}
    
    # Iterar sobre los países objetivo
    for pais in paises_objetivo:
        # Crear una máscara para filtrar las ventas de este país
        mask_pais = paises == pais
        
        # Crear una máscara para filtrar las ventas de este país y del género objetivo
        mask_genero = (paises == pais) & (generos == genero_objetivo)
        
        # Contar la cantidad de calzados vendidos de este género en este país
        cantidad_calzados = np.sum(mask_genero)
        
        # Almacenar la cantidad en el diccionario resultado
        resultado[pais] = cantidad_calzados
    
    return resultado


#main
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    ejecucion = Ventas()
    paises, generos, talles, precios = read_db()
    lista_paises_unicos = obtener_paises_unicos(paises)
    
    paises_objetivo = ["Canada", "Germany"]
    ventas_pais = obtener_ventas_por_pais(paises_objetivo, paises, precios)
    calzado_mas_vendido = obtener_calzado_mas_vendido_por_pais(paises_objetivo, paises, talles)
    genero_objetivo = "Female"
    resultados = obtener_ventas_por_genero_pais(paises_objetivo, genero_objetivo, paises, generos)
    

    

import numpy as np

paises = np.array(["Canada", "Canada", "Canada", "Germany", "Argentina"])
precios = np.array([250, 250, 100, 120, 50])

# Crear una máscara para obtener los índices del array
# que corresponden al país Canada
mask = paises == "Canada"

# Utilizo la máscara para acceder a los indices del array price
# que corresponden a canada
ventas_canada = precios[mask]
print(ventas_canada)
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Generar datos
n = 100
x = np.random.rand(n)
y = np.random.rand(n)
z = np.random.rand(n)
w = np.random.rand(n)  # Cuarta dimensión

# Crear una figura
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Asignar colores en base a la cuarta dimensión
scatter = ax.scatter(x, y, z, c=w, cmap='viridis', s=100)

# Añadir una barra de color
cbar = plt.colorbar(scatter)
cbar.set_label('Cuarta Dimensión (Color)')

# Etiquetas de los ejes
ax.set_xlabel('Eje X')
ax.set_ylabel('Eje Y')
ax.set_zlabel('Eje Z')

# Título
ax.set_title('Visualización de un espacio 4D en 3D')

# Mostrar la figura
plt.show()

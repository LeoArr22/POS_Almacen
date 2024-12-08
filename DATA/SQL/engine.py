from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy.exc import NoResultFound

#Crear la conexión con la base de datos
engine = create_engine('mysql+mysqlconnector://root:root@localhost/db_almacen')

#Declaración de la base y fabrica de sesiones
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Producto(Base):
    __tablename__ = 'Producto'
    productoID = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    precio = Column(Integer)
    stock = Column(Integer)
    costo = Column(Integer)
    codigo_barra = Column(String)
    categoriaID = Column(Integer, ForeignKey('Categoria.categoriaID'))
    
    # Relaciones
    detalle = relationship("Detalle", back_populates="producto")
    categoria = relationship("Categoria", back_populates="productos")  

class Categoria(Base):
    __tablename__ = "Categoria"
    categoriaID = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    descripcion = Column(String)
    
    # Relación con Producto
    productos = relationship("Producto", back_populates="categoria")  

class Detalle(Base):
    __tablename__ = 'Detalle'
    productoID = Column(Integer, ForeignKey('Producto.productoID'), primary_key=True)
    ventaID = Column(Integer, ForeignKey('Venta.ventaID'), primary_key=True)
    cantidad = Column(Integer)
    total_prod = Column(Float)
    
    # Relaciones
    producto = relationship("Producto", back_populates="detalle")
    venta = relationship("Venta", back_populates="detalle") 

class Venta(Base):
    __tablename__ = 'Venta'
    ventaID = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date)
    total_venta = Column(Float)
    vendedorID = Column(Integer, ForeignKey('Vendedor.vendedorID'))
    
    # Relación con Detalle
    detalle = relationship("Detalle", back_populates="venta")  

class Vendedor(Base):
    __tablename__ = "Vendedor"
    vendedorID = Column(Integer, primary_key=True, autoincrement=True)
    usuario = Column(String)
    contrasena = Column(Integer)
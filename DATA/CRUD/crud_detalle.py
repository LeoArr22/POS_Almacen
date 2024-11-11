from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, ForeignKey
from engine import get_session
import validadores

Base = declarative_base()

class Detalle(Base):
    __tablename__ = 'detalle'
    Producto_productoID = Column(Integer, ForeignKey('producto.productoID'), primary_key=True)
    Venta_ventaID = Column(Integer, ForeignKey('venta.ventaID'), primary_key=True)
    cantidad = Column(Integer, nullable=False)
    total_prod = Column(Float, nullable=False)

def crear_detalle(producto_id, venta_id, cantidad, total_prod):
    if validadores.validar_ids(producto_id, venta_id) and validadores.validar_cantidad(cantidad) and validadores.validar_total_prod(total_prod):
        session = get_session()
        nuevo_detalle = Detalle(
            Producto_productoID=producto_id,
            Venta_ventaID=venta_id,
            cantidad=cantidad,
            total_prod=total_prod
        )
        session.add(nuevo_detalle)
        session.commit()
        session.close()
        print("Detalle creado exitosamente.")

def leer_detalles():
    session = get_session()
    detalles = session.query(Detalle).all()
    for detalle in detalles:
        print(f"Producto ID: {detalle.Producto_productoID}, Venta ID: {detalle.Venta_ventaID}, "
              f"Cantidad: {detalle.cantidad}, Total Producto: {detalle.total_prod}")
    session.close()
def actualizar_detalle(producto_id, venta_id, nueva_cantidad, nuevo_total_prod):
    if validadores.validar_ids(producto_id, venta_id) and validadores.validar_cantidad(nueva_cantidad) and validadores.validar_total_prod(nuevo_total_prod):
        session = get_session()
        detalle = session.query(Detalle).filter_by(
            Producto_productoID=producto_id,
            Venta_ventaID=venta_id
        ).first()
        if detalle:
            detalle.cantidad = nueva_cantidad
            detalle.total_prod = nuevo_total_prod
            session.commit()
            print("Detalle actualizado exitosamente.")
        else:
            print("Detalle no encontrado.")
        session.close()

def eliminar_detalle(producto_id, venta_id):
    if validadores.validar_ids(producto_id, venta_id):
        session = get_session()
        detalle = session.query(Detalle).filter_by(
            Producto_productoID=producto_id,
            Venta_ventaID=venta_id
        ).first()
        if detalle:
            session.delete(detalle)
            session.commit()
            print("Detalle eliminado exitosamente.")
        else:
            print("Detalle no encontrado.")
        session.close()

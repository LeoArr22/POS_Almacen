from data.sql.engine import *
from sqlalchemy import func

class CRUD_detalle():
    def __init__(self, Session):
        self.Session = Session

    def crear_detalle(self, producto_id, venta_id, cantidad, total_prod):
        with self.Session() as session:
            detalle_existente, _ = self.obtener_detalle(producto_id, venta_id, session)

            if detalle_existente is None:
                nuevo_detalle = Detalle(
                    productoID=producto_id,
                    ventaID=venta_id,
                    cantidad=cantidad,
                    total_prod=total_prod
                )
                session.add(nuevo_detalle)
                session.commit()
                return nuevo_detalle, None
            return None, "El detalle ya existe para este producto en la venta"

    def obtener_detalle(self, producto_id, venta_id, session=None):
        close_session = False
        if session is None:
            session = self.Session()
            close_session = True
        try:
            detalle = session.query(Detalle).filter_by(
                productoID=producto_id,
                ventaID=venta_id
            ).one()
            return detalle, ""
        except NoResultFound:
            return None, "No se encontró el detalle para este producto en la venta"
        finally:
            if close_session:
                session.close()

    def obtener_detalles_por_venta(self, venta_id):
        with self.Session() as session:
            try:
                detalles = session.query(
                    Detalle.productoID,
                    Detalle.ventaID,
                    Detalle.cantidad,
                    Detalle.total_prod,
                    Producto.nombre.label('producto_nombre')
                ).join(Producto, Detalle.productoID == Producto.productoID).filter(Detalle.ventaID == venta_id).all()
                return detalles
            except Exception:
                return None

    def actualizar_detalle(self, producto_id, venta_id, nueva_cantidad):
        with self.Session() as session:
            detalle, error = self.obtener_detalle(producto_id, venta_id, session)
            producto = session.query(Producto).filter_by(productoID=producto_id).first()

            if detalle is not None and producto is not None:
                detalle.cantidad = nueva_cantidad
                detalle.total_prod = nueva_cantidad * producto.precio  # Recalcular total_prod
                session.commit()
                return detalle, None
            return None, "No se pudo actualizar el detalle"

    def eliminar_detalle(self, producto_id, venta_id):
        with self.Session() as session:
            detalle, error = self.obtener_detalle(producto_id, venta_id, session)
            if detalle is not None:
                session.delete(detalle)
                session.commit()
                return True, None
            return False, error

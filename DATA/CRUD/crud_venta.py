from data.sql.engine import *
from sqlalchemy import func

class CRUD_venta():
    def __init__(self, Session):
        self.Session = Session

    def crear_venta(self, total_venta, ganancia_total, vendedor_id, vendedor_nombre):
        with self.Session() as session:
            nueva_venta = Venta(
                fecha=func.current_date(),  # Fecha actual
                total_venta=total_venta,
                ganancia_total=ganancia_total,
                vendedorID=vendedor_id,
                vendedor_nombre = vendedor_nombre
                
            )
            session.add(nueva_venta)
            session.commit()
            session.refresh(nueva_venta) 
            return nueva_venta, None

    def obtener_venta(self, venta_id):
        with self.Session() as session:
            try:
                venta = session.query(Venta).filter_by(ventaID=venta_id).one()
                return venta, None
            except NoResultFound:
                return None, "No se encontró la venta"

    def obtener_ventas_por_fecha(self, fecha):
        with self.Session() as session:
            ventas = session.query(Venta).filter_by(fecha=fecha).all()
            return ventas

    def obtener_todas_las_ventas(self):
        with self.Session() as session:
            ventas = session.query(Venta).all()
            return ventas

    def actualizar_venta(self, venta_id, nuevo_total, nueva_ganancia):
        with self.Session() as session:
            venta, error = self.obtener_venta(venta_id)
            if venta is not None:
                venta.total_venta = nuevo_total
                venta.ganancia_total = nueva_ganancia
                session.commit()
                return venta, None
            return None, error

    def eliminar_venta(self, venta_id):
        with self.Session() as session:
            venta, error = self.obtener_venta(venta_id)
            if venta is not None:
                session.delete(venta)
                session.commit()
                return True, None
            return False, error

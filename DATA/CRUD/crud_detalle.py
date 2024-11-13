from DATA.SQL.engine import Detalle 
from UTIL.validadores import validar_cantidad, validar_total_prod, validar_ids

class CRUD_detalle():
    def __init__(self, Session):
        self.session = Session

    def crear_detalle(self, producto_id, venta_id, cantidad, total_prod):
        if validar_ids(producto_id, venta_id) and validar_cantidad(cantidad) and validar_total_prod(total_prod):
            if self.obtener_detalle(producto_id, venta_id) is None:
                nuevo_detalle = Detalle( 
                    productoID=producto_id,
                    ventaID=venta_id,
                    cantidad=cantidad,
                    total_prod=total_prod
                )
                self.session.add(nuevo_detalle)
                self.session.commit()
                return nuevo_detalle
            else:
                print("El detalle ya existe para este producto y venta.")
        else:
            print("Error en los datos ingresados para el detalle.")
        return None

    def obtener_detalle(self, producto_id, venta_id):
        try:
            detalle = self.session.query(Detalle).filter_by( 
                productoID=producto_id,
                ventaID=venta_id
            ).one()
            return detalle
        except NoResultFound:
            return None

    def actualizar_detalle(self, producto_id, venta_id, nueva_cantidad, nuevo_total_prod):
        if validar_ids(producto_id, venta_id) and validar_cantidad(nueva_cantidad) and validar_total_prod(nuevo_total_prod):
            detalle = self.obtener_detalle(producto_id, venta_id)
            if detalle:
                detalle.cantidad = nueva_cantidad
                detalle.total_prod = nuevo_total_prod
                self.session.commit()
                return detalle
            else:
                print("El detalle no existe.")
        else:
            print("Error en los datos ingresados para actualizar.")
        return None

    def eliminar_detalle(self, producto_id, venta_id):
        if validar_ids(producto_id, venta_id):
            detalle = self.obtener_detalle(producto_id, venta_id)
            if detalle:
                self.session.delete(detalle)
                self.session.commit()
                return True
            else:
                print("El detalle no existe.")
        else:
            print("Error en los IDs ingresados para el detalle.")
        return False
#putoelqueleadesputosisoseldirectordelacarrera
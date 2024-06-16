from django.db import models


class Province(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)

    def __str__(self):
        return self.name


class Municipality(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE, blank=False, null=False
    )

    def __str__(self):
        return self.name

class Client(models.Model):
    nombre_cliente = models.CharField(max_length=100, blank=False, null=False)
    dni = models.CharField(max_length=15, blank=True, null=True)
    telef = models.CharField(max_length=15, blank=True, null=True)
    telef_nombre = models.CharField(max_length=100, blank=True, null=True)
    telef_2 = models.CharField(max_length=15, blank=True, null=True)
    telef_2_nombre = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    provincia = models.ForeignKey(
        Province, on_delete=models.CASCADE, blank=True, null=True
    )
    localidad = models.ForeignKey(
        Municipality, on_delete=models.CASCADE, blank=True, null=True
    )
    direccion = models.CharField(max_length=100, blank=True, null=True)
    cp = models.IntegerField(blank=True, null=True)
    empresa = models.BooleanField(default=False)
    e_nombre = models.CharField(max_length=100, blank=True, null=True)
    e_dni = models.CharField(max_length=15, blank=True, null=True)
    cap_nombre = models.CharField(max_length=100, blank=True, null=True)
    cap_dni = models.CharField(max_length=15, blank=True, null=True)
    cap_provincia = models.ForeignKey(Province, on_delete=models.CASCADE, blank=True, null=True, related_name="cap_provincia")
    cap_localidad = models.ForeignKey(Municipality, on_delete=models.CASCADE, blank=True, null=True, related_name="cap_localidad")
    cap_direccion = models.CharField(max_length=100, blank=True, null=True)
    cap_cp = models.IntegerField(blank=True, null=True)
    compras_cuenta = models.CharField(max_length=100, blank=True, null=True)
    matricula_cliente = models.CharField(max_length=100, blank=True, null=True)
    nombre_cliente_calcu = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre_cliente


class Sales(models.Model):
    car = models.OneToOneField('catalog.Car', on_delete=models.CASCADE)
    # client = models.ForeignKey(Client, on_delete=models.CASCADE)
    # vendedor = models.ForeignKey(Saler, max_length=100, blank=True, null=True, on_delete=models.CASCADE)
    vendedor = models.CharField(max_length=100, blank=True, null=True)
    f_venta = models.DateField(blank=True, null=True)
    t_iva = models.CharField(max_length=50, blank=True, null=True)
    garantia = models.CharField(max_length=50, blank=True, null=True)   
    garantia_fab_km = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    garantia_fab_fecha = models.DateField(blank=True, null=True)
    garantia_ext_num = models.CharField(max_length=50, blank=True, null=True)
    doble_precio = models.BooleanField(default=False, blank=True, null=True)
    p_contado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    p_financiado = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    p_venta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    p_venta_modif = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    p_nuevo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    info_ventas = models.TextField(blank=True, null=True)
    info_admin = models.TextField(blank=True, null=True)
    info_taller = models.TextField(blank=True, null=True)
    info_publi = models.TextField(blank=True, null=True)
    info_transporte = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha_entrega = models.DateField(blank=True, null=True)
    hora_entrega = models.TimeField(blank=True, null=True)
    cobrado = models.TextField(blank=True, null=True)
    equip_1 = models.TextField(blank=True, null=True)
    equip_2 = models.TextField(blank=True, null=True)
    equip_3 = models.TextField(blank=True, null=True)
    equip_4 = models.TextField(blank=True, null=True)
    equip_5 = models.TextField(blank=True, null=True)
    equip_6 = models.TextField(blank=True, null=True)
    equip_7 = models.TextField(blank=True, null=True)
    equip_8 = models.TextField(blank=True, null=True)
    equip_9 = models.TextField(blank=True, null=True)
    equip_10 = models.TextField(blank=True, null=True)
    equip_11 = models.TextField(blank=True, null=True)
    equip_12 = models.TextField(blank=True, null=True)
    equip_13 = models.TextField(blank=True, null=True)
    equip_14 = models.TextField(blank=True, null=True)
    equip_15 = models.TextField(blank=True, null=True)
    equip_16 = models.TextField(blank=True, null=True)
    equip_17 = models.TextField(blank=True, null=True)
    equip_18 = models.TextField(blank=True, null=True)
    
    
    def __str__(self):
        return f"{self.car} - {self.vendedor}"
    

import ssl
import routeros_api

class apimikrotik:
    def __init__(self, ip, username, password, port, data):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port
        self.data = data
        self.api = None
        self.connect()

    def connect(self):
        try:
            api_pool = routeros_api.RouterOsApiPool(
                host=self.ip,
                username=self.username,
                password=self.password,
                plaintext_login=True,
                port=self.port,
                use_ssl=False,
                ssl_verify=True,
                ssl_verify_hostname=False,
                ssl_context=None,
            )
            self.api = api_pool.get_api()
            print("Conexión exitosa")
        except Exception as e:
            self.data['error'] = f"No hay conexión a la API de Mikrotik: {str(e)}"
            self.api = None

    def reiniciar_mikro(self):
        if self.api is None:
            self.data['error'] = 'No hay conexión a la API de Mikrotik.'
            print("no hay conexion a la mikrptik")
            return

        try:
            self.api.get_resource('/system').call('reboot')
            print("mikrotik reiniciada")
        except Exception as e:
            self.data['error'] = str(e)

    def close(self):
        if self.api is not None:
            self.api.close()
            self.api = None

    def create_queue(self, queue_params):

        if self.api is None:
            self.data['error'] = 'No hay conexión a la API de Mikrotik.'
            print("no hay conexion")
            return
        
        try:
            # Definir los parámetros para crear la cola
            # Obtener el recurso de colas
            queues_resource = self.api.get_resource('/queue/simple')

            # Crear la cola usando el método add()
            queues_resource.add(**queue_params)

            print("Cola creada exitosamente")
        except Exception as e:       
                data['error'] = str(e)
            
        return data

    def editar_queue(self, queue_name, new_name, target_ip, max_limit, burst_limit, limit_at, burst_threshold, burst_time,priority, data):

        if self.api is None:
            self.data['error'] = 'No hay conexión a la API de Mikrotik.'
            return

        try:
            queues_resource = self.api.get_resource('/queue/simple')
            # Obtener todas las colas
            queues = queues_resource.get()
            # Buscar la cola por nombre
            queue_to_edit = None
            for queue in queues:
                if queue['name'] == queue_name:
                    queue_to_edit = queue
                    print(queue_to_edit)
                    break
            
            queue_params = {
                'name': new_name,
                'target': target_ip,
                'max-limit': max_limit,
                'burst-limit': burst_limit,
                'limit-at': limit_at,
                'burst-threshold': burst_threshold,
                'burst-time': burst_time,
                'priority': priority
            }

            if queue_to_edit:
                queues_resource.set(id=queue_to_edit['id'], **queue_params)
                print("cola Actualizada")
                return True
            else:
                print('no se encontro la queue')
                data['error'] = 'No se encontro esta queue'

            self.api.close()

        except Exception as e:       
                data['error'] = str(e)

        return data

    def eliminar_queue(self, queue_name):
        try:
            if self.api in None:
                self.data['error'] = "Mikrotik desconectada"

            # Obtener el recurso de colas
            queues_resource = self.api.get_resource('/queue/simple')

            # Obtener todas las colas
            queues = queues_resource.get()
            #print(queues)

            # Buscar la cola por nombre
            queue_to_delete = None
            for queue in queues:
                if queue['name'] == queue_name:
                    queue_to_delete = queue
                    # print(queue_to_delete)
                    break

            if queue_to_delete:
                # Eliminar la cola utilizando el método remove()
                queues_resource.remove(id=queue_to_delete['id'])
                print("cola eliminada")
                return True
            else:
                self.data['error'] = 'No se encontro el queue'

        except Exception as e:       
                self.data['error'] = str(e)

        return self.data

    def create_secret_pppoe(self, nombre_servicio, password, nombre_perfil):
        if self.api is None:
            self.data['error'] = 'No hay conexión a la API de Mikrotik.'
            return
        
        try:
            create_ppp = self.api.get_resource('/ppp/secrets')
            secret_nuevo = {
                'name': nombre_servicio,
                'password': password,
                'service': 'pppoe',
                'profile': nombre_perfil
            }
            create_ppp.add(secret_nuevo)
        except Exception as e:
            self.data['error'] = str(e)
            return self.data
        
def connection(host, username, password, port):
    api_pool = routeros_api.RouterOsApiPool(
        host=host,
        username=username,
        password=password,
        plaintext_login=True,
        port=port,
        use_ssl=False,
        ssl_verify=True,
        ssl_verify_hostname=False,
        ssl_context=None,
    )
    return api_pool.get_api()

def crear_regla_corte(host, username, password, port, data):
    try:
        api = connection(host, username, password, port)
        print("Conexión exitosa")
        # Definir el nombre de la regla
        rule_name = 'Mora'
        
        # Obtener el recurso de reglas de firewall
        nat_resource = api.get_resource('/ip/firewall/nat')
        
        nat_params_tcp = {
                'chain': 'dstnat',  # La cadena de reenvío
                'src-address-list': rule_name,  # IP del cliente
                'action': 'redirect',  # Acción para bloquear el tráfico
                'comment': 'Manager - Suspension de ips (TCP)',  # Nombre de la regla
                'to-ports': '999',
                'protocol': 'tcp',
                'dst-port': '!8291'
            }
        nat_params_udp = {
                'chain': 'dstnat',  # La cadena de reenvío
                'src-address-list': rule_name,  # IP del cliente
                'action': 'redirect',  # Acción para bloquear el tráfico
                'comment': 'Manager - Suspension de ips (UDP)',  # Nombre de la regla
                'to-ports': '999',
                'protocol': 'udp',
                'dst-port': '!8291,53'
            }
        # Verificar si ya existe una regla con el mismo nombre y acción
        nats = nat_resource.get()
        existing_nat_tcp = None
        existing_nat_udp = None
        
        for nat in nats:
            if nat.get('src-address-list') == rule_name and nat.get('protocol') == 'tcp':
                existing_nat_tcp = nat
                print("regla tcp existente")
                break 
        
        if existing_nat_tcp:
            # Eliminar la regla NAT existente
            nat_resource.remove(id=existing_nat_tcp['id'])
            print(f"Regla NAT eliminada")
            nat_resource.add(**nat_params_tcp)
            print("regla nat tcp creada")
        else:
            nat_resource.add(**nat_params_tcp)
            print("regla nat creada tcp")

        for nat in nats:
            if nat.get('src-address-list') == rule_name and nat.get('protocol') == 'udp':
                existing_nat_udp = nat
                print("regla udp existente")
                break

        if existing_nat_udp:
            # Eliminar la regla NAT existente
            nat_resource.remove(id=existing_nat_udp['id'])
            print(f"Regla NAT eliminada")
            nat_resource.add(**nat_params_udp)
            print("regla nat udp creada")
        else:
            nat_resource.add(**nat_params_udp)
            print("regla nat creada udp")

        #CREAR REGLA FILTER
        filter_resource = api.get_resource('/ip/firewall/filter')
        filter_params = {
                'chain': 'forward',  # La cadena de reenvío
                'src-address-list': rule_name,  # Nombre de la lista
                'action': 'drop',  # Acción para bloquear el tráfico
                'comment': 'filtro de corte de servicio en mora',  # Nombre de la regla
            }
        # Verificar si ya existe una regla con el mismo nombre y acción
        filters = filter_resource.get()
        existing_filter = None
        
        for filter in filters:
            if nat.get('src-address-list') == rule_name:
                existing_filter = filter
                print("regla tcp existente")
                break 
        
        if existing_filter:
            # Eliminar la regla NAT existente
            filter_resource.remove(id=existing_filter['id'])
            print(f"Filtro NAT eliminado")
            filter_resource.add(**filter_params)
            print("filtro nap creado")
        else:
            filter_resource.add(**filter_params)
            print("filtro nap creado")
    except Exception as e:
            data['error'] = str(e)

def crear_regla_acceso(host, username, password, port, data):
    try:
        api = connection(host, username, password, port)
        print("Conexión exitosa")
        # Definir el nombre de la regla
        rule_name = 'Ips_autorizadas'
        
        # Obtener el recurso de reglas de firewall
        filter_resource = api.get_resource('/ip/firewall/filter')
        
        filter_params = {
                'chain': 'forward',  # La cadena de reenvío
                'src-address-list': rule_name,  # Nombre de la lista
                'action': 'accept',  # Acción para permitir el tráfico
                'comment': 'Ips con acceso a internet',  # Nombre de la regla
            }
        # Verificar si ya existe una regla con el mismo nombre y acción
        filters = filter_resource.get()
        existing_filter = None
        
        for filter in filters:
            if filter.get('src-address-list') == rule_name:
                existing_filter = filter
                print("regla existente")
                break 
        
        if existing_filter:
            # Eliminar la regla existente
            filter_resource.remove(id=existing_filter['id'])
            print(f"Filtro eliminado")
            filter_resource.add(**filter_params)
            print("filtro creado")
        else:
            filter_resource.add(**filter_params)
            print("filtro creado")

        filter_params2 = {
                'chain': 'forward',  # La cadena de reenvío
                'src-address-list': '!'+rule_name,  # Nombre de la lista
                'action': 'drop',  # Acción para permitir el tráfico
                'comment': 'Ips sin acceso a internet',  # Nombre de la regla
            }
        # Verificar si ya existe una regla con el mismo nombre y acción
        filters2 = filter_resource.get()
        existing_filter2 = None
        
        for filter2 in filters2:
            if filter2.get('src-address-list') == '!'+rule_name:
                existing_filter2 = filter2
                print("regla existente")
                break 
        
        if existing_filter2:
            # Eliminar la regla existente
            filter_resource.remove(id=existing_filter2['id'])
            print(f"Filtro eliminado")
            filter_resource.add(**filter_params2)
            print("filtro creado")
        else:
            filter_resource.add(**filter_params2)
            print("filtro creado")

    except Exception as e:
            data['error'] = str(e)

def aplicar_reglas(host, username, password, port, data):
    crear_regla_corte(host, username, password, port, data)
    crear_regla_acceso(host, username, password, port, data)

def create_queue(host, username, password, 
                 port, queue_name, target_ip, 
                 max_limit, burst_limit, limit_at,
                burst_threshold, burst_time, priority, data
                 ):
    try:
        api = connection(host, username, password, port)
        print("Conexión exitosa")
        #print("Conexión exitosa")

        # Definir los parámetros para crear la cola
        queue_params = {
            'name': queue_name,
            'target': target_ip,
            'max-limit': max_limit,
            'burst-limit': burst_limit,
            'limit-at': limit_at,
            'burst-threshold': burst_threshold,
            'burst-time': burst_time,
            'priority': priority
        }
        # Obtener el recurso de colas
        queues_resource = api.get_resource('/queue/simple')

        # Crear la cola usando el método add()
        queues_resource.add(**queue_params)

        print("Cola creada exitosamente")
    except Exception as e:       
            data['error'] = str(e)
        
    return data

def editar_queue(host, username, password, port, queue_name, new_name, target_ip, max_limit, burst_limit, limit_at, burst_threshold, burst_time,priority, data):
    try:
        api = connection(host, username, password, port)
        print("Conexión exitosa")

        # Obtener el recurso de colas
        queues_resource = api.get_resource('/queue/simple')

        # Obtener todas las colas
        queues = queues_resource.get()
        # print(queues)

        # Buscar la cola por nombre
        queue_to_edit = None
        for queue in queues:
            if queue['name'] == queue_name:
                queue_to_edit = queue
                print(queue_to_edit)
                break
        
        queue_params = {
            'name': new_name,
            'target': target_ip,
            'max-limit': max_limit,
            'burst-limit': burst_limit,
            'limit-at': limit_at,
            'burst-threshold': burst_threshold,
            'burst-time': burst_time,
            'priority': priority
        }

        if queue_to_edit:
            queues_resource.set(id=queue_to_edit['id'], **queue_params)
            print("cola Actualizada")
            return True
        else:
            print('no se encontro la queue')
            data['error'] = 'No se encontro esta queue'

        api.close()

    except Exception as e:       
            data['error'] = str(e)

    return data

def eliminar_queue(host, username, password, port, queue_name, data):
    try:
        api = connection(host, username, password, port)
        print("Conexión exitosa")

        # Obtener el recurso de colas
        queues_resource = api.get_resource('/queue/simple')

        # Obtener todas las colas
        queues = queues_resource.get()
        #print(queues)

        # Buscar la cola por nombre
        queue_to_delete = None
        for queue in queues:
            if queue['name'] == queue_name:
                queue_to_delete = queue
                # print(queue_to_delete)
                break

        if queue_to_delete:
            # Eliminar la cola utilizando el método remove()
            queues_resource.remove(id=queue_to_delete['id'])
            print("cola eliminada")
            return True
        else:
            data['error'] = 'No se encontro el queue'

    except Exception as e:       
            data['error'] = str(e)

    return data

def deshabilitar_servicio(host, username, password, port, target_ip, queue_name, data):
    try:
        api = connection(host, username, password, port)
        print("Conexión exitosa")
        # Definir el nombre de la lista de direcciones
        address_list = 'Mora'
        # Definir los parámetros para crear la cola
        rule_params = {
            'list': address_list,  # La cadena de reenvío
            'address': target_ip, # ip del cliente
            'comment': queue_name,  # Nombre de la queue
        }

        # Obtener el recurso de colas
        queues_resource = api.get_resource('/ip/firewall/address-list')
        # Crear la cola usando el método add()
        queues_resource.add(**rule_params)

        print("Servicio deshabiitado")
    except Exception as e:
        data['error'] = str(e)

def habilitar_servicio(host, username, password, port, target_ip):
    try:
        api = connection(host, username, password, port)
        print("Conexión exitosa")
        #buscar la regla para esa ip
        queues_resource = api.get_resource('/ip/firewall/filter')
        existing_rule = None
        for rule in queues_resource.get():
            if rule.get('name') == 'Suspendido_por_pago' and rule.get('action') == 'drop':
                existing_rule = rule
                break

        if existing_rule:
            existing_rule['action'] = 'accept'
            queues_resource.set(id=existing_rule['id'], **existing_rule)

        else:
            rule_params = {
                'chain': 'forward',  # La cadena de reenvío
                'src-address': target_ip,  # Reemplaza con la dirección IP del cliente
                'action': 'accept',  # Acción para Autorizar  el tráfico
                'name': 'ips_autorizadas'
            }

            # Crear la cola usando el método add()
            queues_resource.add(**rule_params)
            print("regla creada con exito")

            print("Servicio habiitado")
    except Exception as e:
        print("No se pudo establecer la conexión:", str(e))

def reiniciar_mikro(host, username, password, port, data):
    try:
        api = connection(host, username, password, port)
        print("Conexión exitosa")

        api.get_resource('/system').call('reboot')
        api.close()

    except Exception as e:
        data['error'] = str(e)


data = {}
ip='192.168.100.25'
username='admin'
password='admin'
port=8728
queue_name="Prueba de creacion" 
target_ip="192.168.1.100"
max_limit = '10M/10M'
burst_limit = 'unlimited'
limit_at = 'unlimited'
burst_threshold = 'unlimited'
burst_time = '20s'
priority = '8'

queue_params = {
    'name': "Prueba de creacion",
    'target': "192.168.1.200",
    'max-limit': '10M/10M',
    'limit-at': '5M/5M',
    'priority': '8'
}
test_api = apimikrotik(ip, username, password, port, data)
test_api.create_queue(queue_params)

# Verificar si hubo errores
if 'error' in data:
    print(f"Error: {data['error']}")
else:
    print("Queue creada exitosamente")
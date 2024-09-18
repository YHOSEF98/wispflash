import ssl
import routeros_api

class apimikrotik:
    def __init__(self, host, username, password, port, data):
        self.ip = host
        self.username = username
        self.password = password
        self.port = port
        self.data = data
        self.api = None
        self.api_pool = None
        self.connect()
        self.mensaje = {}

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
        if self.api_pool is not None:
            self.api_pool.disconnect()
            print("Conexión cerrada")

    def create_queue(self, secret_params):

        if self.api is None:
            self.data['error'] = 'No hay conexión a la API de Mikrotik.'
            print("no hay conexion")
            return self.data

        # secret_params={queue_name, target_ip, 
        #          max_limit, burst_limit, limit_at,
        #         burst_threshold, burst_time, priority, data} el name y el target_ip deben ser diferentes a otra cola yacreada
        
        try:
            # Obtener el recurso de colas
            queues_resource = self.api.get_resource('/queue/simple')

            # Crear la cola usando el método add()
            queues_resource.add(**secret_params)

        except Exception as e:       
                self.data['error'] = str(e)
            
        return self.data

    def editar_queue(self, queue_name, queue_params, data):
        if self.api is None:
            data['error'] = 'No hay conexión a la API de Mikrotik.'
            return False
            #     queue_params = {
            #     'name': new_name,
            #     'target': target_ip,
            #     'max-limit': max_limit,
            #     'limit-at': f'{limit_at_upload}/{limit_at_download}',
            #     'priority': priority,
            #     'burst-limit': f'{burst_limit_upload}/{burst_limit_download}',
            #     'burst-threshold': f'{burst_threshold_upload}/{burst_threshold_download}',
            #     'burst-time': f'{burst_time_upload}/{burst_time_download}',
            #     'queue': f'{queue_type_upload}/{queue_type_download}',
            #     'parent': parent
            # } 
        try:
            queues_resource = self.api.get_resource('/queue/simple')
            # Obtener todas las colas
            queues = queues_resource.get()
            # Buscar la cola por nombre
            queue_to_edit = None
            for queue in queues:
                if queue['name'] == queue_name:
                    queue_to_edit = queue
                    # print(queue_to_edit)
                    break

            if queue_to_edit:
                queues_resource.set(id=queue_to_edit['id'], **queue_params)
                print("cola Actualizada")
                return True
            else:
                print('no se encontro la queue')
                data['error'] = 'No se encontro esta queue'

        except Exception as e:       
                data['error'] = str(e)
                return False


    def eliminar_queue(self, queue_name):
        if self.api is None:
            self.data['error'] = "Mikrotik desconectada"
            return self.data

        try:
            # Obtener el recurso de colas
            queues_resource = self.api.get_resource('/queue/simple')

            # Obtener todas las colas
            queues = queues_resource.get()

            # Buscar la cola por nombre
            queue_to_delete = None
            for queue in queues:
                if queue['name'] == queue_name:
                    queue_to_delete = queue
                    break

            if queue_to_delete:
                # Eliminar la cola utilizando el método remove()
                queues_resource.remove(id=queue_to_delete['id'])
                print("Cola eliminada")
                return True
            else:
                self.data['error'] = 'No se encontró la cola'

        except Exception as e:
            self.data['error'] = str(e)

        return self.data

    def create_secret_pppoe(self, secret_nuevo):
        if self.api is None:
            self.data['error'] = 'No hay conexión a la API de Mikrotik.'
            return  False
        else:
            self.mensaje["secret1"]="ok acceso  ala mikrotik"
            print(self.mensaje["secret1"])
        
        try:
            create_ppp = self.api.get_resource('/ppp/secret')
            self.mensaje["secret2"]="accediendo a la ruta de creacion"
            print(self.mensaje["secret2"])
            # secret_nuevo = {
            #     'name': nombre_servicio,
            #     'password': password,
            #     'service': 'pppoe',
            #     'profile': nombre_perfil
            # }
            create_ppp.add(**secret_nuevo)
            self.mensaje["secret3"]="creando el secret"
            print(self.mensaje["secret3"])

            return True
        except Exception as e:
            self.data['error'] = str(e)
            error_msg = f"Error al crear secret PPPoE: {str(e)}"
            self.data['error'] = error_msg
            self.mensaje["error"] = error_msg
            return False

        finally:
            print("Resumen de la operación:")
            for key, value in self.mensaje.items():
                print(f"{key}: {value}")

    def editar_secret_pppoe(self, usuarioppp, secret_params,data):
        if self.api is None:
            data['error'] = 'No hay conexión a la API de Mikrotik.'
            return False
        try:
            secrets_resource = self.api.get_resource('/ppp/secret')
            secrets = secrets_resource.get()
            secret_to_edit = None
            for secret in secrets:
                if secret['name'] == usuarioppp:
                    secret_to_edit = secret
                    break

            if secret_to_edit:
                secrets_resource.set(id=secret_to_edit['id'], **secret_params)
                print("pppoe actualizado")
                return True
            else:
                print('no se encontro el secret')
                data['error'] = 'No se encontro este secret'
                return False
            
        except Exception as e:
            data['error'] = str(e)
            return False
            
    def eliminar_secret_ppp(self, usuarioppp, data):
        if self.api is None:
            self.data['error'] = 'No hay conexión a la API de Mikrotik.'
            return False
        
        try:
            secrets_resource = self.api.get_resource('/ppp/secret')
            secrets = secrets_resource.get()
            secret_to_delete = None
            for secret in secrets:
                if secret['name'] == usuarioppp:
                    secret_to_delete = secret
                    break

            if secret_to_delete:
                secrets_resource.remove(id=secret_to_delete['id'])
                print("secret eliminada")
                return True
            else:
                return False
        except Exception as e:
            data['error'] = str(e)
            return False

    def deshabilitar_servicio(self, target_ip,queue_name, address_list):
        if self.api is None:
            self.data['error'] = 'No hay conexión a la API de Mikrotik.'
            return
        
        try:
            # Definir los parámetros para crear la cola en la lista
            rule_params = {
                'list': address_list,  # La cadena de reenvío
                'address': target_ip, # ip del cliente
                'comment': queue_name,  # Nombre de la queue
            }
            address_list = self.api.get_resource('/ip/firewall/address-list')
            addresses  = address_list.get()
            rule_added = False

            for address in addresses :
                if address.get('address') == target_ip:
                    if address.get('list') == 'Servicios_autorizados':
                        print(address)
                        address_list.remove(id=address.get('id'))
                        print("queue elimnado de la lista Servicios_autorizados")
                        address_list.add(**rule_params)
                        print("queue agregado a la lista Morosos")
                        rule_added = True
                        break

                    elif address.get('list') == 'Morosos':
                        print("El servicio ya se encuentra deshabilitado")
                        rule_added = True
                        break

            if not rule_added:
                address_list.add(**rule_params)
                print("Queue agregado a la lista servicio autorizado")

            print("Servicio deshabiitado")
        except Exception as e:
            self.data['error'] = str(e)

        return True

    def habilitar_servicio(self, target_ip, queue_name,address_list):
        if self.api is None:
            self.data['error'] = 'No hay conexión a la API de Mikrotik.'
            return
        
        rule_params = {
                'list': address_list,  # La cadena de reenvío
                'address': target_ip, # ip del cliente
                'comment': queue_name,  # Nombre de la queue
            }

        try:
            address_list = self.api.get_resource('/ip/firewall/address-list')
            addresses  = address_list.get()
            rule_added = False

            for address in addresses :
                if address.get('address') == target_ip:
                    if address.get('list') == 'Morosos':
                        print(address)
                        address_list.remove(id=address.get('id'))
                        print("queue elimnado de la lista Morosos")
                        address_list.add(**rule_params)
                        print("queue agregado a la lista servicio autorizado")
                        rule_added = True
                        break

                    elif address.get('list') == 'Servicios_autorizados':
                        print("El servicio ya se encuentra habilitado")
                        rule_added = True
                        break

            if not rule_added:
                address_list.add(**rule_params)
                print("Queue agregado a la lista servicio autorizado")

                # Crear la cola usando el método add()
                # queues_resource.add(**rule_params)
        except Exception as e:
            print("No se pudo establecer la conexión:", str(e))

        return True

    def obtener_segmentos_ip(self):
        if self.api is None:
            self.data['error'] = 'No hay conexión a la API de Mikrotik.'
            print("no hay conexion a la mikrptik")
            return

        try:
            segmentos_resource = self.api.get_resource('/ip/address')
            segmentos = segmentos_resource.get()
            return [segmento['address'] for segmento in segmentos]

        except Exception as e:
            self.data['error'] = str(e)
            return []
        
        finally:
            self.close()

    def crear_perfil_pppoe(self,perfil_nuevo):
        if self.api is None:
            self.data['error'] = 'No hay conexión a la API de Mikrotik.'
            print("no hay conexion a la mikrptik")
            return
        
        try:
            profile_ppp = self.api.get_resource('/ppp/profile')
            # profile_nuevo = {
            #     'name': nombre_servicio,
            #     'use-mpls': password,
            #     'use-compression': 'pppoe',
            #     'use-encryption': 'default',
            #     'only-one': 'default',
            #     'change-tcp-mss': 'default',
            #     'use-upnp': 'default',
            #     'rate-limit': 'rate-limit',
            #     'dns-server': 'default',
            # }
            profile_ppp.add(**perfil_nuevo)
        except Exception as e:
            self.data['error'] = str(e)
            return self.data

        finally:
            self.close()

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


# data = {}
# ip='192.168.200.1'
# username='COMUNICAR'
# password='C0MUNIC4RS4S'
# port=8750
# address_list = "Morosos"
# target_ip = '192.168.200.56'
# queue_name = "prueba de corte"

# rule_params = {
#                 'list': address_list,  # La cadena de reenvío
#                 'address': target_ip, # ip del cliente
#                 'comment': queue_name,  # Nombre de la queue
#             }
# # deshabilitar_servicio(self, target_ip,queue_name, rule_params)
# test_api = apimikrotik(ip, username, password, port, data)
# test_api.deshabilitar_servicio(target_ip,queue_name, rule_params)

# # Verificar si hubo errores
# if 'error' in data:
#     print(f"Error: {data['error']}")
# else:
#     print("secret creado correctamente")

# print(data)
# RoundRobin_tickets

Pasos para deploy:
* Configurar tipo de base de datos y ruta de los logs (archivo: config/conf.cfg)
* Configurar las credenciales de la base de datos, por defecto usa sqlite [otras opciones; postgres y mysql] (archivo: config/.env)
* Configurar el puerto del servidor web de flask, por defecto usa el 5000 (archivo: docker-compose.yml)
* Ejecutar archivo de despliegue (archivo: deploy.sh)

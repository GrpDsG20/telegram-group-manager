¿Dónde obtener el api_id y api_hash?
- Visita: https://my.telegram.org/apps
- Inicia sesión con tu número de Telegram.
- Crea una nueva aplicación y obtendrás el api_id y api_hash necesarios para el archivo config.yaml.

![Image](https://github.com/user-attachments/assets/8e0ae089-523d-4729-9abc-5bb14145f44d)

Es importante tener instalado y configurado Telegram Desktop.

1. Ejecuta el script con el siguiente comando:
   python main.py

2. Se solicitará el código de verificación de Telegram.
   - Este código llegará al número configurado en el archivo config.yaml.
   - Ingresa el código cuando se te pida.

3. El script comenzará a ejecutarse automáticamente:
   - Extraerá los miembros del grupo origen (group_source).
   - Intentará agregarlos al grupo destino (group_target).

4. Requisitos importantes:
   - Debes ser administrador en ambos grupos (origen y destino).
   - También funcionará si el grupo origen es público

5. Consideraciones:
   - Solo se pueden añadir usuarios que permitan ser agregados por otros.
   - Telegram impone límites diarios y podría restringir la cuenta por actividad sospechosa.

6. Para evitar bloqueos:
   - El script usa un sistema de delay progresivo.
   - A medida que se agregan usuarios, el tiempo de espera entre cada uno aumenta automáticamente.

![Image](https://github.com/user-attachments/assets/457c9498-8b05-4d6e-9fe6-58b39533cf52)

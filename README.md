> ⚠️ El 80% de este código se ha escrito con IA.

# TeamBudgets 💰📊

Servidor de objetos presupuestarios 


## Deploy

```bash
cd docker/hub
docker compose up -d
```

## Seguridad

Las páginas están protegidas por usuario password. El valor por defecto es `admin` con password `admin`.

Se emplea el siguiente módulo de login [https://github.com/mkhorasani/Streamlit-Authenticator](https://github.com/mkhorasani/Streamlit-Authenticator).

El path del [config file](https://github.com/mkhorasani/Streamlit-Authenticator) se puede setear a través de la variable de entorno `AUTH_CONFIG_FILE`.

```yaml
cookie:
  expiry_days: 1
  key: key
  name: name
credentials:
  usernames:
    admin:
      email: admin@admin.com
      failed_login_attempts: 0 
      first_name: admin
      last_name: admin
      logged_in: False 
      password: admin 
```

## Documentación 📚

* [https://teambudgets.readthedocs.io/](https://teambudgets.readthedocs.io/) 

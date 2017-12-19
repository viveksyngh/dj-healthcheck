# Django Healthcheck

### A Pluggable Django App to get health status of different backend services used by Django project


### Supported services 
1. Databases(Any Database)
2. Caches
3. Celery Worker
4. Message Broker(Redis/RabbitMQ)
5. Salesforce(Make sure you add following setting varibales in Django settings ```SF_USERNAME```, ```SF_PASSWORD```, ```SF_TOKEN```, ```SF_HC_QUERY```

### Future Plan 
1. Add a dashbaord page


### Installation 
```
pip install git+https://github.com/viveksyngh/dj-healthcheck.git
```


### Configurations

##### Add the following to your ```settings.py``` module:

```
INSTALLED_APPS = (
    ...  # Make sure to include the default installed apps here.
    'healthcheck',
)
```


##### Add the following to your ```urls.py``` module in your project:


```
from  healthcheck import urls as healthcheck_urls

...
...

urlpatterns = [
    ...
    url(r'^healthcheck/', include(healthcheck_urls)),
    ...
]
```
API can be used from this url ```APP_BASE_URL/healthcheck/api/```

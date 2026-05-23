from mangum import Mangum
from healthcare_dashboard.asgi import application

handler = Mangum(application)

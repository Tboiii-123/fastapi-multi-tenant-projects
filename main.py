from fastapi import FastAPI
from database import Base, engine
from routers import tenants, users, projects
import auth

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Multi-Tenant SaaS API")

# Routers
#It has 3 params here
#first the router name or identifire,
#Second prefix  name used in the url pattern as a prefix before the acutal path
#Third tags=["tenants"] — groups these endpoints in OpenAPI/Swagger UI.

app.include_router(tenants.router, prefix="/tenants", tags=["Tenants"])
app.include_router(users.router, prefix="/users", tags=["Users"])

app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])


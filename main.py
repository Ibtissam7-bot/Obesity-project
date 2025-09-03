# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from database import models
# from database.database import engine

# from routes import auth as auth_routes
# from routes import predictions as predictions_routes
# # from .routes import livres as livres_routes
# # from .routes import reservations , loans
# # from .routes import recommandations as reco_routes
# # from .routes import stats 
# # from .routes import users 
# # from .routes import statistiques 

# # Crée les tables si elles n'existent pas
# models.Base.metadata.create_all(bind=engine)

# app = FastAPI(title="Bib Readers API")

# # (optionnel) CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # à restreindre en prod
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Routes
# app.include_router(auth_routes.router)   
# app.include_router(predictions_routes.router)  
# # app.include_router(livres_routes.router) 
# # app.include_router(reservations.router)
# # app.include_router(loans.router)
# # app.include_router(reco_routes.router)
# # app.include_router(stats.router)
# # app.include_router(statistiques.router)
# # app.include_router(users.router)

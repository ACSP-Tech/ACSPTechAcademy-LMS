from fastapi.middleware.cors import CORSMiddleware

def configure_cors(app):
    """Configure CORS middleware for the FastAPI app."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

#on stable production
# def configure_cors(app): 
#     app.add_middleware( 
#         CORSMiddleware, 
#         allow_origins=["https://yourfrontend.com"],  # Specific domains
#         allow_credentials=True, 
#         allow_methods=["GET", "POST", "PUT", "DELETE"],  # Specific methods
#         allow_headers=["*"], 
#     )

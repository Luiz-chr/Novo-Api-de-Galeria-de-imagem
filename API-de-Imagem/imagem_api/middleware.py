from fastapi.middleware.cors import CORSMiddleware

def setup_middleware(app):
    """
    Configura as permissões de acesso da API.
    allow_origins=["*"] permite que qualquer site/front-end 
    acesse sua API (ideal para desenvolvimento).
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

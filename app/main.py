from fastapi import FastAPI
from app.routers import users, auth, sessions
from app.routers.task_router import task_router, comments_router

app = FastAPI(
    title='Teste BackEnd Sou Junior-candidato Albert',
    description='Teste para processo seletivo SouJunior',
    version='1.0',
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(sessions.router)
app.include_router(task_router)
app.include_router(comments_router)

@app.get('/health')
def health_check():
    return {'status': 'OK'}
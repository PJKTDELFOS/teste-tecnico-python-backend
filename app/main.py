from fastapi import FastAPI
from app.routers import users,auth,sessions,logs


app=FastAPI(
    title='Teste BackEnd Sou Junior-candidato Albert',
    description='Teste para processo seletivo SouJunior',
    version='1.0',
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(sessions.router)
app.include_router(logs.router)


@app.get('/health')
def health_check():
    return {'status': 'OK'}



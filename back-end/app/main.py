from fastapi import FastAPI

app = FastAPI(title = "Meu Bolso")

@app.get("/hello")
def hello():
    return {"mensagem:" "Olá Meu Bolso"}

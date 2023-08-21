from fastapi import FastAPI


app = FastAPI()
# se torna um decorator que possui
# verbos http depois de instanciado


@app.get('/msg')  # metodo que sera executado (get) no endpoint ('/')
async def message():  # funcao que sera chamada
    return {'msg': 'fastapi on'}

if __name__ == '__main__':

    # para executar "python +nome do aquivo"
    import uvicorn

    uvicorn.run(
        'main:app', host='0.0.0.0',
        port=8000, log_level='info', reload=True
    )

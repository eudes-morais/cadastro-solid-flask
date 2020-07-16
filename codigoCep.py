import requests as req

def buscaCep(cep):
    resp = req.get("https://viacep.com.br/ws/" + cep + "/json/")
    # print(resp.text)
    return resp.json()
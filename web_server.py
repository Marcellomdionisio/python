from gerencianet import Gerencianet
import credentials
import sys
import time
from flask import Flask, jsonify
from flask import Flask, request
gn = Gerencianet(credentials.CREDENTIALS)


app = Flask(__name__)
PORT = 500
HOST = "192.168.15.7"

# Make the WSGI interface available at the top level so wfastcgi can get it.

wsgi_app = app.wsgi_app


#________________________Gera Cobrança_____________________________#

@app.route('/')
def gera_cob():
    global ids
    global txid
    valor = request.args['valor']
    valor = float(valor)
    valor=str('%.2f'% (valor))
    print('R$',valor)
    body = {'calendario': {'expiracao':3600},'devedor': {'cpf': '12345678909','nome': 'francisco da silva' },
        'valor': {'original': valor},'chave': 'fc600b18-c10d-432c-a8d6-57ac60acd94a',
            'solicitacaoPagador': 'fc600b18-c10d-432c-a8d6-57ac60acd94a'}

    response =  gn.pix_create_immediate_charge(body=body)
    ids=str(response['loc']['id'])
    txid = str(response['txid'])
    response =txid
    params = {'id': ids }
    response =  gn.pix_generate_QRCode(params=params)
    response=response['qrcode']
    print(response)
    return(response)



#________________________CheckOut____________________________#

@app.route('/check')
def check_out():
   txid = request.args['txid']
   params = {'txid': txid}
   status=  gn.pix_detail_charge(params=params)
   status=str(status['status'])
   print(status)
   return (status)


if __name__ == "__main__":
     app.run(host = HOST, port = PORT)
##


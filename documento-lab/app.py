# import sys
# import os
# from flask import Flask, render_template, request, jsonify
# from azure.core.credentials import AzureKeyCredential
# from azure.core.exceptions import HttpResponseError
# from azure.ai.formrecognizer import DocumentAnalysisClient
# try:
#     from dotenv import load_dotenv
#     load_dotenv()
# except ImportError:
#     print("Faz o L, a env ta configurada mal em")

# app = Flask(__name__)

# # AZURE_ENDPOINT = os.getenv("AZURE_ENDOPOINT")
# # AZURE_KEY = os.getenv("AZURE_KEY")

# ENDPOINT =  os.getenv("DOC_INTEL_ENDPOINT")
# CHAVE =     os.getenv("DOC_INTEL_KEY")
# cliente_documento = DocumentAnalysisClient(
#     endpoint=ENDPOINT,
#     credential=AzureKeyCredential(CHAVE)
# )

# @app.route('/')
# def index():
#     return render_template('index.html')

# print(f"\n --------------------- \n Sistema de Auditoria de Recibo \n  ---------------------")

# caminho_Arq = "meu_recibo.jpg"

# try: 
#     with open(caminho_Arq, "rb") as documentoFisico:
#         print("A enviar documento para análise de docs")
#         operacao = cliente_documento.begin_analyze_document(
#             model_id="prebuilt-receipt",
#             document=documentoFisico
#         )
#         recibos_extraidos = operacao.result()

#         for recibo in recibos_extraidos.documents:
#             nomeLoja = recibo.fields.get("MerchantName")
#             totalGasto = recibo.fields.get("Total")
#             dataCompra = recibo.fields.get("TransactionDate")
#             print("Resultado da Extração: \n")

#             if nomeLoja:
#                 print(f"\n Fornecedor: {nomeLoja.value}")
#             if (dataCompra):
#                 print(f"\n Data da Compra: {dataCompra.value}")
#             if(totalGasto):
#                 print(f"\n O total a reembolsar: R$ {totalGasto.value}")
            


# except FileNotFoundError:
#     print(f"\n [ERRO]: Arquivo não encontrado no {caminho_Arq} na pasta do projeto")

# except Exception as error:
#     print(f"\n [ERRO NA LEITURA] volta tudo \n {error}")
# codigo novo abaixo com html, css e js

import sys
import os
from flask import Flask, render_template, request, jsonify
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.formrecognizer import DocumentAnalysisClient
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Faz o L, a env ta configurada mal em")

app = Flask(__name__)

# AZURE_ENDPOINT = os.getenv("AZURE_ENDOPOINT")
# AZURE_KEY = os.getenv("AZURE_KEY")

ENDPOINT =  os.getenv("DOC_INTEL_ENDPOINT")
CHAVE =     os.getenv("DOC_INTEL_KEY")
cliente_documento = DocumentAnalysisClient(
    endpoint=ENDPOINT,
    credential=AzureKeyCredential(CHAVE)
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analisar', methods=['POST'])
def analisarRecibo():
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado de forma correta."}), 400
        
    arquivo = request.files['file']
    
    if arquivo.filename == '':
        return jsonify({"error": "Nenhum arquivo selecionado."}), 400

    

    try: 
        documento_bytes = arquivo.read()
                
        print("A enviar documento para análise de docs via Web")
        operacao = cliente_documento.begin_analyze_document(
                    model_id="prebuilt-receipt",
                    document=documento_bytes # Passando a variável de bytes corrigida
                )
        recibos_extraidos = operacao.result()

                # Dicionário padrão caso não encontre algum dado
        dados_finais = {
                    "fornecedor": "Não identificado",
                    "data": "Não identificada",
                    "total": "Não identificado"
                }

        for recibo in recibos_extraidos.documents:
                    nomeLoja = recibo.fields.get("MerchantName")
                    totalGasto = recibo.fields.get("Total")
                    dataCompra = recibo.fields.get("TransactionDate")
                    print("Resultado da Extração: \n")

                    if nomeLoja:
                        print(f"\n Fornecedor: {nomeLoja.value}")
                    if (dataCompra):
                        print(f"\n Data da Compra: {dataCompra.value}")
                    if(totalGasto):
                        print(f"\n O total a reembolsar: R$ {totalGasto.value}")
        print(totalGasto)
        return jsonify(dados_finais)



    except Exception as error:
        print(f"[ERRO NA LEITURA] {error}")
        return jsonify({"error": f"Erro na Azure: {str(error)}"}), 500

if __name__ == '__main__':
    print("\n --------------------- \n Sistema de Auditoria de Recibo Iniciado \n  ---------------------")
    app.run(debug=True)
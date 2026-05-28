# import cv2
# import os
# import numpy as np
# import random
# from azure.ai.vision.imageanalysis import ImageAnalysisClient
# from azure.ai.vision.imageanalysis.models import VisualFeatures
# from azure.core.credentials import AzureKeyCredential


# try:
#     from dotenv import load_dotenv
#     load_dotenv()
# except ImportError:
#     print("Baixa o dotenv ne")

# ENDPOINT = os.getenv("AZURE_LANGUAGE_ENDPOINT")
# KEY =      os.getenv("AZURE_LANGUAGE_KEY")

# client_azure = ImageAnalysisClient(
#     endpoint=ENDPOINT,
#     credential=AzureKeyCredential(KEY)
# )

# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     print("Erro: nao foi possível acessar a camera")
#     exit()
# print("Camera ativada")
# print("Mostre um texto/painel para a camera e pressione 'S' para escanear")
# print("Pressione 'q' para sair")

# nome_janela = "Scanner d edocumentos da Azure"
# while True:
#     sucesso, frame = cap.read()
#     if sucesso == None:
#         print("Não foi possível capturar a imagem da câmera")
#         break

#     cv2.imshow(nome_janela, frame)
#     tecla = cv2.waitKey(1)& 0xFF
#     if cv2.getWindowProperty(nome_janela, cv2.WND_PROP_VISIBLE) <1:
#         print("Janela fechada pelo usuario")
#         break
#     if tecla == ord("s"):
#         print("Extraindo texto da imagem")
#             # resultado = client_azure.analyze(
#             #     image_data = dados_img,
#             #     _

#         sucesso_encode, buffer = cv2.imencode("jpg", frame)
#         if not sucesso_encode:print("Erro ao converter a imagem para jpg")
#         continue

#         dados_img = buffer()
#         try:
#             resultado = client_azure.analyze(
#                 image_data = dados_img,
#                 visual_features=[VisualFeatures.READ]
            
#             if resultado.read is None:
#                 print("\n === Dados Extraídos ===")
#                 for bloco in resultado.read.blocks:
#                     for linha in bloco.lines:
#                         texto_extraido = linha.text
#                         print(f"Lido: {texto_extraido}")

#                         pontos = linha.bouding_polygon
#                         if pontos:
#                             pts = np.array([(p.x,p.y) for p in pontos],
#                                            np.int32
#                                            )

#                                            pts = pts.reshape((-1,1,2))
#                                            cv2.polylines(frame, [pts], isClosed=True, color(0, 255, 0), thickness=2)

#                                            x,y = pts[0][0]
#                                            posicao_y_text = max(y -10, 20)
#                                            cv2.putText(
#                                                       frame, texto_extraido, (x, posicao_y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
#                                                       )
#
#                                            print("================")
#                                            cv2.imshow(nome_janela, frame)
#                                            print("Leitura concluida, pressione a tecla para continuar")
#                                            cv2.waitKey(0)
#                                      else:
#                                                   print("OCR: Nenhum texto detectado")
#
#
#


#             )


import cv2
import os
import numpy as np
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Baixa o dotenv ne")

ENDPOINT = os.getenv("AZURE_LANGUAGE_ENDPOINT")
KEY = os.getenv("AZURE_LANGUAGE_KEY")

client_azure = ImageAnalysisClient(
    endpoint=ENDPOINT,
    credential=AzureKeyCredential(KEY)
)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erro: nao foi possível acessar a camera")
    exit()

print("Camera ativada")
print("Mostre um texto/painel para a camera e pressione 'S' para escanear")
print("Pressione 'q' para sair")

nome_janela = "Scanner d edocumentos da Azure"
while True:
    sucesso, frame = cap.read()
    if sucesso is False:
        print("Não foi possível capturar a imagem da câmera")
        break

    cv2.imshow(nome_janela, frame)
    tecla = cv2.waitKey(1) & 0xFF
    
    if cv2.getWindowProperty(nome_janela, cv2.WND_PROP_VISIBLE) < 1:
        print("Janela fechada pelo usuario")
        break
        
    if tecla == ord("s"):
        print("Extraindo texto da imagem")

        sucesso_encode, buffer = cv2.imencode(".jpg", frame)
        if not sucesso_encode:
            print("Erro ao converter a imagem para jpg")
        else:
            dados_img = buffer.tobytes()
            try:
                resultado = client_azure.analyze(
                    image_data = dados_img,
                    visual_features=[VisualFeatures.READ]
                )

                if resultado.read is not None:
                    print("\n === Dados Extraídos ===")
                    for bloco in resultado.read.blocks:
                        for linha in bloco.lines:
                            texto_extraido = linha.text
                            print(f"Lido: {texto_extraido}")

                            pontos = linha.bounding_polygon
                            if pontos:
                                pts = np.array([(p.x, p.y) for p in pontos], np.int32)
                                pts = pts.reshape((-1, 1, 2))
                                cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

                                x, y = pts[0][0]
                                posicao_y_text = max(y - 10, 20)
                                cv2.putText(frame, texto_extraido, (x, posicao_y_text), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                    print("================")
                    cv2.imshow(nome_janela, frame)
                    print("Leitura concluida, pressione qualquer tecla para continuar")
                    cv2.waitKey(0)
                else:
                    print("OCR: Nenhum texto detectado")
            except Exception as erro:
                print(f"Erro na análise: {erro}")

    if tecla == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("Scanner concluido")
# import os
# from flask import Flask, render_template, request, jsonify
# from azure.core.credentials import AzureKeyCredential
# from azure.core.exceptions import HttpResponseError
# from azure.ai.formrecognizer import DocumentAnalysisClient
# from openai import AzureOpenAI
# import azure.cognitiveservices.speech as speech_sdk



# speech_config = None


# def configuracao_fala():
# #"""
        
# #"""
#     global speech_config
#     print("e")
#     azure_speech_key = os.get("AZURE_SPEECH_KEY")
#     speech_region = os.getenv("AZURE_REGION")

#     speech_config = speech_sdk.SpeechConfig(subscription=azure_speech_key, region=speech_region)
#     speech_config.speech_synthesis_voice_name = "pt-BR-FranciscaNeural"

# def falar_texto(texto_pr_falar):
#     global speech_config
#     if not speech_config:
#         print("ERRO: O servico de fala não está configurado!")
#         return
#     audio_config = speech_sdk.audio.AudioOutputConfig(use_default_speaker=True)
#     speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
#     speech_synthesizer.speak_text_async(texto_pr_falar).get()

# def main():
#     try:
#         from dotenv import load_dotenv
#         load_dotenv()
#         configuracao_fala()
#         client = AzureOpenAI(azure_endpoint=os.getenv("AZURE_OAI_ENDPOINT"),
#                              api_key=os.getenv("AZURE_OAI_KEY"),
#                              api_version="2024-02-15-preview")
        
#         deployment_name = os.getenv("AZURE_OAI_DEPLOYMENT")
#         system_message ="""
#         Você é um assistente de IA prestativo e amigavel. Responda sempre de forma muito curta, direta e em tom de conversa, pois sua resposta será lida me voz alta por um sintetizador de falar.
#         """

#         messages_array = [{"role": "system", "content": system_message}]
#         print("--- ChatBot IA com voz iniciado (digite quit para sair) --- ")
#         while True:
#             inpt_text = input("Você saiu!")
#             if inpt_text.lower() == 'quit':
#                 print("Sistema encerrado")
#                 break
#             messages_array.append({"role":"system", "content": inpt_text})
#             print("A IA está processando")


#             response = client.chat.completions.create(
#                 model=deployment_name,
#                 messages=messages_array,
#                 max_tokens=50
#             )

#             generate_text= response.choices[0].message.content
#             messages_array.append({"role": "assistant", "content": generate_text})
#             print(f"IA: {generate_text}")
#             falar_texto(generate_text)
#     except Exception as e:
#         print(f"Siga o Erro: \n {e}")
# if __name__ == '__main__':
#     main()

# # try:
# #     from dotenv import load_dotenv
# #     load_dotenv()
# # except ImportError:
# #     print("se lascou na env em")

# # app = Flask(__name__)


# # ENDPOINT = os.getenv("AZURE_OAI_ENDPOINT")
# # KEY  = os.getenv("AZURE_OAI_KEY")
# # oAI  = os.getenv("AZURE_OAI_DEPLOYMENT")
# # AZURE_SPEECH_KEY  = os.getenv("")
# # AZURE_DEPLOYMENT  = os.getenv("")



import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import azure.cognitiveservices.speech as speech_sdk

speech_config = None

def configurar_fala():
    global speech_config
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION")
    speech_config = speech_sdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_synthesis_voice_name = "pt-BR-FranciscaNeural"

def falar_texto(texto_para_falar):
    if not speech_config:
        print("[Erro] O serviço de fala não está configurado.")
        return
    audio_config = speech_sdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesizer.speak_text_async(texto_para_falar).get()

def main():
    try:
        load_dotenv()
        configurar_fala()
        client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OAI_KEY"),
            api_version="2024-02-15-preview"
        )
        deployment_name = os.getenv("AZURE_OAI_DEPLOYMENT")
        system_message = """Você é um assistente de IA prestativo e amigável.
        Responda sempre de forma MUITO curta, direta e em um tom de conversa,
        pois a sua resposta será lida em voz alta por um sintetizador de fala."""
        messages_array = [{"role": "system", "content": system_message}]
        print("--- Chatbot IA com Voz Iniciado (digite 'quit' para sair) ---")

        while True:
            input_text = input("\nVocê: ")
            if input_text.lower() == "quit":
                print("Encerrando o sistema...")
                break
            messages_array.append({"role": "user", "content": input_text})
            print("IA está a processar...")
            response = client.chat.completions.create(
                model=deployment_name,
                messages=messages_array,
                max_tokens=150
            )
            generated_text = response.choices[0].message.content
            messages_array.append({"role": "assistant", "content": generated_text})
            print(f"IA: {generated_text}")
            falar_texto(generated_text)

    except Exception as ex:
        print(f"Ocorreu um erro catastrófico na execução: {ex}")

if __name__ == '__main__':
    main()
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()
TEMP_PATH = os.environ.get("TEMP_PATH", "src/temp")
IS_USING_IMAGE_RUNTIME = bool(os.environ.get("IS_USING_IMAGE_RUNTIME", False))

def get_sentiments_helper(documents):
    url_servicio = os.environ.get('ENDPOINT')+"language/:analyze-text?api-version=2023-04-01"
    payload = {
        "kind": "SentimentAnalysis",
        "analysisInput": {"documents": documents},
    }
    headers = {"Ocp-Apim-Subscription-Key": os.environ.get('LANGUAGE_KEY')}
    try:
        response = requests.post(url_servicio, headers=headers, json=payload, timeout=120)
        if response.status_code == 200:            
            return response.json()["results"]["documents"]
        else:
            print("Respuesta no OK")
    except requests.RequestException as exc:
        return f"Could not reach Azure Speech service: {exc}", 502

def get_sentiment_analysis(phrases):
    retval = []
    documents = []
    for phrase in phrases:
        id = str(phrase["speaker"])+"-"+str(phrase["offsetMilliseconds"])
        documents.append({
            "id": id,
            "language": "es",
            "text": phrase["text"],
        })
    # We can only analyze sentiment for 10 documents per request.
    def chunk(lst, size):
        for i in range(0, len(lst), size):
            yield lst[i:i + size]

    # Get the sentiments for each chunk of documents.
    result_chunks = list(map(lambda xs: get_sentiments_helper(xs), chunk(documents, 10)))

    for result_chunk in result_chunks:
        for document in result_chunk:
            retval.append({
                "speaker":int(document["id"].split("-")[0]),
                "offset":int(document["id"].split("-")[1]),
                "documents": document
            }
            )
    with open(get_runtime_temp_path()+'/response_sentiment.json', 'w', encoding='utf-8') as json_file:
        json.dump(retval, json_file, ensure_ascii=False, indent=4)
    return retval

def obtener_analisis(file):
    if not os.path.exists(get_runtime_temp_path()):
        os.makedirs(get_runtime_temp_path())
    transcripcion = obtener_transcripcion(file)
    analisis_sentimientos = get_sentiment_analysis(transcripcion["phrases"])

    def solo_mensajes(elemento):
        clase_text = "agente-message" if elemento["speaker"]==1 else "user-message"
        return {"texto":elemento["documents"]["sentences"][0]["text"],"clase":clase_text,"sentimiento":elemento["documents"]["sentiment"]}
    
    sentiment_result = get_sentiment_analysis(transcripcion["phrases"])
    resultado_json = list(map(solo_mensajes,sentiment_result))
    return resultado_json, transcripcion["combinedPhrases"][0]["text"]

def obtener_desde_json():
    try:
        transcr_json = get_runtime_temp_path()+'/response.json'
        with open(transcr_json, encoding='utf8') as file:
            transcripcion = json.load(file)

        sent_json = 'src/temp/response_sentiment.json'
        with open(sent_json, encoding='utf8') as file:
            sentiment_result = json.load(file)

        def solo_mensajes(elemento):
            clase_text = "agente-message" if elemento["speaker"]==1 else "user-message"
            return {"texto":elemento["documents"]["sentences"][0]["text"],"clase":clase_text,"sentimiento":elemento["documents"]["sentiment"]}

        resultado_json = list(map(solo_mensajes,sentiment_result))
        return resultado_json, transcripcion["combinedPhrases"][0]["text"]
    except Exception as exc:
        return f"Se presentó una excepción: {exc}", exc
    

def obtener_transcripcion(file):
    url_servicio = os.environ.get('ENDPOINT')+"speechtotext/transcriptions:transcribe?api-version=2024-11-15"
    files = {
        "audio": (file.filename, file.stream, file.mimetype or "application/octet-stream"),
        "definition": (None, json.dumps({"locales": ["en-US","es-MX","pt-BR","fr-FR"],"diarization": {"maxSpeakers": 2,"enabled": True}}), "application/json")
    }
    headers = {"Ocp-Apim-Subscription-Key": os.environ.get('SPEECH_KEY')}

    try:
        response = requests.post(url_servicio, headers=headers, files=files, timeout=120)
        if response.status_code == 200:
            new_data = response.json()
            with open(get_runtime_temp_path()+'/response.json', 'w', encoding='utf-8') as json_file:
                json.dump(new_data, json_file, ensure_ascii=False, indent=4)
                print("Audio procesado con éxito")
            return new_data
        else:
            print("Respuesta no OK")
            return "No se obtubo una buena respuesta al transcribir"
    except requests.RequestException as exc:
        return f"Could not reach Azure Speech service: {exc}", 502

def get_runtime_temp_path():
    if IS_USING_IMAGE_RUNTIME:
        return f"/tmp/{TEMP_PATH}"
    else:
        return TEMP_PATH
    
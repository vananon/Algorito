import telebot
import google.generativeai as genai
from funciones import DefOp
from funciones import RefRespuesta
from funciones import FormularReq
from Codeforces import getProblemas

# Configure the generative AI API
genai.configure(api_key="AIzaSyCOrtq_8NnFXXB8zNSmQMUfEyTSPAavtTk")
TOKEN = "7938398787:AAGWFu-XC7wR_Ea3cEFeaNYpSVEBJ8iPNRg"
bot = telebot.TeleBot(TOKEN)


def crear(user_id):
    if user_id not in user_sessions:
        start_new_session(user_id)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-8b",
    generation_config=generation_config,
  system_instruction="Eres un asistente virtual experto en algoritmos y programación.\n\n## Funciones\n\n* **0 || 6 <nombre_algoritmo> <instruccion_opcional> **: Identifica el algoritmo. Responde con el nombre oficial si existe (ej: \"0BFS\" -> \"0Breath-First Search\"). Si no existe, responde \"NONE\" (ej: \"0SJHG\" -> \"0NONE\").\n* **1 <nombre_algoritmo><instruccion_opcional>**: Describe brevemente el algoritmo. Debes especificar el nombre del algoritmo (ej: \"1Breath-First Search es...\").\n* **2 <nombre_algoritmo> <lenguaje> <instruccion_opcional>**: Muestra solo una plantilla del código del algoritmo en el lenguaje especificado (ej: \"2Breath-First Search Python\").\n* **3 <tema_interes><tema_interes>...**: Recomienda solo un algoritmo existente relacionado con el tema de interés, que sea diferente al tema de interés (ej: \"3Grafos\" -> \"3Dijkstra\"; \"3Dijkstra\" -> \"Bellman-Ford\").\n\n## Instrucciones\n\n* Sigue este formato para interactuar conmigo, cada mensaje debe comenzar con un dígito cual represente la opción, En el caso que el algoritmo de la conversación ya no se hable, el mensaje retorna a '?'.\n\n## Ejemplos\n\n* **Usuario**: 0BFS\n* **Gemini**: 0Breath-First Search\n\n* **Usuario**: 0Djstra\n* **Gemini**: 0Dijkstra\n\n* **Usuario**: 6bfs\n* **Gemini**: 6Breath-First Search \n\n* **Usuario**: 1Breath-First Search\n* **Gemini**: 1Breath-First Search es un algoritmo para recorrer grafos...\n\n* **Usuario**: 1Breath-First Search no entendí lo que dijiste\n* **Gemini**: 1No te preocupes, Breath-First Seach es... \n\n* **Usuario**: 2Breath-First Search Python\n* **Gemini**: [Código en Python]\n\n* **Usuario**: 3Ordenamiento\n* **Gemini**: 3Merge Sort\n\n* **Usuario**: 2Me gusta dormir.\n* **Gemini**: ?",
)

user_sessions = {}
user_phases = {}
user_ALGORIT = {}

def start_new_session(user_id):
    history = []
    user_phases[user_id] = "-"
    user_ALGORIT[user_id] = "NONE"
    chat_session = model.start_chat(history=history)
    user_sessions[user_id] = chat_session


@bot.message_handler(commands=['start'])
def welcome(message):
    crear(message.chat.id)
    bot.reply_to(message, '¡Te saluda Algorito! El robot más experto en Algoritmos y Estructuras de datos. Escribe /help para descubrir cómo te puedo ayudar :)')

@bot.message_handler(commands=['practicar'])
def practicar(message):
    crear(message.chat.id)
    bot.reply_to(message, '¡La práctica siempre lleva al maestro!\n Indique su nombre de usuario de codeforces para ayudarlo :)')
    user_phases[message.chat.id] = "6"
    user_ALGORIT[message.chat.id]="NONE"

@bot.message_handler(commands=['aprender'])
def aprender(message):
    crear(message.chat.id)
    bot.reply_to(message, 'Soy bueno explicando algoritmos,\n¿Qué algoritmo deseas buscar?')
    user_phases[message.chat.id] = "0"
    user_ALGORIT[message.chat.id]="NONE"

@bot.message_handler(commands=['recomendar'])
def recomendar(message):
    crear(message.chat.id)
    bot.reply_to(message, 'Claro que te puedo ayudar a elegir el siguiente algoritmo que puedes aprender.\n ¿Con qué algoritmos tienes experiencia?\n¿Qué te gusta hacer? ')
    user_phases[message.chat.id] = "3"
    user_ALGORIT[message.chat.id]="NONE"

@bot.message_handler(commands=['help'])
def help_command(message):
    crear(message.chat.id)
    bot.reply_to(message, 'Tienes dudas sobre un algoritmo y Algorito te responderá. Puedes usar los comandos: \n /start: Inicia el bot \n /help: Muestra este mensaje de ayuda\n /aprender: Investigar sobre x algoritmo\n /practicar: Mejora tus habilidades en programación competitiva \n /recomendar: Algorito te sugerirá un algoritmo nuevo a aprender en base a tus conocimientos :) \n \n Por favor, marcar un comando antes de empezar a preguntar')



@bot.message_handler(func=lambda m: True)
def rpt(message):
    user_id = message.chat.id
    crear(message.chat.id) 
    chat_session = user_sessions[user_id]
    respuesta = '---'

    respuesta, user_phases[user_id] = DefOp(user_phases[user_id], message.text, user_ALGORIT[user_id], respuesta)
    if(user_phases[user_id]== "6"):
        respuesta = getProblemas(message.text)
        bot.reply_to(message, respuesta)

    elif respuesta == "---" and user_phases[user_id] != "-":
        try:
            messageOfc = message.text
            messageOfc = FormularReq(user_phases[user_id], messageOfc, user_ALGORIT[user_id])
            chat_session.send_message(messageOfc)
            respuesta = chat_session.last.text
            user_phases[user_id], respuesta, user_ALGORIT[user_id] = RefRespuesta(user_phases[user_id], respuesta, user_ALGORIT[user_id])
            bot.reply_to(message, respuesta)

        except Exception as e:
            bot.reply_to(message, f"Lo siento, ocurrió un error: {str(e)}. Inténtalo de nuevo más tarde.")
    elif user_phases[user_id] != "-" and user_phases[user_id]!= "2":
        bot.send_message(message.chat.id, 'Antes de ayudarte, no te olvides de utilizar los comandos /aprender, /recomendar o /practicar para saber lo que necesitas :=) ')
    else:
        bot.reply_to(message, respuesta)

if __name__ == "__main__": 
	bot.polling(none_stop=True)

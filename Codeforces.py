import requests

def getProblemas(mensaje):
    respuesta = ""
    handle = mensaje
    url_user_info = f"https://codeforces.com/api/user.info?handles={handle}"
    
    try:
        response_user = requests.get(url_user_info)
        data_user = response_user.json()

        if data_user['status'] == 'OK':
            rating_usuario = data_user['result'][0].get('rating', None)
            if rating_usuario is None:
                return f"El usuario {handle} no tiene un rating disponible."
            
            respuesta += f"Wow! Parece que el rating de {handle} es: {rating_usuario}... Muy bueno, pero veamos qué problemas te ayudarán a mejorar el rating \n"
            
            url_problems = "https://codeforces.com/api/problemset.problems"
            response_problems = requests.get(url_problems)
            data_problems = response_problems.json()

            if data_problems['status'] == 'OK':
                problemas = data_problems['result']['problems']
                url_user_status = f"https://codeforces.com/api/user.status?handle={handle}"
                response_status = requests.get(url_user_status)
                data_status = response_status.json()

                problemas_resueltos = {p['problem']['contestId']: p['problem']['index'] 
                                       for p in data_status['result'] if p['verdict'] == 'OK'}
                
                problemas_filtrados = [
                    p for p in problemas 
                    if 'rating' in p and p['rating'] is not None
                    and p['rating'] > rating_usuario
                    and p['rating'] <= rating_usuario + 400
                    and (p['contestId'], p['index']) not in problemas_resueltos
                ]
                
                if problemas_filtrados:
                    respuesta += f"Problemas con rating mayor a {rating_usuario} y como máximo {rating_usuario + 400}, que {handle} no ha resuelto:"
                    i = 0
                    for p in problemas_filtrados:
                        if(i >= 7):
                            break
                        respuesta += f"\n\nTítulo: {p['name']}"
                        respuesta += f"\nRating: {p['rating']}"
                        respuesta += f"\nURL: https://codeforces.com/problemset/problem/{p['contestId']}/{p['index']}"
                        i += 1
                    return respuesta
                else:
                    return f"\nNo se encontraron problemas con rating mayor a {rating_usuario} y como máximo {rating_usuario + 400} que {handle} no haya resuelto."
            else:
                return "Error al obtener los problemas."
        else:
            return f"Parece que el usuario {handle} no existe :(\n Prueba con otro usuario :)."  
    except requests.exceptions.RequestException as e:
        return f"Error al realizar la solicitud: {e}"


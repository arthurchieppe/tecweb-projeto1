from os import error, replace
from utils import load_data, load_template
import urllib
from database.database import Database, Note

def index(request):
    try:
        print("AQUIIIII")
        print(request)
        db = Database('note')
        if request.startswith('POST'):
            request = request.replace('\r', '')  # Remove caracteres indesejados
            # Cabeçalho e corpo estão sempre separados por duas quebras de linha
            partes = request.split('\n\n')
            corpo = partes[1]
            if corpo.split("=")[0] == 'delete':
                id = int(corpo.split("=")[1])
                db.delete(id)
            else:
                params = {}
                # Preencha o dicionário params com as informações do corpo da requisição
                # O dicionário conterá dois valores, o título e a descrição.
                # Posteriormente pode ser interessante criar uma função que recebe a
                # requisição e devolve os parâmetros para desacoplar esta lógica.
                # Dica: use o método split da string e a função unquote_plus

                #titulo=Sorvete+de+banana 
                #detalhes=Coloque+uma+banana+no+congelador+e+espere.+Pronto%21+1%2B1%3D
                for chave_valor in corpo.split('&'):
                    if chave_valor.startswith("titulo"):
                        params["titulo"] = urllib.parse.unquote_plus(chave_valor[chave_valor.find("=")+1:], encoding="utf-8", errors="replace")
                    if chave_valor.startswith("detalhes"):
                        params["detalhes"] = urllib.parse.unquote_plus(chave_valor[chave_valor.find("=")+1:], encoding="utf-8", errors="replace")
                db.add(Note(None, params["titulo"], params["detalhes"]))


        # Cria uma lista de <li>'s para cada anotação
        # Se tiver curiosidade: https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
        note_template = load_template('components/note.html')
        # db = Database('note')
        print(db.get_all())
        notes_li = [
            note_template.format(id=dados.id, title=dados.title, details=dados.content)
            for dados in db.get_all()
        ]
        
        notes = '\n'.join(notes_li)

        return load_template('index.html').format(notes=notes).encode()
    except:
        return load_template('404.html').encode()

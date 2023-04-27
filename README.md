# nltk_tree

app needs to work this libraries, you can inspall it with pip install:
nltk.tree,
fastapi

uvicorn as a server

to start app you can use uvicorn with command:
uvicorn ntlk:app

to access started app use:
http://127.0.0.1:8000/paraphrase?tree= "your tree"

app returns a list of parse trees in json format

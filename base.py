# Imports
# JSON, pour lire les informations récupérées via une API
import json
# OS, pour accéder à différentes ressources locales
import os
# Interactions, le module principal qui sert à se connecter à l'API de Discord, dans sa version 4.4.0
import interactions
# Requests, pour envoyer des requêtes à différents services
import requests
# La fonction load_dotenv, pour récupérer les variables d'environnement
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Récupération du token Discord présent dans le .env
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

# On crée une variable contenant le chemin complet de l'emplacement du bot
dirname = os.path.dirname(os.path.realpath(__file__))

# On définit le bot
bot = interactions.Client(token=DISCORD_TOKEN)

# On ajoute une liste pour stocker les identifiants des serveurs où le bot se trouver
guild_ids = []

# Événement de démarrage du bot
@bot.event
# Fonction de l'événement
async def on_ready():
    # On itère sur les serveurs du bot
    for guild in bot.guilds:
            # Pour chaque serveur, on ajoute son identifiant dans la liste précédemment définie
            guild_ids.append(guild.id)

# Exemple de commande commande
@bot.command(
    # On donne un nom à la commande
    name="chat",
    # On donne une description à la commande
    description="Image de chat",
    # On indique dans quels serveurs la commande sera disponible (ici, on met le nom de la liste pour indiquer qu'il s'agit de tous les serveurs)
    scope=guild_ids,
)
# On définit une fonction associée à la commande
async def chat(ctx):
    try:
        # Requête vers un service renvoyant des images de chat
        r = requests.get('https://cataas.com/cat?json=true')
        # On récupère le contenu renvoyé sous forme de chaîne de caractères
        a = (str(r.content))
        # On adapte la chaîne de caractères selon nos souhaits pour ne pas l'avoir sous forme de bytes
        a = a.replace("b'", "")
        a = a.replace("}'", "}")
        # On convertit en json
        ext = (json.loads(a)['mimetype']).split('/')[1]
        # On récupère l'URL finale contenant l'image de chat
        res = ("https://cataas.com" + json.loads(a)['url'] + "." + ext)
    except:
        # Si jamais le premier service n'est pas disponible, on effectue une requête du même genre, avec les mêmes étapes
        # Requête vers un service renvoyant des images de chat
        r = requests.get('https://aws.random.cat/meow')
        # On récupère le contenu renvoyé sous forme de chaîne de caractères
        c = str(r.content)
         # On adapte la chaîne de caractères selon nos souhaits pour ne pas l'avoir sous forme de bytes
        c = c.replace("\\", "")
        a = c.replace("b'", "")
        a = a.replace("}'", "}")
        # On convertit en json
        ext = (json.loads(a)['file'])
        # On récupère l'URL finale contenant l'image de chat
        res = ext
    try:
        # # On crée un embed pour que le message soit plus propre
        # # Ici, on envoie une image, on ne définit donc qu'un titre et une couleur (vert)
        # embed = interactions.Embed(title='Chat', type=None, description=None, color=65280)
        # # On ajoute l'image à l'embed
        # embed.set_image(url=res)
        # # On envoie l'embed
        # await ctx.send(embeds=embed)

###############################################################################################################################################

        # La dernière mise à jour de Discord bloque les images dans les embeds, on passe donc par un autre moyen pour pouvoir en envoyer
        # On effectue une requête via l'URL précédemment récupérée
        r = requests.get(res, stream=True)
        # Si l'URL est correcte, on enregistre l'image
        if r.status_code == 200:
            # On ouvre un fichier en mode Write-Byte
            with open(f"{dirname}/img.png", 'wb') as f:
                # Pour chaque partie de 1024 octets dans le fichier récupéré via l'URL
                for chunk in r.iter_content(1024):
                    # On écrit cette partie dans le fichier en local
                    f.write(chunk)
        # On crée un fichier Discord contenant l'image que l'on vient de télécharger
        file = interactions.File(f'{dirname}/img.png')
        # On envoie le fichier, malheureusement sans embed
        await ctx.send(files=file)
        # On supprime le fichier sur le disque pour avoir un gain de place, mais ce n'est pas obligatoire, il aurait été écrasé à la prochaine exécution de la commande
        os.remove(f'{dirname}/img.png')

    except Exception as e:
        # En cas de problème, on renvoie une erreur
        # On définit un titre, une couleur (rouge) et une description contenant l'erreur
        embed = interactions.Embed(title='Chat', type=None, description=f"Une erreur a eu lieu : {e}", color=16711680)
        # On envoie ensuite l'embed, en "ephemeral", pour que ce ne soit visible que par l'utilisateur ayant exécuté la commande
        await ctx.send(embeds=embed, ephemeral=True)

# On appelle la fonction de démarrage du bot
bot.start()
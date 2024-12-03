from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import json
import requests

# Configuration
HOST = "127.0.0.1"  # Adresse du serveur
PORT = 8000         # Port du serveur
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1313580345165221918/rAbP91ephTBTU7iez_pxXTs4WknLD7RLpYCfnAsH282SVuQfZR85bUZsSin1_Brxxt3n"  # Remplacez par votre webhook Discord

class PoliceToolHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Servir le formulaire HTML
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.html_form().encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Page not found")

    def do_POST(self):
        # Gérer le formulaire soumis
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        form_data = urlparse.parse_qs(post_data.decode('utf-8'))

        # Récupérer les données du formulaire
        nom_prenom = form_data.get("nom_prenom", [""])[0]
        rapport = form_data.get("rapport", [""])[0]
        amendes = form_data.get("amendes", [""])[0]
        saisies = form_data.get("saisies", [""])[0]
        important = form_data.get("important", [None])[0]

        if not important:
            # Si la case "Important" n'est pas cochée
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Vous devez cocher la case 'Important' pour envoyer le rapport.")
            return

        # Préparer l'embed pour Discord
        embed = {
            "embeds": [
                {
                    "title": "🚔 Nouveau rapport pour la BCSO",
                    "color": 255,  # Bleu
                    "fields": [
                        {"name": "Nom et Prénom", "value": nom_prenom, "inline": True},
                        {"name": "Rapport", "value": rapport, "inline": False},
                        {"name": "Amendes", "value": amendes if amendes else "Aucune", "inline": True},
                        {"name": "Saisies", "value": saisies if saisies else "Aucune", "inline": True},
                    ]
                }
            ]
        }

        # Envoyer à Discord via le webhook
        response = requests.post(DISCORD_WEBHOOK_URL, json=embed)
        if response.status_code == 204:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Rapport envoye avec succes !")
        else:
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Erreur lors de l'envoi du rapport. Veuillez reessayer.")

    @staticmethod
    def html_form():
        # Code HTML du formulaire
        return """
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Police Tool - MalyaRolePlay</title>
            <style>
                /* Styles généraux */
                body {
                    font-family: 'Arial', sans-serif;
                    background-color: #1c1f24; /* Fond sombre */
                    color: white;
                    margin: 0;
                    padding: 0;
                }

                /* En-tête */
                header {
                    background-color: #003366; /* Bleu foncé */
                    padding: 20px;
                    text-align: center;
                    border-bottom: 3px solid #FFD700; /* Ligne dorée pour le style policier */
                }

                header h1 {
                    font-size: 2.5rem;
                    margin: 0;
                    color: #FFD700; /* Texte doré */
                }

                header p {
                    font-size: 1.2rem;
                    color: white;
                }

                /* Conteneur du formulaire */
                .form-container {
                    max-width: 600px;
                    margin: 30px auto;
                    padding: 20px;
                    background-color: #2c2f33; /* Gris foncé */
                    border-radius: 10px;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
                }

                /* Champs du formulaire */
                label {
                    font-weight: bold;
                    display: block;
                    margin-top: 10px;
                }

                input, textarea {
                    width: 100%;
                    padding: 10px;
                    margin-top: 5px;
                    margin-bottom: 15px;
                    border: 1px solid #FFD700;
                    border-radius: 5px;
                    font-size: 16px;
                    background-color: #1c1f24; /* Fond sombre pour les champs */
                    color: white;
                }

                input:focus, textarea:focus {
                    outline: none;
                    border-color: #003366; /* Bleu foncé */
                }

                /* Bouton */
                button {
                    width: 100%;
                    padding: 15px;
                    background-color: #003366;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 18px;
                    font-weight: bold;
                    cursor: pointer;
                    transition: background-color 0.3s ease;
                }

                button:hover {
                    background-color: #001f33; /* Plus sombre au survol */
                }

                /* Pied de page */
                footer {
                    text-align: center;
                    padding: 10px;
                    margin-top: 20px;
                    background-color: #003366;
                    color: white;
                    border-top: 3px solid #FFD700;
                }

                footer p {
                    margin: 0;
                    font-size: 0.9rem;
                }
            </style>
        </head>
        <body>
            <header>
                <h1>Police Tool</h1>
                <p>MalyaRolePlay - Rapports et gestion</p>
            </header>

            <div class="form-container">
                <form action="/" method="post">
                    <label for="nom_prenom">Nom et Prénom :</label>
                    <input type="text" id="nom_prenom" name="nom_prenom" placeholder="Exemple : John Doe" required>

                    <label for="rapport">Rapport :</label>
                    <textarea id="rapport" name="rapport" rows="10" placeholder="Détaillez le rapport ici..." required></textarea>

                    <label for="amendes">Amendes :</label>
                    <textarea id="amendes" name="amendes" rows="5" placeholder="Liste des amendes (si applicable)"></textarea>

                    <label for="saisies">Saisies :</label>
                    <textarea id="saisies" name="saisies" rows="5" placeholder="Liste des saisies (si applicable)"></textarea>

                    <input type="checkbox" id="important" name="important" value="1">
                    <label for="important" style="display: inline;">Marquer comme important</label>

                    <button type="submit">Envoyer le rapport</button>
                </form>
            </div>

            <footer>
                <p>&copy; 2024 Police Tool - MalyaRolePlay. Tous droits réservés.</p>
            </footer>
        </body>
        </html>
        """

# Lancer le serveur HTTP
def run_server():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, PoliceToolHandler)
    print(f"Serveur en cours d'exécution sur http://{HOST}:{PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()

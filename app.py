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
        <form id="policeForm">
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

    <script>
        const form = document.getElementById("policeForm");

        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            // Récupérer les données du formulaire
            const nom_prenom = document.getElementById("nom_prenom").value;
            const rapport = document.getElementById("rapport").value;
            const amendes = document.getElementById("amendes").value;
            const saisies = document.getElementById("saisies").value;
            const important = document.getElementById("important").checked;

            if (!important) {
                alert("Vous devez cocher la case 'Important' pour envoyer le rapport.");
                return;
            }

            // Préparer l'embed pour Discord
            const embed = {
                "embeds": [
                    {
                        "title": "🚔 Nouveau rapport pour MalyaRolePlay",
                        "color": 3447003,  // Bleu
                        "fields": [
                            {"name": "Nom et Prénom", "value": nom_prenom, "inline": true},
                            {"name": "Rapport", "value": rapport, "inline": false},
                            {"name": "Amendes", "value": amendes || "Aucune", "inline": true},
                            {"name": "Saisies", "value": saisies || "Aucune", "inline": true}
                        ]
                    }
                ]
            };

            // Envoyer à Discord via le webhook
            try {
                const response = await fetch("https://discord.com/api/webhooks/votre_webhook", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(embed)
                });

                if (response.ok) {
                    alert("Rapport envoyé avec succès !");
                    form.reset();
                } else {
                    alert("Erreur lors de l'envoi du rapport. Veuillez réessayer.");
                }
            } catch (error) {
                alert("Erreur lors de l'envoi du rapport. Veuillez vérifier votre connexion.");
            }
        });
    </script>
</body>
</html>

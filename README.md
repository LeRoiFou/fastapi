# Librairie fastapi

Date : 08/06/2025 <br>
---

## 1. Liste des fichiers / répertoires / ...

### indexA : tutos youtube

- indexA001 : présentation et aboutissement de l'utilisation de la librairie fastapi
- indexA002 : [introduction à la librairie FastApi](https://www.youtube.com/watch?v=maCSBgFHoZ4) avec [Documentation de l'API](https://www.youtube.com/watch?v=otkuRlCwtGc&list=PL9DK-47Rpfjjtk7mBH6AyZSHhJYXSXUn7&index=2)
- indexA003 :
  - indexA003_app : [1er cours](https://www.youtube.com/watch?v=7D_0JTeaKWg) sur les bases de la librairie fastapi
  - indexA003_todo : [2ème cours](https://youtu.be/7D_0JTeaKWg?t=2627) sur le recours à l'instruction C.R.U.D.
  - indexA003_test_file et indexA003_test : [3ème cours](https://youtu.be/7D_0JTeaKWg?t=8542) sur le test de notre script
  - répertoire projet_indexA003 : [4ème cours](https://youtu.be/7D_0JTeaKWg?t=9259) sur docker
- indexA004_intro : [Fast API : "Créer facilement une API en Python"](https://youtu.be/0-yncL0bqZs?t=3) + [script sur Github](https://github.com/bandeDeCodeurs/fast_api/blob/main/main.py)

### indexB : divers tests sur la librairie fastapi

- indexB001_essai : afficher "Hello World!" avec une combinaison la librairie python fastapi et un fichier HTML
- indexB002_essai : afficher "Hello World!" après avoir appuyé sur un bouton
- indexB003_essai : zone de saisie avec un bouton affichant le texte saisi dès validation
- indexB004_essai : message d'erreur en cas de saisi autre que des nombres entiers
- indexB005_essai : calcul de l'IMC (application partagée via le dossier fastapi_cloud1)
- indexB006_essai : chargement d'un fichier Excel avec export des traitements opérés sous format Excel
- indexB007_essai : chargement d'un fichier Excel avec récupération de valeurs uniques dans le champ 'civilité' -> sélection du titre affecté à chaque 'civilité' puis affichage des titres affectés à chacune des civilités

---

## 2. [Documentation sur les CORS](https://fastapi.tiangolo.com/tutorial/cors/) : <br>

Toutes routes de notre API peuvent ne pas répondre en cas de partage sur un serveur auprès de différents utilisateurs. <br>
Cette documentation permet de résoudre ce problème, mais également de limiter l'accès de données auprès de tous ou de certains utilisateurs...

---

## 3. La librairie pydantic

La librairie pydantic est similaire à la librairie databases, mais à la différence
de la librairie databases :

- pydantic est similable aux setters de java, cad qu'on peut donner des restrictions
  aussi bien sur le type précis attribué à une instance, que la valeur attribuée à
  cette instance (exemple : l'attribut ne peut pas avoir des valeurs négatives)
- le compilateur traduit tout le programme en une seule fois en code machine,
  tandis que l'interpréteur traduit et exécute le programme ligne par ligne. Python
  est un interpréteur à la différence de java qui est un compilateur. L'avantage
  de Java est que l'erreur est décelée avant même de lancer le programme et permet
  d'être exécuté plus rapidement. Pydantic agit comme un compilateur, cad qu'il
  informe l'erreur d'entrée lors du lancement du programme.
- la librairie databases est directement intégrée à python et donc plus légère,
  alors que pour pydantic, il faut installer la librairie.

Conclusion : pour restreindre des valeurs à attribuer auprès d'un utilisateur, il
est préconisé d'utiliser pydantic (exemple : format du nom du FEC). À défaut, il
est préconisé d'utiliser la librairie databases

Les classes importées de la librairie pydantic :

- BaseModel : permet d'attribuer un type d'attribut figé à une variable
- field_validator : permet de générer selon la valeur attribuée à un paramètre
- SecretStr : permet de masquer la valeur de l'attribut déclaré
- Field : permet d'imposition des conditions à la valeur attribuée
- EmailStr : permet de vérifier que l'adresse email saisie est cohérente

---

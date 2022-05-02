#### Readme
# projet2 - rains-forcast-api

- Cette API (Rains Forcast API) reçoit en entrée un fichier de type .csv contenant les données devant faire l'objet de prediction

- Le fichier pourra être stocker sur AWS s3 par exemple ou Google Cloud Storage et un lien vers ce fichier devra être fourni

- Il est aussi possible d'évaluer les modèles sur de nouvelles données labélisées, il faudra fournir deux fichier comme indiquer au point de terminaison /performance
- ex: https://storage.googleapis.com/datascientest-projet2-storage/db_new_partitition.csv

- docker-compose.yml: Fichier contenant l'orchestration des tests de l'api

- launch_api_test.sh: Fichier permettant de lancer les tests et ecrire les resultats au sein du fichier api_test_results.txt
- api_test_results.txt : resultats du dernier run des tests

- kubernetes_files: Fichier contenant les fichiers Kubernetes de deploiements des pods

- rains-forcast-api-image: Fichier contenant le code (au sein du fichier files/) de l'API et son Dockerfile

- test_authentification_image: Fichier contenant le Dockerfile et le script python du test d'authentification

- test_performance_image: Fichier contenant le Dockerfile et le script python du test de renvoi des performance des modèles

- test_prediction_image: Fichier contenant le Dockerfile et le script python du test de prediction des modèles

#! /bin/bash

mkdir ~/rains_logs/

docker image pull 554477/rains-forcast-api-image:latest
docker image pull 554477/rains_test_authentification_image:latest
docker image pull 554477/rains_test_prediction_image:latest
docker image pull 554477/rains_test_performance_image:latest
docker-compose up --detach
docker-compose down


date=`(date)`
printf "\n\t\t\t$date\n" > ./api_test_results.txt

printf "\n\t\t\tAUTHENTIFICATION TEST\n\n" >> ./api_test_results.txt
cat ~/rains_logs/api_test_authentification.log >> ./api_test_results.txt
printf "\n============================= END ==============================================\n\n\n" >> ./api_test_results.txt

printf "\n\t\t\tPREDICTION TEST\n\n" >> ./api_test_results.txt
cat ~/rains_logs/api_test_model_prediction.log >> ./api_test_results.txt
printf "\n============================= END ==============================================\n\n\n" >> ./api_test_results.txt

printf "\n\t\t\tPERFORMANCE TEST\n\n" >> ./api_test_results.txt
cat ~/rains_logs/api_test_model_performance.log >> ./api_test_results.txt
printf "\n============================= END ==============================================\n\n\n" >> ./api_test_results.txt

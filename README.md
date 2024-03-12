<div align="center">
<h2>Automatic_Speech_Recognition and Elasticsearch Amazon EC2 deployment</h2>
</div>

# About The Project
This project consist of 3 parts
1. Local generation of text from audio file using hugging face facebook/wav2vec2-large-960h model
2. Deployment of Elasticsearch and Frontend UI Locallly or on  Amazon EC2 Instance 
3. Uploading of csv file generated from step 1 to elastric search

## Installation
Prior to running this project on your local machine, please ensure that the following prerequisites are met:

### Prerequisites
1. Internet connection
2. Docker Desktop
3. Python 
4. Running Amazon EC2 Instance (Only for cloud deployment, not required for local deployment)
5. Donloaded dataset from [Kaggle](https://www.kaggle.com/datasets/mozillaorg/common-voice), only need the cv-valid-dev directory which contains 4076 mp3 file and  cv-valid-dev.csv
* You may skip the last prerequisites if you do not wish to generate your own dataset. A generated dataset is provided in the repo

### Starting up (Only required in Local)
1. Start Docker desktop
2. Clone the repository.
3. Using your Terminal, navigate into **Automatic_Speech_Recognition** directory, where docker-compose.yaml file is located. This will be the the **Root** directory for this project
4. You may wish to create a python virtual environment here
5. Run the following command in the Terminal or python virtual environment.
    ```shell
    pip install -r requirements.txt
    ```

## Part 1 (Only required in Local)
* Skip this step if you only want the **output.csv** file mentioned in step 6, which is available as **final.csv** in the **Root**:\asr directory
1. Navigate to **Root**:\asr
2. Run the following command in the Terminal 
   ```shell
    docker build .t asr . # build a docker image and tag it as asr
    docker run --name asr-service --rm -p 8001:8001 asr # start a docker container with the name asr-service using the asr image built earlier, expose port 8001, and auto clean the container once it has stopped
    ```
3. Go to browser and open http://localhost:8001/ping, it should responde you with _"response": "pong"_ once the server is up and running
4. Copy the cv-valid-dev directory and cv-valid-dev.csv  you have downloaded from Kaggle to **Root**:\asr (step 5 of Prerequisites). _**The original cv-valid-dev directory and the cv-valid-dev.csv file will be automatically deleted after program execution**_
5. **Optional** you may edit the following line within cv-decode.py to adjust the number of concurrent jobs
   ```shell
   CONNECTION_SEMAPHORE = asyncio.Semaphore(15) # currently set at 15 concurrent jobs
   ```
   
7. Run the following command in the Terminal or python virtual environment. 
    ```shell
    python cv-decode.py
    ```
8. After completion you will see a newly generated **output.csv** file
9. Stop the running asr-service from step 2 using the following command
   ```shell
   docker stop asr-service
   ```
## Part 2 and Part 3(Local)
### Part 2 local deployment of services
1. Navigate to **Root**:\search-ui and change line 9 to
 ```shell
ENV REACT_APP_DATABASE_API=localhost
```
3. Navigate to **Root**
4. Run the following command in the Terminal and wait for the 3 containers to start up
```shell
docker-compose up
```
5. If go to http://localhost:3000/ and you will see the following error, which is perfectly normally, becasue we have not loaded the correct data yet
   
![image](https://github.com/xiuxiucui/Automatic_Speech_Recognition/assets/41736859/b4c8a5de-821d-4e2b-b6bf-c4af5382295e)
### Part 3 Loading data to local Elasticsearch node
6.  Navigate to **Root**:\elastic-backend and ensure the host is set to http://localhost:9200 on line 9
```shell
Line 9 host="http://localhost:9200"
```
7. Run the following command in the Terminal
```shell
python cv-index.py
```
8. You will see the following lines once it is completed
```shell
____________
completed
```
9. Now you may go to http://localhost:3000/ in a browser and the application will be working fine.





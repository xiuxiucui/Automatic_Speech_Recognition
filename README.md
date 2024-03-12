<div align="center">
<h1>Automatic Speech Recognition and Elasticsearch Amazon EC2 deployment</h1>
</div>

# About The Project
This repository containes the source code for Automatic Speech Recognition, Elasticsearch Backend deployment and an UI that interacts with the Elasticbackend
 You may visit the link to access the demonstration service deployed in Amazon EC2 t2.micro
 * http://ec2-3-27-34-117.ap-southeast-2.compute.amazonaws.com:3000/

![image](https://github.com/xiuxiucui/Automatic_Speech_Recognition/assets/41736859/7b0977eb-ef08-444a-9a77-d3633f8ad20f)

### This project consist of 3 parts
1. Local generation of text from audio file using hugging face facebook/wav2vec2-large-960h model
2. Deployment of Elasticsearch and Frontend UI Locallly or on  Amazon EC2 Instance 
3. Uploading of csv file generated from step 1 to elastric search

## Installation
Prior to running this project on your local machine, please ensure that the following prerequisites are met:

### Prerequisites
1. Internet connection
2. Docker Desktop
3. Python 3.10
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
4. Copy the cv-valid-dev directory and cv-valid-dev.csv  you have downloaded from Kaggle into **Root**:\asr (step 5 of Prerequisites). _**The original cv-valid-dev directory and the cv-valid-dev.csv file will be automatically deleted after program execution**_
5. Navigate to **Root**:\asr
6. **Optional** you may edit the following line within cv-decode.py to adjust the number of concurrent jobs
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
1. Navigate to **Root**:\search-ui open Dockerfile and change line 9 to
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
6.  Navigate to **Root**:\elastic-backend open cv-index.py and ensure the host is set to http://localhost:9200 on line 8
```shell
Line 8 host="http://localhost:9200"
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
9. Now you may go to http://localhost:3000/ in a browser and the application will start up normally

## Part 2 and Part 3(Amazon EC2)
### Part 2 Deployment of services on Amazon EC2
#### Deployment plan
![image](https://github.com/xiuxiucui/Automatic_Speech_Recognition/assets/41736859/b22e5234-4c04-4fd0-9501-7bf40ba5538f)

The following deployment plan works on Amazon Linux 2 Kernel 5.10 t2.micro as of 03/Dec/2024, you may need to change some of the configuration in future


1. Connect to your EC2 instance using SSH
2. Install Docker, Docker Compose, git and Amazon efs utilities tools using the following command
```shell
# install Docker
sudo yum update -y
sudo amazon-linux-extras install docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# install Docker Compose
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# install git
sudo yum install git -y

# Install Amazon efs utilities
sudo yum -y install amazon-efs-utils

```
3. Disconnect the SSH session and reconnect it back again, This step allow us to run docker command without sudo
4. Run following command to set up swap file
   **This step is critical, as the t2.micro instance only provides 1GB of RAM and each Elastic search node require around 2GB of RAM**
The following code gives to creadit to [Ahmad Bilesanmi](https://medium.com/bilesanmiahmad/how-to-install-elasticsearch-on-aws-9d1bb1045daf)
   
```shell
sudo fallocate -l 1500M /swapfile   # allocate extra 1500MB for memory swap
ls -lh /swapfile                    # verify the allocation is indeed 1500MB
sudo chmod 600 /swapfile            # change the permissions for the file
ls -lh /swapfile                    # verify  the permissions change
sudo mkswap /swapfile               # set up swap space
sudo swapon /swapfile               # enable swap space
free -m                             # verify space allocated 
```

The terminal should look like this 
![image](https://github.com/xiuxiucui/Automatic_Speech_Recognition/assets/41736859/871dd3a3-ec69-4fec-b355-5c35c5bc56a4)

5. Create a folder called **application** to store our project using the following code 
```shell
mkdir application
cd application
```
6. Create a folder called **esdata** and map it to Amazon elastic filesystem efs using the following code, the name **esdata** is important, It is defined as a volumne mount in the docker-compose file. Please refer to Appendix for creation of efs volume
```shell
mkdir esdata
sudo mount -t efs -o tls <your file system id> esdata
```
7. Finally we can git clone the repo into our EC2 instance and start the service.
8. Prior clone to the EC2 instance there is 1 changes you need to make
   1. Go to **Root**\search-ui\Dockerfile change the following line
 ```shell
ENV REACT_APP_DATABASE_API=<your own EC2 instance address>  such as ec2-1-11-11-11.ap-southeast-2.compute.amazonaws.com
```
9. Ensure that you are in the **application** folder we have created in step 5, and within the **application** folder there is another folder called **esdata**.
10. git clone the repository and navigate inside using the following command(i am using my own repo as an example)
```shell
git clone git@github.com:xiuxiucui/Automatic_Speech_Recognition.git
cd  Automatic_Speech_Recognition
```
11. Run the following command in the Terminal and wait for the 3 containers to start up
```shell
docker-compose up
```
12. If go to http://<your instance address>:3000/ and you will see the following error, which is perfectly normally, becasue we have not loaded the correct data yet. Or your EC2 security rule is not set up properly, refer to Appendix for EC2 security rule set up
    ![image](https://github.com/xiuxiucui/Automatic_Speech_Recognition/assets/41736859/b4c8a5de-821d-4e2b-b6bf-c4af5382295e)

### Part 3 Loading data to local Elasticsearch node (you should  execute this step locally)
13.  Navigate to **Root**:\elastic-backend open cv-index.py and ensure the host is set to http://\<your_instance_address>:9200 on line 8
```shell
Line 8 host="<your_instance_address>:9200"
```
14. Run the following command in the Terminal
```shell
python cv-index.py
```
15. You will see the following lines once it is completed
```shell
____________
completed
```
16. Now you may go to http://localhost:3000/ in a browser and the application will start up normally




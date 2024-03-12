<div align="center">
<h1>Automatic Speech Recognition and Elasticsearch Amazon EC2 deployment</h1>
</div>

# About The Project
This repository containes the source code for Automatic Speech Recognition, Elasticsearch Backend deployment and an UI which interacts with the Elasticsearch backend
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
   docker build -t asr . # build a docker image and tag it as asr
   docker run --name  asr-api --rm -p 8001:8001 asr # start a docker container with the name  asr-api using the asr image built earlier, expose port 8001, and auto clean the container once it has stopped
    ```
3. Go to browser and open http://localhost:8001/ping, it should responde you with _"response": "pong"_ once the server is up and running
4. Copy the cv-valid-dev directory and cv-valid-dev.csv  you have downloaded from Kaggle into **Root**:\asr (step 5 of Prerequisites). _**The original cv-valid-dev directory and the cv-valid-dev.csv file will be automatically deleted after program execution**_
5. Navigate to **Root**:\asr
6. **Optional** you may edit the following line within cv-decode.py to adjust the number of concurrent jobs
   ```shell
   Line 25 CONNECTION_SEMAPHORE = asyncio.Semaphore(15) # currently set at 15 concurrent jobs
   ```
   
7. Run the following command in the Terminal or python virtual environment. 
    ```shell
    python cv-decode.py
    ```
8. After completion you will see a newly generated **output.csv** file
9. Stop the running asr-service from step 2 using the following command
   ```shell
   docker stop asr-api
   ```
## Part 2 and Part 3(Local deployment)
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
5. Go to http://localhost:3000/ and you will see the following error, which is perfectly normally, becasue we have not loaded the correct data yet
   
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

## Part 2 and Part 3(Amazon EC2 Deployment)
### Part 2 Deployment of services on Amazon EC2
#### Deployment plan
![current drawio (1)](https://github.com/xiuxiucui/Automatic_Speech_Recognition/assets/41736859/12fa4e28-0da0-426a-a3c0-6846734c1e8e)


The following deployment plan works on Amazon Linux 2 Kernel 5.10 t2.micro as of 03/Dec/2024, you may need to change some of the configuration in future


1. Connect to your EC2 instance using SSH
2. Install Docker, Docker Compose and git using the following command
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

6. Finally we can git clone the repo into our EC2 instance and start the service
7. Prior clone to the EC2 instance there is 1 changes you need to make
   1. Go to **Root**\search-ui\Dockerfile change the following line
 ```shell
ENV REACT_APP_DATABASE_API=<your own EC2 instance address>  such as ec2-1-11-11-11.ap-southeast-2.compute.amazonaws.com
```
8. Ensure that you are in the **application** folder we have created in step 5
9. git clone the repository and navigate inside using the following command(i am using my own repo as an example)
```shell
git clone git@github.com:xiuxiucui/Automatic_Speech_Recognition.git
cd  Automatic_Speech_Recognition
```
10. Run the following command in the Terminal and wait for the 3 containers to start up
```shell
docker-compose up
```
11. If go to http://\<your instance address>:3000/ and you will see the following error, which is perfectly normally, becasue we have not loaded the correct data yet. Or your EC2 security rule is not set up properly, refer to Appendix for EC2 security rule set up
    ![image](https://github.com/xiuxiucui/Automatic_Speech_Recognition/assets/41736859/b4c8a5de-821d-4e2b-b6bf-c4af5382295e)

### Part 3 Loading data to local Elasticsearch node (you should  execute this step locally)
12.  Navigate to **Root**:\elastic-backend open cv-index.py and ensure the host is set to http://\<your_instance_address>:9200 on line 8
```shell
Line 8 host="<your_instance_address>:9200"
```
13. Run the following command in the Terminal
```shell
python cv-index.py
```
14. You will see the following lines once it is completed
```shell
____________
completed
```
15. Now you may go to http://\<your_instance_address>:3000/ in a browser and the application will start up normally
## Furture improvement
1. Currently, this document details the use of the HTTP protocol for requests, which lacks robust security. Given that this project is in its prototype phase, this approach remains acceptable. However, transitioning to a production environment necessitates the adoption of the HTTPS protocol, endorsed by Elasticsearch Backend. Attempts to establish an HTTPS connection, involving the integration of a self-signed CA certificate from Elasticsearch, were made but did not succeed.
2. The choice to deploy Elasticsearch on an Amazon EC2 Free Tier t2.micro instance falls short of ideal. The official documentation from Elasticsearch recommends a minimum of 2GB of RAM per node, with swapping disabled to ensure optimal performance. The t2.micro's limited resources compel us to enable swapping, both in the EC2 instance and within the docker-compose.yml, inevitably compromising node performance. For optimal deployment using docker-compose please refer to the [official Docker repo](https://github.com/elastic/elasticsearch/blob/8.12/docs/reference/setup/install/docker/docker-compose.yml), which implements both HTTPS for security and disabled swapping for performance.
3. Presently, our index resides on a single shard, with a replica shard serving as a backup. Enhancing performance could be achieved by distributing our index across multiple shards on the two nodes. Nevertheless, the considerable amount of time dedicated to the HTTPS implementation precluded the completion of the sharding process within the allocated timeframe.
4. At present, ElasticSearch Backend data can only be accessed within Docker, posing significant data security risks. An improved strategy involves mapping data stored in Docker to a directory on the EC2 instance. This approach could be further refined by linking the EC2 directory to an external storage solution, such as Amazon Elastic File System (EFS), as shown in the proposed schematic below. Although efforts to implement this configuration were made, they led to Docker container crashes with exit code 1. I plan to persist in seeking a viable solution.
![current drawio (2)](https://github.com/xiuxiucui/Automatic_Speech_Recognition/assets/41736859/3b0b0493-beec-4ae0-a869-60bfa6d04cc4)

## Appendix
[YouTube Video on how to configure EC2 outbound and inbound network traffic](https://www.youtube.com/watch?v=kxuUMZE9dxU)

## Contact
If you have any inquires or issue with this submission , feel free to approach me using any of the channel below

Cui Xiuqun - [LinkedIn](https://www.linkedin.com/in/xiuqun-cui/) - xiuqun@u.nus.edu


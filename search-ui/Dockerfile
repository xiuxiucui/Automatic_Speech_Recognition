FROM node:16-alpine

WORKDIR '/app'

COPY package.json .
RUN npm install
COPY . .

ENV REACT_APP_DATABASE_API=ec2-3-27-34-117.ap-southeast-2.compute.amazonaws.com

CMD ["npm","run","start"]
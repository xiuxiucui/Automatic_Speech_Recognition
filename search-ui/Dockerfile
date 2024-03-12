FROM node:16-alpine

WORKDIR '/app'

COPY package.json .
RUN npm install
COPY . .

ENV REACT_APP_DATABASE_API=ec2-13-212-254-81.ap-southeast-1.compute.amazonaws.com

CMD ["npm","run","start"]

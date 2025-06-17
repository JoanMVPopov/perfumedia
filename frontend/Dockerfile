FROM node:lts-alpine

#FROM node:14-alpine

RUN npm cache clean --force

# make the 'app' folder the current working directory
WORKDIR /app/frontend

# copy both 'package.json' and 'package-lock.json' (if available)
COPY package*.json ./

COPY vue.config.js ./

# install simple http server for serving static content
RUN npm install -g http-server --verbose

# install project dependencies
RUN npm install && npm update

#----------

# USING VOLUMES RIGHT NOW, CHANGE TO THIS LATER FOR PRODUCTION
# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY . .

# build app for production with minification
#RUN npm run build
#
#EXPOSE 8080
#CMD [ "http-server", "dist" ]

#-----------

EXPOSE 8080
CMD npm run serve
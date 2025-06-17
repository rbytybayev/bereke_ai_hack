# build stage
FROM node:20 AS builder
WORKDIR /app
COPY . .
RUN npm install && npm run build

# production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80

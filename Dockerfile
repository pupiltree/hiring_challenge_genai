# Dockerfile
FROM node:18 as frontend
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend .
RUN npm run build

FROM python:3.9-slim as backend
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend .

FROM nginx:alpine
COPY --from=frontend /app/build /usr/share/nginx/html
COPY --from=backend /app /usr/share/nginx/html/api
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"] 
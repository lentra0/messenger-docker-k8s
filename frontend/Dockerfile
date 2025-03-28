FROM node:16

WORKDIR /app

# Кэшируем зависимости
COPY package*.json ./
RUN npm install

# Копируем остальные файлы
COPY . .

# Проверяем наличие критических файлов
RUN test -f public/index.html && \
    test -f src/index.js && \
    test -f src/index.css || \
    (echo "Missing required files" && exit 1)

# Сборка проекта
RUN npm run build

EXPOSE 3000
CMD ["npm", "start"]

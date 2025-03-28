Вот профессиональный `README.md` для вашего мессенджера с поддержкой Kubernetes:

```markdown
# 🚀 Messenger App with Kubernetes Deployment

![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

Реализация мессенджера с автоматизированным CI/CD пайплайном для развертывания в Kubernetes.

## 📦 Структура проекта

```
messenger/
├── backend/              # Python/FastAPI сервер
│   ├── app/              # Исходный код
│   └── Dockerfile        # Конфигурация образа
├── frontend/             # React клиент
│   ├── src/              # Исходный код
│   └── Dockerfile        
├── k8s/                  # Kubernetes манифесты
│   ├── backend.yaml
│   ├── frontend.yaml
│   └── redis.yaml
└── .github/workflows/    # CI/CD пайплайны
    └── deploy.yml
```

## 🛠️ Требования

- Docker 20.10+
- Kubernetes 1.25+ (или Minikube)
- Python 3.9+ (для backend)
- Node.js 18+ (для frontend)

## 🚀 Быстрый старт

### Локальное развертывание (Minikube)

```bash
# 1. Запуск кластера
minikube start --driver=docker

# 2. Сборка образов
eval $(minikube docker-env)
docker build -t messenger-backend ./backend
docker build -t messenger-frontend ./frontend

# 3. Развертывание
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/backend.yaml
kubectl apply -f k8s/frontend.yaml

# 4. Получение доступа
minikube service frontend-service --url
```

## ☁️ CI/CD Pipeline

Автоматический пайплайн выполняет:
1. Сборку Docker-образов
2. Загрузку в GitHub Container Registry
3. Развертывание в Kubernetes


## 🌐 Доступ к сервисам

После деплоя:
- **Frontend**: `minikube service frontend-service --url`
- **Backend**: `kubectl port-forward service/backend-service 8000:80`

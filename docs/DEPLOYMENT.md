# 🚀 Deployment Guide

Complete guide for deploying Vocalizr in production environments.

## Table of Contents

- [Deployment Overview](#deployment-overview)
- [Docker Deployment](#docker-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Cloud Platforms](#cloud-platforms)
- [Load Balancing](#load-balancing)
- [Monitoring & Logging](#monitoring--logging)
- [Security Considerations](#security-considerations)
- [Performance Optimization](#performance-optimization)
- [Scaling Strategies](#scaling-strategies)

## Deployment Overview

### Architecture Patterns

#### Single Instance Deployment
```
Internet → Load Balancer → Vocalizr Instance
```

#### High Availability Deployment
```
Internet → Load Balancer → [Vocalizr Instance 1]
                        → [Vocalizr Instance 2]
                        → [Vocalizr Instance N]
```

#### Microservices Architecture
```
Internet → API Gateway → [Voice Service]
                      → [Audio Processing Service]
                      → [File Storage Service]
```

### Deployment Checklist

- [ ] Environment configuration validated
- [ ] Resource requirements calculated
- [ ] Security measures implemented
- [ ] Monitoring and logging configured
- [ ] Backup and recovery procedures established
- [ ] Performance testing completed
- [ ] Health checks implemented
- [ ] Auto-scaling configured (if needed)

## Docker Deployment

### Basic Docker Deployment

```bash
# Pull the latest image
docker pull ghcr.io/alphaspheredotai/vocalizr:latest

# Run with basic configuration
docker run -d \
  --name vocalizr \
  -p 7860:7860 \
  -e GRADIO_SERVER_NAME=0.0.0.0 \
  -e DEBUG=false \
  ghcr.io/alphaspheredotai/vocalizr:latest
```

### Production Docker Configuration

```bash
# Create necessary directories
mkdir -p /opt/vocalizr/{cache,results,logs,config}

# Run with production settings
docker run -d \
  --name vocalizr-prod \
  --restart unless-stopped \
  -p 7860:7860 \
  -e GRADIO_SERVER_NAME=0.0.0.0 \
  -e GRADIO_SERVER_PORT=7860 \
  -e DEBUG=false \
  -e HF_HOME=/app/cache \
  -v /opt/vocalizr/cache:/app/cache \
  -v /opt/vocalizr/results:/app/results \
  -v /opt/vocalizr/logs:/app/logs \
  --memory=8g \
  --cpus=4 \
  --health-cmd="curl -f http://localhost:7860/health || exit 1" \
  --health-interval=30s \
  --health-timeout=10s \
  --health-retries=3 \
  ghcr.io/alphaspheredotai/vocalizr:latest
```

### Docker Compose for Production

```yaml
# docker-compose.yml
version: '3.8'

services:
  vocalizr:
    image: ghcr.io/alphaspheredotai/vocalizr:latest
    container_name: vocalizr-app
    restart: unless-stopped
    ports:
      - "7860:7860"
    environment:
      - GRADIO_SERVER_NAME=0.0.0.0
      - GRADIO_SERVER_PORT=7860
      - DEBUG=false
      - HF_HOME=/app/cache
    volumes:
      - vocalizr_cache:/app/cache
      - vocalizr_results:/app/results
      - vocalizr_logs:/app/logs
      - ./config:/app/config:ro
    deploy:
      resources:
        limits:
          memory: 8G
          cpus: '4.0'
        reservations:
          memory: 4G
          cpus: '2.0'
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:7860/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    depends_on:
      - redis
    networks:
      - vocalizr_network

  nginx:
    image: nginx:alpine
    container_name: vocalizr-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - vocalizr
    networks:
      - vocalizr_network

  redis:
    image: redis:alpine
    container_name: vocalizr-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    networks:
      - vocalizr_network

  prometheus:
    image: prom/prometheus
    container_name: vocalizr-prometheus
    restart: unless-stopped
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    networks:
      - vocalizr_network

  grafana:
    image: grafana/grafana
    container_name: vocalizr-grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - vocalizr_network

volumes:
  vocalizr_cache:
  vocalizr_results:
  vocalizr_logs:
  redis_data:
  prometheus_data:
  grafana_data:

networks:
  vocalizr_network:
    driver: bridge
```

### Nginx Configuration

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream vocalizr_backend {
        server vocalizr:7860;
        # Add more servers for load balancing
        # server vocalizr2:7860;
        # server vocalizr3:7860;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=generate:10m rate=1r/s;

    server {
        listen 80;
        server_name your-domain.com;
        
        # Redirect HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        # SSL Configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
        ssl_prefer_server_ciphers off;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";

        # File upload limits
        client_max_body_size 10M;

        # Proxy settings
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Main application
        location / {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://vocalizr_backend;
            proxy_read_timeout 300s;
            proxy_connect_timeout 75s;
        }

        # Audio generation endpoint (stricter rate limiting)
        location /generate {
            limit_req zone=generate burst=5 nodelay;
            proxy_pass http://vocalizr_backend;
            proxy_read_timeout 600s;  # Longer timeout for generation
        }

        # WebSocket support for Gradio
        location /ws {
            proxy_pass http://vocalizr_backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }

        # Health check
        location /health {
            proxy_pass http://vocalizr_backend;
            access_log off;
        }

        # Static files (if any)
        location /static/ {
            alias /var/www/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

## Kubernetes Deployment

### Basic Kubernetes Manifests

#### Namespace
```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: vocalizr
```

#### ConfigMap
```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: vocalizr-config
  namespace: vocalizr
data:
  GRADIO_SERVER_NAME: "0.0.0.0"
  GRADIO_SERVER_PORT: "7860"
  DEBUG: "false"
  HF_HOME: "/app/cache"
```

#### Secret
```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: vocalizr-secrets
  namespace: vocalizr
type: Opaque
data:
  HF_TOKEN: <base64-encoded-token>
```

#### Persistent Volume Claims
```yaml
# pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: vocalizr-cache-pvc
  namespace: vocalizr
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 50Gi
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: vocalizr-results-pvc
  namespace: vocalizr
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Gi
```

#### Deployment
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vocalizr
  namespace: vocalizr
  labels:
    app: vocalizr
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
  selector:
    matchLabels:
      app: vocalizr
  template:
    metadata:
      labels:
        app: vocalizr
    spec:
      containers:
      - name: vocalizr
        image: ghcr.io/alphaspheredotai/vocalizr:latest
        ports:
        - containerPort: 7860
          name: http
        envFrom:
        - configMapRef:
            name: vocalizr-config
        - secretRef:
            name: vocalizr-secrets
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "8Gi"
            cpu: "4"
        volumeMounts:
        - name: cache-volume
          mountPath: /app/cache
        - name: results-volume
          mountPath: /app/results
        livenessProbe:
          httpGet:
            path: /health
            port: 7860
          initialDelaySeconds: 60
          periodSeconds: 30
          timeoutSeconds: 10
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health
            port: 7860
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
      volumes:
      - name: cache-volume
        persistentVolumeClaim:
          claimName: vocalizr-cache-pvc
      - name: results-volume
        persistentVolumeClaim:
          claimName: vocalizr-results-pvc
```

#### Service
```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: vocalizr-service
  namespace: vocalizr
  labels:
    app: vocalizr
spec:
  selector:
    app: vocalizr
  ports:
  - protocol: TCP
    port: 80
    targetPort: 7860
    name: http
  type: ClusterIP
```

#### Ingress
```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: vocalizr-ingress
  namespace: vocalizr
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "10"
    nginx.ingress.kubernetes.io/rate-limit-burst: "20"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "300"
spec:
  tls:
  - hosts:
    - your-domain.com
    secretName: vocalizr-tls
  rules:
  - host: your-domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: vocalizr-service
            port:
              number: 80
```

#### Horizontal Pod Autoscaler
```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vocalizr-hpa
  namespace: vocalizr
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: vocalizr
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Deploy to Kubernetes

```bash
# Apply all manifests
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
kubectl apply -f pvc.yaml
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f ingress.yaml
kubectl apply -f hpa.yaml

# Check deployment status
kubectl get pods -n vocalizr
kubectl get services -n vocalizr
kubectl get ingress -n vocalizr

# View logs
kubectl logs -f deployment/vocalizr -n vocalizr
```

## Cloud Platforms

### AWS Deployment

#### ECS Fargate
```json
{
  "family": "vocalizr-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "2048",
  "memory": "8192",
  "executionRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "vocalizr",
      "image": "ghcr.io/alphaspheredotai/vocalizr:latest",
      "portMappings": [
        {
          "containerPort": 7860,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "GRADIO_SERVER_NAME",
          "value": "0.0.0.0"
        },
        {
          "name": "DEBUG",
          "value": "false"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/vocalizr",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:7860/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

#### CloudFormation Template
```yaml
# cloudformation.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Vocalizr deployment on AWS'

Parameters:
  VpcId:
    Type: AWS::EC2::VPC::Id
    Description: VPC ID for deployment
  
  SubnetIds:
    Type: List<AWS::EC2::Subnet::Id>
    Description: Subnet IDs for deployment

  DomainName:
    Type: String
    Description: Domain name for the application

Resources:
  # Application Load Balancer
  LoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Type: application
      Scheme: internet-facing
      Subnets: !Ref SubnetIds
      SecurityGroups:
        - !Ref LoadBalancerSecurityGroup

  # ECS Cluster
  ECSCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: vocalizr-cluster
      CapacityProviders:
        - FARGATE
        - FARGATE_SPOT

  # ECS Service
  ECSService:
    Type: AWS::ECS::Service
    Properties:
      Cluster: !Ref ECSCluster
      TaskDefinition: !Ref TaskDefinition
      DesiredCount: 3
      LaunchType: FARGATE
      NetworkConfiguration:
        AwsvpcConfiguration:
          SecurityGroups:
            - !Ref AppSecurityGroup
          Subnets: !Ref SubnetIds
          AssignPublicIp: ENABLED
      LoadBalancers:
        - ContainerName: vocalizr
          ContainerPort: 7860
          TargetGroupArn: !Ref TargetGroup

  # Auto Scaling
  AutoScalingTarget:
    Type: AWS::ApplicationAutoScaling::ScalableTarget
    Properties:
      ServiceNamespace: ecs
      ResourceId: !Sub service/${ECSCluster}/${ECSService.Name}
      ScalableDimension: ecs:service:DesiredCount
      MinCapacity: 2
      MaxCapacity: 10

  AutoScalingPolicy:
    Type: AWS::ApplicationAutoScaling::ScalingPolicy
    Properties:
      PolicyName: vocalizr-scaling-policy
      PolicyType: TargetTrackingScaling
      ScalingTargetId: !Ref AutoScalingTarget
      TargetTrackingScalingPolicyConfiguration:
        TargetValue: 70.0
        PredefinedMetricSpecification:
          PredefinedMetricType: ECSServiceAverageCPUUtilization
```

### Google Cloud Platform

#### Cloud Run Deployment
```yaml
# cloud-run.yaml
apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: vocalizr
  annotations:
    run.googleapis.com/ingress: all
spec:
  template:
    metadata:
      annotations:
        autoscaling.knative.dev/minScale: "1"
        autoscaling.knative.dev/maxScale: "10"
        run.googleapis.com/cpu-throttling: "false"
        run.googleapis.com/memory: "8Gi"
        run.googleapis.com/cpu: "4"
    spec:
      containers:
      - image: ghcr.io/alphaspheredotai/vocalizr:latest
        ports:
        - containerPort: 7860
        env:
        - name: GRADIO_SERVER_NAME
          value: "0.0.0.0"
        - name: GRADIO_SERVER_PORT
          value: "7860"
        - name: DEBUG
          value: "false"
        resources:
          limits:
            memory: "8Gi"
            cpu: "4"
        livenessProbe:
          httpGet:
            path: /health
            port: 7860
          initialDelaySeconds: 60
          periodSeconds: 30
```

Deploy to Cloud Run:
```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/vocalizr

# Deploy to Cloud Run
gcloud run deploy vocalizr \
  --image gcr.io/PROJECT_ID/vocalizr \
  --platform managed \
  --region us-central1 \
  --memory 8Gi \
  --cpu 4 \
  --min-instances 1 \
  --max-instances 10 \
  --port 7860 \
  --allow-unauthenticated \
  --set-env-vars GRADIO_SERVER_NAME=0.0.0.0,DEBUG=false
```

### Azure Container Instances

```yaml
# azure-container.yaml
apiVersion: 2021-07-01
location: eastus
name: vocalizr-container-group
properties:
  containers:
  - name: vocalizr
    properties:
      image: ghcr.io/alphaspheredotai/vocalizr:latest
      ports:
      - port: 7860
        protocol: TCP
      environmentVariables:
      - name: GRADIO_SERVER_NAME
        value: "0.0.0.0"
      - name: DEBUG
        value: "false"
      resources:
        requests:
          cpu: 4
          memoryInGB: 8
  osType: Linux
  restartPolicy: Always
  ipAddress:
    type: Public
    ports:
    - port: 7860
      protocol: TCP
```

## Load Balancing

### HAProxy Configuration

```haproxy
# haproxy.cfg
global
    daemon
    maxconn 4096

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms
    option httplog

frontend vocalizr_frontend
    bind *:80
    bind *:443 ssl crt /etc/ssl/certs/vocalizr.pem
    redirect scheme https if !{ ssl_fc }
    
    # Rate limiting
    stick-table type ip size 100k expire 30s store http_req_rate(10s)
    http-request track-sc0 src
    http-request reject if { sc_http_req_rate(0) gt 10 }
    
    default_backend vocalizr_backend

backend vocalizr_backend
    balance roundrobin
    option httpchk GET /health
    
    server vocalizr1 vocalizr1:7860 check
    server vocalizr2 vocalizr2:7860 check
    server vocalizr3 vocalizr3:7860 check
```

### Nginx Load Balancer

```nginx
# nginx-lb.conf
upstream vocalizr_pool {
    least_conn;
    server vocalizr1:7860 max_fails=3 fail_timeout=30s;
    server vocalizr2:7860 max_fails=3 fail_timeout=30s;
    server vocalizr3:7860 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    
    # Health check endpoint
    location /health {
        proxy_pass http://vocalizr_pool;
        proxy_set_header Host $host;
        access_log off;
    }
    
    # Main application
    location / {
        proxy_pass http://vocalizr_pool;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # Session affinity (sticky sessions)
        ip_hash;
    }
}
```

## Monitoring & Logging

### Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'vocalizr'
    static_configs:
      - targets: ['vocalizr:7860']
    metrics_path: /metrics
    scrape_interval: 30s

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']

rule_files:
  - "vocalizr_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Vocalizr Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "Requests/sec"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      },
      {
        "title": "Memory Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "process_resident_memory_bytes",
            "legendFormat": "Memory Usage"
          }
        ]
      }
    ]
  }
}
```

### Logging Stack (ELK)

#### Elasticsearch Configuration
```yaml
# elasticsearch.yml
cluster.name: vocalizr-logs
node.name: node-1
path.data: /usr/share/elasticsearch/data
network.host: 0.0.0.0
discovery.type: single-node
```

#### Logstash Configuration
```ruby
# logstash.conf
input {
  beats {
    port => 5044
  }
}

filter {
  if [fields][service] == "vocalizr" {
    grok {
      match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} \| %{WORD:level} \| %{GREEDYDATA:msg}" }
    }
    
    date {
      match => [ "timestamp", "yyyy-MM-dd HH:mm:ss" ]
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "vocalizr-logs-%{+YYYY.MM.dd}"
  }
}
```

#### Filebeat Configuration
```yaml
# filebeat.yml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /app/logs/*.log
  fields:
    service: vocalizr
  fields_under_root: true

output.logstash:
  hosts: ["logstash:5044"]
```

## Security Considerations

### SSL/TLS Configuration

#### Let's Encrypt with Certbot
```bash
# Install certbot
apt-get update && apt-get install -y certbot python3-certbot-nginx

# Generate certificate
certbot --nginx -d your-domain.com

# Auto-renewal
echo "0 12 * * * /usr/bin/certbot renew --quiet" | crontab -
```

#### Custom SSL Certificate
```nginx
# SSL configuration
ssl_certificate /etc/ssl/certs/vocalizr.crt;
ssl_certificate_key /etc/ssl/private/vocalizr.key;
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
ssl_prefer_server_ciphers off;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
```

### Network Security

#### Firewall Rules (iptables)
```bash
# Allow SSH, HTTP, HTTPS
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Allow application port (internal only)
iptables -A INPUT -p tcp --dport 7860 -s 10.0.0.0/8 -j ACCEPT

# Drop everything else
iptables -A INPUT -j DROP
```

#### AWS Security Groups
```yaml
SecurityGroup:
  Type: AWS::EC2::SecurityGroup
  Properties:
    GroupDescription: Vocalizr Security Group
    VpcId: !Ref VpcId
    SecurityGroupIngress:
      - IpProtocol: tcp
        FromPort: 80
        ToPort: 80
        CidrIp: 0.0.0.0/0
      - IpProtocol: tcp
        FromPort: 443
        ToPort: 443
        CidrIp: 0.0.0.0/0
      - IpProtocol: tcp
        FromPort: 7860
        ToPort: 7860
        SourceSecurityGroupId: !Ref LoadBalancerSecurityGroup
```

### Authentication & Authorization

#### OAuth2 Integration
```python
# oauth_config.py
from authlib.integrations.flask_client import OAuth

oauth = OAuth(app)

oauth.register(
    name='google',
    client_id='your-client-id',
    client_secret='your-client-secret',
    server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

@app.route('/login')
def login():
    redirect_uri = url_for('callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/callback')
def callback():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    # Store user session
    return redirect('/')
```

## Performance Optimization

### Caching Strategies

#### Redis Caching
```python
import redis
import pickle

class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.Redis(host=host, port=port, db=db)
    
    def get_audio(self, text_hash):
        cached = self.redis_client.get(f"audio:{text_hash}")
        if cached:
            return pickle.loads(cached)
        return None
    
    def set_audio(self, text_hash, audio_data, ttl=3600):
        self.redis_client.setex(
            f"audio:{text_hash}",
            ttl,
            pickle.dumps(audio_data)
        )
```

#### CDN Configuration (CloudFlare)
```javascript
// CloudFlare Worker
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const cache = caches.default
  const cacheKey = new Request(request.url, request)
  
  // Check cache first
  let response = await cache.match(cacheKey)
  
  if (!response) {
    // Forward to origin
    response = await fetch(request)
    
    // Cache audio files
    if (request.url.includes('/generate') && response.status === 200) {
      response = new Response(response.body, response)
      response.headers.set('Cache-Control', 'max-age=3600')
      event.waitUntil(cache.put(cacheKey, response.clone()))
    }
  }
  
  return response
}
```

### Database Optimization

#### PostgreSQL for Metadata
```sql
-- Create tables for audio metadata
CREATE TABLE generated_audio (
    id SERIAL PRIMARY KEY,
    text_hash VARCHAR(32) UNIQUE NOT NULL,
    text_content TEXT NOT NULL,
    voice VARCHAR(50) NOT NULL,
    speed FLOAT NOT NULL,
    file_path VARCHAR(255),
    duration FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_text_hash ON generated_audio(text_hash);
CREATE INDEX idx_created_at ON generated_audio(created_at);
CREATE INDEX idx_voice ON generated_audio(voice);

-- Cleanup old records
DELETE FROM generated_audio 
WHERE accessed_at < NOW() - INTERVAL '7 days';
```

## Scaling Strategies

### Horizontal Scaling

#### Auto-scaling Configuration
```yaml
# kubernetes-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vocalizr-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: vocalizr
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
```

### Vertical Scaling

#### Resource Optimization
```yaml
# Optimized resource allocation
resources:
  requests:
    memory: "4Gi"
    cpu: "2"
    nvidia.com/gpu: 1
  limits:
    memory: "16Gi"
    cpu: "8"
    nvidia.com/gpu: 1
```

### Geographic Distribution

#### Multi-Region Deployment
```yaml
# Region-specific deployments
regions:
  us-west-2:
    replicas: 5
    resources:
      cpu: "4"
      memory: "8Gi"
  
  eu-west-1:
    replicas: 3
    resources:
      cpu: "4"
      memory: "8Gi"
  
  ap-southeast-1:
    replicas: 2
    resources:
      cpu: "4"
      memory: "8Gi"
```

### Health Checks and Readiness

```python
# health_check.py
from flask import Flask, jsonify
import psutil
import torch

app = Flask(__name__)

@app.route('/health')
def health_check():
    """Basic health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "vocalizr",
        "timestamp": time.time()
    })

@app.route('/readiness')
def readiness_check():
    """Detailed readiness check."""
    try:
        # Check memory usage
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        
        # Check GPU if available
        gpu_available = torch.cuda.is_available()
        gpu_memory = None
        if gpu_available:
            gpu_memory = torch.cuda.memory_allocated() / torch.cuda.max_memory_allocated() * 100
        
        # Check model loading
        model_loaded = True  # Check if PIPELINE is loaded
        
        status = "ready" if all([
            memory_usage < 90,
            model_loaded,
            gpu_memory is None or gpu_memory < 90
        ]) else "not_ready"
        
        return jsonify({
            "status": status,
            "checks": {
                "memory_usage": f"{memory_usage:.1f}%",
                "gpu_available": gpu_available,
                "gpu_memory": f"{gpu_memory:.1f}%" if gpu_memory else "N/A",
                "model_loaded": model_loaded
            }
        })
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500
```

This deployment guide provides comprehensive coverage for deploying Vocalizr in production environments, from simple Docker deployments to complex Kubernetes clusters with auto-scaling, monitoring, and security features.

## Next Steps

- Review [Configuration Guide](CONFIGURATION.md) for environment-specific settings
- Check [Troubleshooting Guide](TROUBLESHOOTING.md) for deployment issues
- See [Monitoring Guide] for operational best practices
- Explore [Security Guide] for hardening your deployment
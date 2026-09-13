# OpsFlow

SaaS multi-tenant para desenhar, executar e auditar processos internos.

**Demo:** https://opsflow-ebon.vercel.app

**API:** https://opsflow-api-x066.onrender.com/docs

> A API usa o plano gratuito do Render e pode levar até um minuto para responder ao primeiro acesso após um período de inatividade.

![Next.js](https://img.shields.io/badge/Next.js-15-111827) ![FastAPI](https://img.shields.io/badge/FastAPI-Python-059669) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-2563eb) ![Docker](https://img.shields.io/badge/Docker-Compose-0284c7)

## MVP implementado

- cadastro, login JWT e RBAC (`admin`, `manager`, `member`);
- workflows, etapas com SLA, execuções e aprovações sequenciais;
- bloqueio de autoaprovação e isolamento por organização;
- auditoria, indicadores operacionais e worker para tarefas atrasadas;
- Next.js, FastAPI, PostgreSQL, Redis/Celery, Docker Compose, testes e CI.

## Executar

1. Copie `.env.example` para `.env`.
2. Rode `docker compose up --build`.
3. Abra http://localhost:3000. Swagger: http://localhost:8000/docs.

## Demonstração ponta a ponta

1. Crie a empresa e o usuário administrador.
2. Em **Equipe**, crie um usuário `manager` e um `member`.
3. Em **Workflows**, crie um fluxo ativo e adicione etapas para esses perfis.
4. Em **Execuções**, inicie um onboarding.
5. Entre com o usuário responsável e aprove sua tarefa.
6. Acompanhe o avanço em **Execuções** e os eventos em **Auditoria**.

Sem Docker: o backend usa SQLite por padrão. Rode `pip install -e ".[dev]"` e `pytest` em `backend`.

## API principal

`POST /auth/register`, `POST /auth/login`, `GET/POST/PUT /workflows`, `POST /workflows/{id}/steps`, `GET/POST /executions`, `GET /tasks`, `POST /tasks/{id}/approve`, `POST /tasks/{id}/reject`, `GET /audit-logs` e `GET /analytics/overview` (todos sob `/api/v1`).

## Decisões de engenharia

- isolamento de tenants aplicado em todas as consultas de negócio;
- solicitantes não podem aprovar a própria solicitação;
- tarefas avançam sequencialmente e respeitam o perfil responsável;
- mudanças relevantes deixam trilha de auditoria;
- SLA vencido é processado de forma assíncrona pelo Celery;
- CI executa lint, testes e build a cada push ou pull request.

## Roadmap

OAuth Microsoft/Google, webhooks, notificações, templates de processo, anexos em S3 e camada analítica Bronze/Silver/Gold.

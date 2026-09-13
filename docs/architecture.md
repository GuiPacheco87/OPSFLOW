# Arquitetura

O OpsFlow utiliza um monólito modular: simples para operar no MVP, mas com limites claros entre apresentação, regras de negócio e persistência.

```text
Next.js / TypeScript
        │ HTTPS + JSON
        ▼
FastAPI / Pydantic
        │
        ├── autenticação e RBAC
        ├── workflows e execuções
        ├── tarefas e aprovações
        ├── auditoria e analytics
        ▼
Services → SQLAlchemy → PostgreSQL
        │
        └── Celery → Redis (ambiente Docker completo)
```

## Ambientes

| Componente | Desenvolvimento | Demonstração pública |
|---|---|---|
| Frontend | Next.js em Docker | Vercel |
| API | FastAPI em Docker | Render Free |
| Banco | PostgreSQL 16 | Neon PostgreSQL |
| Filas | Redis + Celery | Regra síncrona sob demanda |

No plano gratuito público, tarefas vencidas são atualizadas quando endpoints operacionais são consultados. No ambiente completo, o Celery executa essa rotina em segundo plano.

## Fluxo de uma execução

1. O usuário inicia um workflow ativo.
2. A API cria a execução e a tarefa da primeira etapa.
3. Um usuário com o perfil responsável aprova ou rejeita a tarefa.
4. Uma aprovação cria a próxima tarefa; uma rejeição encerra a execução.
5. A última aprovação conclui o processo.
6. Cada mutação relevante é registrada no audit log.

O tenant vem exclusivamente do JWT autenticado, nunca de um identificador de organização confiado ao cliente.


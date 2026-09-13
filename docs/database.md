# Modelo de dados

```text
Organization 1 ── N User
Organization 1 ── N Workflow 1 ── N WorkflowStep
Workflow     1 ── N WorkflowExecution 1 ── N Task
Task         1 ── N Approval
Organization 1 ── N AuditLog
```

## Entidades

- **Organization:** tenant proprietário dos dados.
- **User:** identidade, credencial, perfil e estado de ativação.
- **Workflow:** definição versionável de um processo.
- **WorkflowStep:** unidade ordenada de trabalho ou aprovação.
- **WorkflowExecution:** instância de um workflow com os dados da solicitação.
- **Task:** trabalho gerado para uma etapa, com responsável e vencimento.
- **Approval:** decisão, comentário, autor e momento.
- **AuditLog:** registro imutável das mutações relevantes.

Identificadores usam UUID. Datas são armazenadas com timezone. Restrições únicas impedem e-mails duplicados dentro de uma organização e ordens repetidas no mesmo workflow.


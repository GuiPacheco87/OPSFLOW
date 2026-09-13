# API e regras de negócio

Swagger: https://opsflow-api-x066.onrender.com/docs

Todos os endpoints de negócio utilizam o prefixo `/api/v1` e exigem `Authorization: Bearer <token>`.

| Método | Rota | Finalidade |
|---|---|---|
| POST | `/auth/register` | Criar organização e administrador |
| POST | `/auth/login` | Obter JWT |
| GET | `/me` | Consultar usuário autenticado |
| GET/POST | `/users` | Listar ou criar usuários |
| GET/POST | `/workflows` | Listar ou criar workflows |
| GET/PUT | `/workflows/{id}` | Consultar ou atualizar workflow |
| POST | `/workflows/{id}/steps` | Adicionar etapa |
| GET/POST | `/executions` | Listar ou iniciar execuções |
| GET | `/tasks` | Consultar tarefas disponíveis |
| POST | `/tasks/{id}/approve` | Aprovar e avançar o processo |
| POST | `/tasks/{id}/reject` | Rejeitar e encerrar o processo |
| GET | `/audit-logs` | Consultar trilha de auditoria |
| GET | `/analytics/overview` | Obter indicadores operacionais |

## Regras implementadas

- somente workflows ativos podem ser executados;
- workflows sem etapas não podem ser iniciados;
- uma tarefa já decidida não pode receber nova decisão;
- o solicitante não pode aprovar a própria solicitação;
- apenas o perfil atribuído ou um administrador pode decidir uma tarefa;
- dados de outra organização retornam como inexistentes;
- aprovação da última etapa conclui a execução;
- reprovação encerra imediatamente a execução.


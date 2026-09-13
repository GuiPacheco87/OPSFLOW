# Arquitetura

Monólito modular: `Next.js → FastAPI → Services → SQLAlchemy → PostgreSQL`, com tarefas assíncronas via `Celery → Redis`.

O tenant vem do JWT autenticado, não de parâmetros enviados pelo cliente. Uma execução cria sua primeira tarefa; a aprovação cria a próxima, e a última encerra a execução. A reprovação encerra o fluxo. Toda mutação relevante gera um registro de auditoria.


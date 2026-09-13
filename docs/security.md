# Segurança e multi-tenancy

## Controles implementados

- senhas processadas com Argon2 e nunca retornadas pela API;
- JWT assinado, com expiração e identificação do tenant;
- RBAC para Admin, Manager e Member;
- validação de entrada com Pydantic;
- CORS restrito aos frontends configurados;
- segredos fornecidos por variáveis de ambiente;
- consultas filtradas pela organização autenticada;
- trilha de auditoria para mutações relevantes;
- bloqueio de autoaprovação.

## Modelo de isolamento

Todas as entidades operacionais possuem `organization_id`. A API extrai a organização do token validado e aplica o filtro no servidor. O cliente não escolhe o tenant de uma consulta.

## Produção corporativa

Antes de uso comercial, o roadmap de segurança inclui rotação e revogação de tokens, refresh tokens, MFA/OAuth, rate limiting distribuído, gestão formal de migrações, criptografia de campos sensíveis, backup e restore testado, observabilidade, política de retenção e testes automatizados de autorização entre tenants.


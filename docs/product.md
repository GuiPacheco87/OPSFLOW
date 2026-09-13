# Especificação do produto

## Problema

Processos internos frequentemente dependem de e-mails, planilhas e conhecimento informal. Isso dificulta saber quem deve agir, qual é o prazo, onde está o gargalo e por que uma decisão foi tomada.

## Proposta

O OpsFlow oferece um workspace por empresa no qual administradores desenham processos reutilizáveis e colaboradores iniciam, acompanham e aprovam solicitações com rastreabilidade completa.

## Personas

- **Administrador:** configura a organização, usuários, perfis e workflows; consulta toda a auditoria.
- **Gestor:** cria processos, configura etapas, acompanha execuções e aprova tarefas de gestão.
- **Colaborador:** inicia solicitações e executa tarefas atribuídas ao seu perfil.
- **Auditor ou liderança:** acompanha histórico, SLAs, volume, resultados e gargalos.

## Casos de uso

- onboarding e offboarding de colaboradores;
- solicitação e revogação de acessos;
- aquisição e entrega de equipamentos;
- férias, reembolsos e aprovações financeiras;
- chamados internos e solicitações entre departamentos;
- processos de compliance e revisões periódicas.

## Funcionalidades disponíveis

| Área | Capacidades |
|---|---|
| Identidade | Cadastro de empresa, login JWT e usuários por organização |
| Permissões | Perfis Admin, Manager e Member |
| Workflows | Nome, descrição, status e etapas ordenadas |
| Etapas | Perfil responsável, ação, obrigatoriedade e SLA em horas |
| Execuções | Dados da solicitação, andamento e conclusão |
| Tarefas | Responsável sugerido, prazo, aprovação e reprovação |
| Governança | Bloqueio de autoaprovação e audit log |
| Operação | Processos abertos, concluídos, atrasados e rejeitados |

## Exemplo: onboarding

```text
RH inicia solicitação
        ↓
Gestor aprova contratação
        ↓
TI prepara equipamento e acessos
        ↓
RH confirma conclusão
```

Os dados podem incluir nome, e-mail, cargo, departamento, gestor, data de início, modelo de trabalho, equipamento e sistemas necessários.

## Diferenciais técnicos

- isolamento multi-tenant desde o primeiro modelo;
- regras de aprovação concentradas na camada de serviço;
- API documentada automaticamente com OpenAPI;
- mesma base preparada para automações e uma futura plataforma de dados;
- execução local completa com um único comando Docker Compose.


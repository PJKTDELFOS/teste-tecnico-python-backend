Metodologia de Desenvolvimento — Performance Log API
Sobre este documento
Este documento descreve a abordagem utilizada no desenvolvimento deste projeto,
com transparência sobre o papel da IA no processo.

O Processo
Este projeto foi desenvolvido com auxílio da IA Claude (Anthropic) como
ferramenta de suporte técnico — não como substituto do desenvolvedor.
Todas as decisões de arquitetura, modelagem de dados, regras de negócio e
escolhas tecnológicas foram tomadas pelo desenvolvedor. A IA atuou como
um auxiliar técnico — um par de programação disponível para tirar dúvidas,
apontar erros e sugerir correções pontuais.

O que o desenvolvedor fez

Analisou o enunciado e definiu o escopo do sistema
Projetou a arquitetura em camadas: models, schemas, routers, services, core
Modelou as entidades e suas relações: User, Session, Task, Comentario
Definiu as regras de negócio:

Uma session ativa por usuário
Fechamento automático de session anterior ao abrir nova
Tasks fechadas com nivel_foco default 3 em caso de fechamento abrupto
Diagnóstico calculado sobre todas as sessions do usuário


Tomou decisões técnicas conscientes:

UUID para tasks (evitar enumeração)
PostgreSQL para suporte a múltiplos usuários simultâneos
JWT para autenticação sem estado
Separação clara entre modelo de banco e schema de validação


Identificou e corrigiu inconsistências nas sugestões da IA
Refatorou a estrutura de arquivos conforme sua visão de organização


O que a IA auxiliou

Explicar diferenças entre Django e FastAPI durante a curva de aprendizado
Apontar erros de sintaxe e typos durante as revisões de código
Sugerir correções pontuais quando solicitado
Identificar incompatibilidade de versão do bcrypt que causava erro 500
Auxiliar na configuração do Alembic e variáveis de ambiente


Decisões onde o desenvolvedor discordou da IA
Durante o desenvolvimento, o desenvolvedor questionou e corrigiu sugestões
da IA em diversos momentos:

db_manager.py: A IA assumiu erroneamente que o arquivo se chamava
database.py. O desenvolvedor manteve seu próprio nome de arquivo.
Campo nota: A IA sugeriu nullable=False. O desenvolvedor identificou
que a nota pode ser atribuída em momentos diferentes e manteve nullable=True.
Email encriptado: A IA sugeriu adicionar camada de encriptação. O
desenvolvedor avaliou a complexidade e optou conscientemente por não adicionar
nesse momento, priorizando a entrega.
Nomes de arquivos: O desenvolvedor reorganizou os nomes dos arquivos
(tasks_models.py, tasks_schemas.py) conforme sua própria convenção.


Conclusão
O uso de IA como ferramenta de desenvolvimento acelera o processo mas não
substitui o raciocínio do desenvolvedor. Neste projeto, cada linha de código
foi revisada, questionada e aprovada pelo desenvolvedor antes de ser incluída.
A capacidade de identificar erros nas sugestões da IA, questionar decisões
arquiteturais e manter controle sobre o projeto é o que diferencia um
desenvolvedor que usa IA de um que é usado por ela.

Desenvolvido por Albert — processo seletivo SouJunior
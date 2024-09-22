# Sistema de Gerenciamento de Acessos e Logs
Este projeto é um sistema de gerenciamento de acessos e logs, desenvolvido em uma arquitetura distribuída. É um projeto feito para fins academicos, grande parte de sua estrutura foi disponibilizada pelo Prof. Fernando Posser, sendo realizado apenas alguma adaptações e adições para realizar a integração com o sistema de leitura de tags RFID.

## Funcionalidades
1. Página Web para Visualização em Tempo Real
Uma interface web que permite visualizar as atividades em tempo real. A página é atualizada dinamicamente com informações sobre acessos e tentativas de acesso.

2. Sistema de Leitura de Tags
Um sistema físico que lê as tags RFID dos colaboradores e, ao ser inicializado, busca informações do sistema de gerenciamento de acessos. Os dados são armazenados temporariamente na memória para garantir a continuidade das operações, mesmo em caso de perda de conexão.

3. Análise de Dados com Pandas
Utiliza a biblioteca Pandas para analisar os dados gerados nos logs de acesso. As análises incluem:
- Contagem de entradas e saída.
- Cálculo do tempo total que um colaborador específico permaneceu na sala.
- Contagem de Tentativas de invasão e de entradas não autorizadas

## Tecnologias Utilizadas
- Flask: Para o backend e gerenciamento de rotas.
- SQLite: Banco de dados para armazenar informações de colaboradores e logs.
- JavaScript: Para interações na página web.
- Pandas: Para análise de dados.
- HTML/CSS: Para construção da interface do usuário.
## Estrutura do Projeto
O projeto está estruturado em múltiplos módulos que se comunicam entre si, permitindo uma arquitetura escalável e modular. Cada parte do sistema é responsável por uma funcionalidade específica, o que facilita a manutenção e futuras expansões.

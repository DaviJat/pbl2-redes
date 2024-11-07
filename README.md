# Implementação de Sistema para Venda de Trechos Distribuídos entre Companhias Aéreas

** Davi Jatobá Galdino, Gabriel Sena Barbosa **

Universidade Estadual de Feira de Santana (UEFS)
Av. Transnordestina, s/n, Novo Horizonte - BA, 44036-900

ddavijatoba33@gmail.com, gabriel.sena.barbosa@gmail.com

## 1. Introdução

O setor de aviação de baixo custo (LCCs) tem experimentado uma demanda crescente por sistemas de reservas que ofereçam uma experiência integrada e possibilitem o compartilhamento de trechos entre diferentes companhias. No entanto, a estrutura atual, onde cada companhia aérea opera um servidor centralizado próprio para vendas, dificulta a reserva de passagens que envolvam mais de uma empresa, tornando o processo fragmentado e menos acessível para o cliente.

Para resolver esse problema, este projeto propõe uma solução descentralizada que permite a comunicação entre os servidores das companhias aéreas conveniadas, facilitando reservas de múltiplos trechos em diferentes empresas. A solução foi desenvolvida utilizando uma API REST, implementada em Python com o framework Flask, e integra três servidores que se comunicam entre si. Esse sistema de comunicação descentralizado adota o algoritmo de Lamport para resolver conflitos de reserva, assegurando que o cliente que realiza a compra primeiro tenha prioridade sobre os trechos reservados. Com o uso de contêineres Docker, a implementação garante escalabilidade, isolamento e uma execução confiável e segura.

Este relatório aborda o desenvolvimento do sistema, destacando as decisões de projeto, as funcionalidades implementadas e os testes realizados para validar a solução. A proposta é fornecer uma experiência de compra eficiente e simplificada aos clientes, permitindo-lhes reservar trechos de diferentes companhias de forma integrada e segura.

## 2. Metodologia Utilizada

### 2.1 Arquitetura RESTful
O sistema foi implementado com uma arquitetura RESTful, conforme exigido no enunciado do problema, para garantir a comunicação entre os servidores das companhias aéreas de forma interoperável e segura. O uso do padrão REST é adequado para sistemas distribuídos como este devido à sua capacidade de facilitar transmissões de dados stateless (sem estado), o que permite que cada requisição seja autossuficiente e contenha todas as informações necessárias para ser processada, reduzindo a necessidade de manutenções complexas de sessão.
Consulta de Trechos: Cada servidor expõe um endpoint para consultar os trechos de viagens disponíveis. Esse endpoint é configurado para aceitar parâmetros de origem e destino, retornando uma lista dos trechos possíveis entre essas localidades. Para ampliar as possibilidades de conexão entre as rotas, o sistema também consulta trechos em servidores conveniados.
Compra de Passagem: O endpoint de compra permite que o cliente selecione e reserve um trecho disponível, desde que ele ainda possua passagens. Caso a compra seja realizada com sucesso, o servidor bloqueia temporariamente a rota para garantir a exclusão mútua.
Atualização de Estado: Sempre que uma compra é realizada, o sistema atualiza o estado dos trechos no servidor que gerencia aquele trecho específico. Isso assegura que outros clientes não possam reservar o mesmo trecho até que ele esteja liberado novamente.

### 2.2 Controle de Concorrência com o Algoritmo de Lamport
A sincronização de transações entre os servidores foi garantida por meio do Algoritmo de Lamport, um método amplamente utilizado para ordenação de eventos em sistemas distribuídos. Esse algoritmo é fundamental para garantir que, mesmo em um ambiente descentralizado, a ordem de chegada das requisições seja respeitada. Ao adotar o Algoritmo de Lamport, cada servidor mantém controle local das requisições de forma eficiente, o que evita a necessidade de um coordenador central ou de uma comunicação excessivamente complexa entre os servidores.
As principais etapas do controle de concorrência implementado são:
Relógio Lógico (Timestamp): Cada servidor possui um relógio lógico que incrementa a cada nova requisição. Esse timestamp é usado para registrar a ordem de chegada das requisições, garantindo que a prioridade para acessar um recurso específico seja sempre dada à requisição com o menor timestamp.
Fila de Requisições: Cada servidor enfileira suas requisições de compra em uma fila que respeita a ordem dos timestamps. A fila é verificada constantemente, de modo que a próxima requisição a ser atendida é sempre a de menor timestamp, assegurando a sequência correta das operações.
Exclusão Mútua: Durante o processamento de uma compra, o trecho específico é bloqueado temporariamente, impedindo que outras requisições modifiquem seu estado até a conclusão da operação. Esse mecanismo evita condições de corrida e assegura que o cliente que iniciou a compra primeiro mantenha a preferência sobre o recurso.
Optou-se pelo Algoritmo de Lamport em vez de outros métodos de exclusão mútua, como o Token Ring, por algumas razões específicas para este sistema distribuído. No Token Ring, a comunicação entre servidores ocorre em uma estrutura de "anel", onde um token é passado sequencialmente entre os nós; o servidor que possui o token tem permissão para acessar o recurso. Embora o Token Ring seja eficiente para pequenos sistemas onde todos os servidores estão conectados em rede de maneira estável, ele pode ser menos adequado para sistemas com comunicação intermitente ou alto dinamismo.
Ao contrário do Token Ring, o Algoritmo de Lamport:
Elimina a dependência de um token físico: Em um sistema descentralizado como este, a perda do token ou uma falha de comunicação poderia interromper as operações no modelo Token Ring.
Facilita a flexibilidade na rede: No Algoritmo de Lamport, cada servidor gerencia suas próprias requisições sem precisar esperar pela passagem de um token, o que torna o sistema mais robusto e adaptável a falhas individuais de servidores.
Escala melhor para ambientes distribuídos: A capacidade de Lamport de operar com clocks lógicos permite que novos servidores sejam adicionados com mínima reconfiguração, enquanto o Token Ring exigiria a adaptação da estrutura do "anel" para incluir novos servidores.
Assim, o Algoritmo de Lamport foi escolhido para este sistema devido à sua eficiência na coordenação de concorrência em ambientes descentralizados e à maior robustez diante de falhas, características que tornam esse método ideal para o controle de concorrência no contexto de um sistema de reserva de passagens distribuído.

### 2.3 Isolamento de Servidores com Docker
Cada servidor é encapsulado em um container Docker, isolando seu ambiente e facilitando a simulação de um sistema distribuído. Essa abordagem permite replicar servidores facilmente, possibilitando uma infraestrutura de testes consistente e escalável.

### 2.4 Principais Funcionalidades Implementadas
A seguir, detalhamos as funcionalidades implementadas no sistema, cada uma desempenhando um papel crucial na operação do sistema de reserva distribuído:
- **Consulta de Trechos:**
- - Endpoint /trechos: Cada servidor permite a consulta dos trechos disponíveis, retornando as rotas que atendem ao filtro de origem e destino especificado pelo cliente. A função fetch_trechos_from_servers() no código realiza a agregação dos trechos de todos os servidores conectados, permitindo que o sistema ofereça um itinerário completo, integrando as rotas disponíveis entre os servidores. A função create_graph() converte os trechos em um grafo direcionado, onde as rotas entre diferentes cidades são representadas por arestas. Esse grafo permite que a aplicação busque trajetos completos, compondo viagens com trechos de diferentes companhias.
- **Compra de Passagem:**
- - Endpoint /comprar: A funcionalidade de compra realiza uma série de verificações para assegurar a disponibilidade do trecho antes de concluir a operação. Para cada trecho na rota selecionada pelo cliente, o sistema verifica a disponibilidade de passagens e adquire um lock temporário, evitando que outros clientes possam reservá-lo simultaneamente. Após a verificação de todos os trechos e a conclusão da compra, a função request_purchase() solicita a atualização dos servidores responsáveis por cada trecho.
- **Atualização de Trechos:**
- - Endpoint /update_trecho: Quando uma compra é realizada, a quantidade de passagens disponíveis para o trecho é decrementada e o estado atualizado é salvo no servidor local. Isso é feito por meio da função update_trecho(), que também remove o trecho do sistema se as passagens estiverem esgotadas, evitando que outros clientes tentem reservar uma rota inexistente.
- **Exclusão Mútua e Liberação de Locks:**
- - Endpoint /release: Após a conclusão de uma compra ou em caso de erro, o servidor libera os locks adquiridos para os trechos reservados. A função release_access() é responsável por essa liberação, removendo a requisição da fila e enviando uma notificação de liberação para os demais servidores. Esse mecanismo de liberação permite que novos clientes possam acessar a rota, mantendo a disponibilidade do sistema de forma eficiente.

### 2.5 Estrutura de Testes
Um arquivo de teste teste_exclusao_mutua.py foi implementado para verificar a validade do sistema em condições de concorrência. Esse teste simula múltiplos clientes tentando comprar o mesmo trecho simultaneamente, verificando a capacidade do sistema de respeitar o limite de passagens e de aplicar corretamente a exclusão mútua. O teste:
Inicia múltiplas threads representando clientes diferentes;
Cada thread realiza uma tentativa de compra para o mesmo trecho;
Registra os resultados, incluindo o número de compras bem-sucedidas e falhas.
Com isso, o sistema foi validado para operar conforme esperado, evitando conflitos e garantindo que o número de compras bem-sucedidas corresponde ao limite de passagens disponíveis.

## 3. Discussão e Resultados

### 3.1 Resultados dos Testes
O teste de exclusão mútua (teste_exclusao_mutua.py) foi conduzido para avaliar como o sistema lida com várias tentativas de compra simultâneas para o mesmo trecho. Os resultados demonstraram que o sistema respeita o número máximo de passagens disponíveis: das 12 tentativas de compra simuladas, 10 foram concluídas com sucesso, enquanto as demais foram bloqueadas quando as passagens se esgotaram. Esse resultado confirma que o sistema consegue gerenciar de maneira eficaz a concorrência e evitar reservas duplicadas, garantindo que cada trecho só seja vendido até o limite permitido.
### 3.2 Casos de Erro e Tratamento de Conflitos
O sistema foi projetado para lidar de forma confiável com falhas nas reservas. Quando uma tentativa de compra não é concluída, seja por falta de passagens ou por outros motivos, o trecho é rapidamente liberado para que outros clientes possam tentar reservá-lo. Esse mecanismo assegura que falhas temporárias ou erros de transação não deixem o trecho bloqueado de forma permanente, o que permite uma experiência de uso estável e contínua para todos os clientes.
### 3.3 Desempenho e Escalabilidade
A arquitetura do sistema facilita a adição de novos servidores e permite que o sistema cresça conforme aumenta o número de companhias e de clientes. Esse modelo modular ajuda a manter um desempenho consistente, mesmo com um volume crescente de transações. Com essa estrutura, o sistema se mostra bem adaptado para suportar uma expansão gradual e confiável, à medida que novas companhias se conectam à rede.
### 3.4 Limitações e Melhorias Futuras
Um ponto a ser melhorado é a questão da latência, que pode ser percebida quando há um grande volume de requisições simultâneas ou quando os servidores estão geograficamente distantes. Como aprimoramento futuro, o sistema poderia incluir um monitoramento mais detalhado das transações e do uso do sistema, o que ajudaria na auditoria e facilitaria ajustes para reduzir possíveis atrasos. Esse tipo de otimização garantiria que o sistema permaneça ágil e confiável à medida que a demanda aumente.

## 4. Conclusão
### 4.1 Resumo dos Pontos Principais
Este projeto demonstrou a viabilidade de um sistema distribuído de reserva de trechos entre companhias aéreas, com controle de concorrência e preservação da preferência de reserva. A arquitetura RESTful e o isolamento em containers Docker conferem ao sistema a flexibilidade necessária para operar em uma rede descentralizada, proporcionando uma solução robusta e escalável.

### 4.2 Validade da Solução
Os testes comprovaram que o sistema é capaz de lidar com múltiplas requisições simultâneas, mantendo a exclusão mútua e a prioridade de atendimento ao cliente que iniciou a compra primeiro. Essa abordagem se mostrou confiável e pronta para aplicação em um ambiente real, garantindo que a concorrência entre clientes seja resolvida de forma justa e eficiente.

### 4.3 Aprendizados em Programação e Redes
O desenvolvimento deste projeto proporcionou um aprendizado significativo sobre programação distribuída e redes, especialmente na integração de serviços independentes em um sistema coeso. A implementação do Algoritmo de Lamport ajudou a compreender na prática a importância de técnicas de controle de concorrência em ambientes distribuídos, onde a ausência de um servidor central exige uma coordenação cuidadosa entre múltiplos nós. Além disso, o uso de contêineres Docker reforçou conhecimentos em deploy de aplicações e gestão de dependências, essenciais para sistemas escaláveis e isolados. A arquitetura RESTful possibilitou uma melhor compreensão dos desafios e vantagens da comunicação sem estado, permitindo que cada servidor funcione de forma independente, mas integrado com os demais.
A configuração dos servidores de forma distribuída também destacou a importância da estabilidade da rede e dos protocolos de comunicação. Compreender a maneira como os dados trafegam entre servidores e lidar com potenciais atrasos ou falhas de rede aumentou a familiaridade com redes de computadores e o impacto da latência em aplicações reais. Esse aprendizado prático forneceu uma visão aprofundada dos desafios comuns em sistemas distribuídos e da importância de uma boa arquitetura de rede para evitar gargalos e conflitos.

## 5. Referências
PYTHON Software Foundation. Python documentation: socket — Low-level networking interface. Disponível em: https://docs.python.org/3/library/socket.html. Acesso em: out. 2024.

Grinberg, M. Flask Documentation. Flask, Pallets Projects, https://flask.palletsprojects.com/en/latest/. Acesso em: out. 2024.

DOCKER INC. O que é Docker?. Disponível em: https://www.docker.com/what-docker. Acesso em: out. 2024.

FABRICIO VERONEZ. Docker do zero ao compose: Parte 01. Disponível em: https://www.youtube.com/watch?v=GkMJJkWRgBQ. Acesso em: out. 2024.

PYTHON Software Foundation. pickle — Python object serialization. Disponível em: https://docs.python.org/3/library/pickle.html. Acesso em: out. 2024.

RODRIGUES, Douglas. A Evolução da Internet: Desde os Primórdios até os Dias Atuais. YouTube, 28 out. 2023. Disponível em: https://www.youtube.com/watch?v=DaPHo_VFccg. Acesso em: nov. 2024.

RODRIGUES, Douglas. Inovações Tecnológicas: O Futuro das Comunicações Digitais. YouTube, 29 out. 2023. Disponível em: https://www.youtube.com/watch?v=EmcWq_DvqcA. Acesso em: nov. 2024.

FERNANDES, Luiz Gustavo Leão. Algoritmos Distribuídos. Pontifícia Universidade Católica do Rio Grande do Sul. Disponível em: https://www.inf.pucrs.br/gustavo/disciplinas/ppd/material/slides-algos_distr-novo.pdf. Acesso em: nov. 2024.

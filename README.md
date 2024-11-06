Implementação de Sistema para Venda de Trechos Distribuídos entre Companhias Aéreas
Autores:
Davi Jatobá Galdino, Gabriel Sena Barbosa

Instituição:
Universidade Estadual de Feira de Santana (UEFS)
Av. Transnordestina, s/n, Novo Horizonte - BA, 44036-900

Contato:

Emails: ddavijatoba33@gmail.com, gabriel.sena.barbosa@gmail.com
Abstract
In the low-cost aviation sector, there is an increasing demand for systems that enable route sharing among airlines, facilitating integrated ticket reservations. Currently, each airline operates its own sales server, which complicates the purchase of tickets across routes involving multiple carriers. This work presents a decentralized solution that connects the servers of partner airlines and allows for multi-leg reservations. Three servers were developed in Python using a RESTful architecture with Flask, enabling communication between them. The Lamport algorithm was implemented to resolve reservation conflicts, ensuring that the first customer to make a reservation has priority. Running on Docker containers, this solution provides customers with an integrated and efficient experience, allowing for quick and secure reservations across different airlines.

Resumo
No setor de aviação de baixo custo, há uma crescente demanda por sistemas que possibilitem o compartilhamento de trechos entre companhias, facilitando a realização de reservas integradas de passagens. Atualmente, cada companhia opera seu próprio servidor de vendas, o que dificulta a compra de passagens em rotas que envolvem mais de uma empresa. Este trabalho apresenta uma solução descentralizada que conecta os servidores das companhias aéreas e permite reservas de múltiplos trechos entre as companhias conveniadas. Para isso, foram desenvolvidos três servidores em Python com uma API de arquitetura REST, utilizando Flask, que se comunicam entre si. O algoritmo de Lamport foi implementado para resolver conflitos de reserva, assegurando que o primeiro cliente a realizar uma reserva tenha prioridade. Com a solução executada em contêineres Docker, o sistema oferece uma experiência integrada e eficiente aos clientes, permitindo reservas de trechos entre diferentes companhias de maneira rápida e segura.

1. Introdução
O setor de aviação de baixo custo (LCCs) tem experimentado uma demanda crescente por sistemas de reservas que ofereçam uma experiência integrada e possibilitem o compartilhamento de trechos entre diferentes companhias. No entanto, a estrutura atual, onde cada companhia aérea opera um servidor centralizado próprio para vendas, dificulta a reserva de passagens que envolvam mais de uma empresa, tornando o processo fragmentado e menos acessível para o cliente.

Para resolver esse problema, este projeto propõe uma solução descentralizada que permite a comunicação entre os servidores das companhias aéreas conveniadas, facilitando reservas de múltiplos trechos em diferentes empresas. A solução foi desenvolvida utilizando uma API REST, implementada em Python com o framework Flask, e integra três servidores que se comunicam entre si. Esse sistema de comunicação descentralizado adota o algoritmo de Lamport para resolver conflitos de reserva, assegurando que o cliente que realiza a compra primeiro tenha prioridade sobre os trechos reservados. Com o uso de contêineres Docker, a implementação garante escalabilidade, isolamento e uma execução confiável e segura.

Este relatório aborda o desenvolvimento do sistema, destacando as decisões de projeto, as funcionalidades implementadas e os testes realizados para validar a solução. A proposta é fornecer uma experiência de compra eficiente e simplificada aos clientes, permitindo-lhes reservar trechos de diferentes companhias de forma integrada e segura.

2. Metodologia Utilizada
2.1 Arquitetura RESTful
O sistema foi implementado com uma arquitetura RESTful, conforme exigido no enunciado do problema, para garantir a comunicação entre os servidores das companhias aéreas de forma interoperável e segura. O uso do padrão REST é adequado para sistemas distribuídos como este devido à sua capacidade de facilitar transmissões de dados stateless (sem estado), o que permite que cada requisição seja autossuficiente e contenha todas as informações necessárias para ser processada, reduzindo a necessidade de manutenções complexas de sessão.

Consulta de Trechos: Cada servidor expõe um endpoint para consultar os trechos de viagens disponíveis. Esse endpoint é configurado para aceitar parâmetros de origem e destino, retornando uma lista dos trechos possíveis entre essas localidades. Para ampliar as possibilidades de conexão entre as rotas, o sistema também consulta trechos em servidores conveniados.

Compra de Passagem: O endpoint de compra permite que o cliente selecione e reserve um trecho disponível, desde que ele ainda possua passagens. Caso a compra seja realizada com sucesso, o servidor bloqueia temporariamente a rota para garantir a exclusão mútua.

Atualização de Estado: Sempre que uma compra é realizada, o sistema atualiza o estado dos trechos no servidor que gerencia aquele trecho específico. Isso assegura que outros clientes não possam reservar o mesmo trecho até que ele esteja liberado novamente.

2.2 Controle de Concorrência com o Algoritmo de Lamport
A sincronização de transações entre os servidores foi garantida por meio do Algoritmo de Lamport, um método amplamente utilizado para ordenação de eventos em sistemas distribuídos. Esse algoritmo é fundamental para garantir que, mesmo em um ambiente descentralizado, a ordem de chegada das requisições seja respeitada. Ao adotar o Algoritmo de Lamport, cada servidor mantém controle local das requisições de forma eficiente, o que evita a necessidade de um coordenador central ou de uma comunicação excessivamente complexa entre os servidores.

As principais etapas do controle de concorrência implementado são:

Relógio Lógico (Timestamp): Cada servidor possui um relógio lógico que incrementa a cada nova requisição. Esse timestamp é usado para registrar a ordem de chegada das requisições, garantindo que a prioridade para acessar um recurso específico seja sempre dada à requisição com o menor timestamp.

Fila de Requisições: Cada servidor enfileira suas requisições de compra em uma fila que respeita a ordem dos timestamps. A fila é verificada constantemente, de modo que a próxima requisição a ser atendida é sempre a de menor timestamp, assegurando a sequência correta das operações.

Exclusão Mútua: Durante o processamento de uma compra, o trecho específico é bloqueado temporariamente, impedindo que outras requisições modifiquem seu estado até a conclusão da operação. Esse mecanismo evita condições de corrida e assegura que o cliente que iniciou a compra primeiro mantenha a preferência sobre o recurso.

3. Discussão e Resultados
3.1 Resultados dos Testes
O teste de exclusão mútua (teste_exclusao_mutua.py) foi conduzido para avaliar como o sistema lida com várias tentativas de compra simultâneas para o mesmo trecho. Os resultados demonstraram que o sistema respeita o número máximo de passagens disponíveis: das 12 tentativas de compra simuladas, 10 foram concluídas com sucesso, enquanto as demais foram bloqueadas quando as passagens se esgotaram. Esse resultado confirma que o sistema consegue gerenciar de maneira eficaz a concorrência e evitar reservas duplicadas, garantindo que cada trecho só seja vendido até o limite permitido.

3.2 Casos de Erro e Tratamento de Conflitos
O sistema foi projetado para lidar de forma confiável com falhas nas reservas. Quando uma tentativa de compra não é concluída, seja por falta de passagens ou por outros motivos, o trecho é rapidamente liberado para que outros clientes possam tentar reservá-lo. Esse mecanismo assegura que falhas temporárias ou erros de transação não deixem o trecho bloqueado de forma permanente, o que permite uma experiência de uso estável e contínua para todos os clientes.

3.3 Desempenho e Escalabilidade
A arquitetura do sistema facilita a adição de novos servidores e permite que o sistema cresça conforme aumenta o número de companhias e de clientes. Esse modelo modular ajuda a manter um desempenho consistente, mesmo com um volume crescente de transações. Com essa estrutura, o sistema se mostra bem adaptado para suportar uma expansão gradual e confiável, à medida que novas companhias se conectam à rede.

3.4 Limitações e Melhorias Futuras
Um ponto a ser melhorado é a questão da latência, que pode ser percebida quando há um grande volume de requisições simultâneas ou quando os servidores estão geograficamente distantes. Como aprimoramento futuro, o sistema poderia incluir um monitoramento mais detalhado das transações e do uso do sistema, o que ajudaria na auditoria e facilitaria ajustes para reduzir possíveis atrasos. Esse tipo de otimização garantiria que o sistema permaneça ágil e confiável à medida que a demanda aumente.

4. Conclusão
4.1 Resumo dos Pontos Principais
Este projeto demonstrou a viabilidade de um sistema distribuído de reserva de trechos entre companhias aéreas, com controle de concorrência e preservação da preferência de reserva. A arquitetura RESTful e o isolamento em containers Docker conferem ao sistema a flexibilidade necessária para operar em uma rede descentralizada, proporcionando uma solução robusta e escalável.

4.2 Validade da Solução
Os testes comprovaram que o sistema é capaz de lidar com múltiplas requisições simultâneas, mantendo a exclusão mútua e a prioridade de atendimento ao cliente que iniciou a compra primeiro. Essa abordagem se mostrou confiável e pronta para aplicação em um ambiente real, garantindo que a concorrência entre clientes seja resolvida de forma justa e eficiente.

4.3 Aprendizados em Programação e Redes
O desenvolvimento deste projeto proporcionou um aprendizado significativo sobre programação distribuída e redes, especialmente na integração de serviços independentes em um sistema coeso. A implementação do Algoritmo de Lamport ajudou a compreender na prática a importância de técnicas de controle de concorrência em ambientes distribuídos, onde a ausência de um servidor central exige uma coordenação cuidadosa entre múltiplos nós. Além disso, o uso de contêineres Docker reforçou conhecimentos em deploy de aplicações e gestão de dependências, essenciais para sistemas escaláveis e isolados. A arquitetura RESTful possibilitou uma melhor compreensão dos desafios e vantagens da comunicação sem estado, permitindo que cada servidor funcione de forma independente, mas integrado com os demais.

5. Referências
PYTHON Software Foundation. Python documentation: socket — Low-level networking interface. Disponível em: https://docs.python.org/3/library/socket.html. Acesso em: out. 2024.
Grinberg, M. Flask Documentation. Flask, Pallets Projects, https://flask.palletsprojects.com/en/latest/. Acesso em: out. 2024.
DOCKER INC. O que é Docker?. Disponível em: https://www.docker.com/what-docker. Acesso em: out. 2024.
FABRICIO VERONEZ. Docker do zero ao compose: Parte 01. Disponível em: https://www.youtube.com/watch?v=GkMJJkWRgBQ. Acesso em: out. 2024.
PYTHON Software Foundation. pickle — Python object serialization. Disponível em: https://docs.python.org/3/library/pickle.html. Acesso em: out. 2024.
RODRIGUES, Douglas. A Evolução da Internet: Desde os Primórdios até os Dias Atuais. YouTube, 28 out. 2023. Disponível em: https://www.youtube.com/watch?v=DaPHo_VFccg. Acesso em: nov. 2024.
RODRIGUES, Douglas. Inovações Tecnológicas: O Futuro das Comunicações Digitais. YouTube, 29 out. 2023. Disponível em: https://www.youtube.com/watch?v=EmcWq_DvqcA. Acesso em: nov. 2024.
FERNANDES, Luiz Gustavo Leão. Algoritmos Distribuídos. Pontifícia Universidade Católica do Rio Grande do Sul. Disponível em: https://www.inf.pucrs.br/gustavo/disciplinas/ppd/material/slides-algos_distr-novo.pdf. Acesso em: nov. 2024.

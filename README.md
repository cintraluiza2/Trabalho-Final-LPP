# Trabalho-Final-LPP
O seguinte repositório guarda o código do trabalho final da disciplina de Linguagem e Paradigma de Programação.

O trabalho foi estruturado utilizando as linguagens de programação Python e JavaScript. 

A ideia consiste em desenvolver um chatbot (denominado Heloisa) que auxilia indivíduos com aconselhamentos diversos para entrevistas e trabalhos na área de vendas. Para isso, foi utilizado um LLM (gpt-3.5 turbo) que modela toda a parte de Processamento de Linguagem Natural do chatbot. Também foi adicionado um memory buffer para que o modelo consiga guardar o tom da conversa e as perguntas e respostas anteriores, mantendo o contexto conversacional. Para aplicar o modelo especificamente para a área de vendas, foi utilizado um RAG (retrieval augmented generation) que é uma técnica de otimização dinâmica para adaptar o modelo para contextos específicos. O RAG pode ser utilizado de diversas maneiras, desde definindo prompts específicos (que foi a solução escolhida para o trabalho) através de arquivos .txt até a incorporação de documentos/artigos para serem revisitados de maneira dinâmica durante a execução do programa.

Foi utilizado o framework Flask para fazer a integração do back-end em Python com o Front-end desenvolvido com a linguagem de marcação HTML e uma parte de tratamento de erros/exceções em JavaScript. O layout da aplicação é bastante simples, focando na estrutura de chat message e na interação do usuário com a Heloisa (chatbot). Além do RAG, o modelo contempla uma função para lidar com perguntas que estão fora do banco de dados do RAG, respondendo de maneira generalista. 

Buscando contemplar os assuntos estudados na disciplina, o código, apesar de bastante enxuto (já que a linguagem Python acaba trabalhando muito mais com a utilização de bibliotecas do que aplicação 100% procedural de execução de funções e alocação/desalocação de objetos em memória, como C, por exemplo) contempla muitos assuntos que foram vistos ao longo do curso, a saber:

Paradigma Orientado a Objetos (POO)
Descrição:
O uso do framework Flask em Python exemplifica abstração e encapsulamento. As funcionalidades, como inicialização do servidor e rotas, são implementadas como métodos de objetos que o framework Flask gerencia.
A biblioteca LangChain também utiliza classes, como OpenAI, FAISS e ConversationBufferMemory, que encapsulam funcionalidades específicas, alinhando-se aos conceitos de herança e reutilização.
Exemplo no código:
llm = OpenAI(temperature=0, openai_api_key="...", model_name="gpt-3.5-turbo-instruct")
vectorstore = FAISS.from_documents(documents, embeddings)
Aqui, objetos são criados a partir de classes para encapsular funcionalidades específicas.

Paradigma Funcional
Descrição:
Linguagens modernas como Python permitem o uso de paradigmas híbridos. Funções como answer_with_fallback seguem o estilo funcional ao operar sobre entradas e retornar saídas sem efeitos colaterais diretos.
Exemplo no Código:
def answer_with_fallback(question):
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(question)
    if docs:
        response = qa_chain.run(input_documents=docs, question=question)
        return response
    else:
        return llm.predict(question)
Essa função demonstra características funcionais: recebe uma entrada, processa, e retorna um resultado sem modificar estados globais.


Paradigma Baseado em Eventos
Descrição:
A interação entre cliente (HTML/JavaScript) e servidor (Flask) segue um paradigma baseado em eventos, onde eventos como cliques ou mensagens enviadas pelo usuário disparam ações específicas no sistema.
Exemplo no Código:
sendBtn.addEventListener('click', sendMessage);
inputMessage.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
Os event listeners implementam o paradigma baseado em eventos no frontend.

Abstração e Modulação
Descrição:

O código é modular, com diferentes partes da lógica separadas em funções (answer_with_fallback, chat) e camadas distintas (servidor Flask, processamento com LangChain, e interface do usuário em HTML/JavaScript).
O uso de bibliotecas externas como LangChain para embeddings, recuperação de informações e gerenciamento de memória exemplifica abstração.
Exemplo no Código:
app = Flask(__name__)
CORS(app)
A abstração proporcionada pelo Flask elimina a necessidade de implementar manualmente os detalhes de comunicação HTTP.

Processamento de Linguagem Natural (PLN)
Descrição:

O código faz uso de processamento de linguagem natural (PLN) para gerar respostas baseadas em dados contextuais e consultas ao modelo LLM.
Isso está associado ao conceito de linguagens baseadas em regras e manipulação de strings.
Exemplo no Código:
qa_chain = load_qa_chain(llm, chain_type="stuff")
response = qa_chain.run(input_documents=retrieved_docs, question=query)

Multiparadigma
Descrição:
O código Python combina paradigmas:
Orientado a objetos com o uso de classes do Flask e LangChain.
Funcional com a implementação de funções puras.
Imperativo com estruturas sequenciais e condicionais.

Programação Declarativa
Descrição:

Na parte de frontend (HTML), o estilo declarativo é evidente, pois o layout e o comportamento da interface são descritos, e não controlados diretamente.
Exemplo no Código:
<input id="input-message" type="text" placeholder="Type your message here..." />
Isso define a aparência e o comportamento do elemento sem especificar como ele será renderizado.



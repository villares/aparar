# APARAR 

### Anotador de Pranchas para Análise e Registro de Áreas Relativas

#### Objetivo
Ferramenta experimental para facilitar a anotação e posterior análise de documentos, especialmente "pranchas" usadas para representação de projetos, permitindo  marcar e identificar com categorias regiões do documento, gerando depois um relatório com quantificação das áreas relativas entre as regiões.

> [!NOTE]
> Este branch contém a tentativa de portar a ferramenta, saindo do Processing IDE 3.5.4, adotando a biblioteca [py5](https://py5coding) como infraestrutura.

#### Dependências e instalação
 - [Ambiente com Thonny + py5](https://abav.lugaralgum.com/como-instalar-py5/)
 - ...  (trabalho em andamento) 
 
#### Instruções de operação

- Selecione uma pasta com imagens PNG ou JPG com nomes no formato `AAAAA_BBBBB_CCC_texto_livre.png`
> `AAAAA` é um identificador de grupo (concurso, disciplina, etc.), `BBBBB` é um identificador de autor (aluno, equipe, etc.) e `CCC` é um identificador do número da prancha (ou página do documento).
> `AAAAA`, e `BBBBB` podem ter quaisquer número de caracteres, mas `CCC` deve ter exatamente 3 caracteres. Todo o texto após `CCC` será ignorado, e por isso é considerado como um "texto livre".
> Os identificadores serão usados na exportação dos relatórios em CSV, populando a primeira, segunda e terceira colunas. Pranchas de um mesmo grupo (`AAAAA`) e mesmo autor (`BBBBB`) produzirão linhas de totalização do projeto no relatório.

# APARAR 

### Anotador de Pranchas para Análise e Registro de Áreas Relativas

#### Objetivo
Ferramenta experimental para facilitar a anotação e posterior análise de documentos, especialmente "pranchas" usadas para representação de projetos, permitindo  marcar e identificar com categorias regiões do documento, gerando depois um relatório com quantificação das áreas relativas entre as regiões.

#### Dependências e instalação
 - Instale o Processing IDE 3.5.4 e a extensão modo Python ([instruções detalhadas](https://abav.lugaralgum.com/como-instalar-o-processing-modo-python/))
 - Baixe a pasta compactada da última versão e descompacte.
 - Use o Processing IDE para abrir o arquivo com terminação `.pyde` na pasta.

#### Instruções de operação

- Selecione uma pasta com imagens PNG ou JPG com nomes no formato `AAAAA_BBBBB_CCC_texto_livre.png`, sendo que `AAAAA` é um identificador de grupo (concurso, disciplina, etc.), `BBBBB` é um identificador de autor (aluno, equipe, etc.) e `CCC` é um identificador do número da prancha (ou página do documento). `AAAAA`, e `BBBBB` podem ter quaisquer número de caracteres, mas `CCC` deve ter exatamente 3 caractere (todo o texto após CCC serár ignorado). Os valores de serão usados na exportação do relatório em CSV, populando a primeira, segunda e terceira colunas. Pranchas de um mesmo grupo (`AAAAA`) e mesmo autor (`BBBBB`) produzirão linhas de de totalização do projeto no relatório.

[TODO: Mostrar exemplos de relatórios]

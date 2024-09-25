# SADATA
---
The **Academic Trajectories Data Analysis System** (SADATA) aims to enable a better understanding of the academic paths of students based on information available on the Lattes Platform. The tool provides a broad view of the geographical reach of educational centers, exchanges between institutions, graduates from each course, and the continuity of each individual's academic life.

## What is the project structure?
---
- **`db`** contains the set of curricula for data extraction
- **`src`** contains the modules that enable both general and specific analyses developed for the project
- **`results`** contains the files obtained as a result of data extraction and processing

## What are the general and specific analyses?
---
The **general analysis module** ensures the collection of information that is not focused on a particular institution. This allows for the visualization of facts and relationships that consider the education system as a whole.

On the other hand, the **specific analysis module** selects only individuals who, at some point, have built part of their academic journey at a selected institution. This approach allows for understanding the position of a given educational center in the general landscape and also enables the study of internal phenomena within the institution.

### What information is provided in the general analysis?
---
1. Academic records of each individual (`primary/historicos.csv`)
2. Major field and field of work of each individual (`primary/areasDeAtuacao.csv`)
3. Birthplaces and work locations of each individual (`primary/localizacao.csv`)
4. Connections established between universities across all academic records (`primary/conexoesUniversidades`)
5. Total number of completed courses (`quantitative/contFormacoesTotal.csv`)
6. Number of courses started (`quantitative/contHistoricosInicio.csv`)
7. Number of courses completed (`quantitative/contHistoricosFim.csv`)
8. Number of birthplaces (`quantitative/contNascimento.csv`)
9. Number of work locations (`quantitative/contAtuacao.csv`)
10. Number of major fields and fields of work (`quantitative/contAreas.csv`)
11. Geographical heatmap of birthplaces (`visualization/mapaNascimento.html`)
12. Geographical heatmap of work locations (`visualization/mapaAtuacao.html`)
13. Institutions that connected to others (`graph/nos.csv`)

### What information is provided in the specific analysis?
---
1. All the information mentioned in the previous section
2. Academic records of each individual at the selected institution (`primary/historicosUniversidade.csv`)
3. Number of degrees that each individual has at the selected institution (`primary/pontuacaoIndividual.csv`)
4. Number of courses started at the selected institution (`quantitative/contHistoricosUniInicio.csv`)
7. Number of courses completed at the selected institution (`quantitative/contHistoricosUniFim.csv`)

## What external programs enhance SADATA's analyses?
---
The following programs were used to improve the visualization of the extractions performed by SADATA:
- **OpenRefine** for data filtering
- **Flourish** for building treemaps of the number of courses completed
- **Gephi** for constructing graphs of connections between educational institutions
- *Python libraries* can be found in the `requirements.txt` file
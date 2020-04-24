
## Export trello board to github project. 

#### Motivation
I and my colleagues had a lot of the Trello boards, where each corresponds to certain github repository. Therefore, to avoid one level of, say, personal bureaucracy I created a script to convert trello board information to github project. 

Currently working for `TODO -> In Progress -> Done` scheme. (In the future scheme scheme might be dynamic.)


#### Run
Run script : `run.sh`, script is **self-explanatory**. Just fill placeholders

#### Console output example 

```
Trello board "Learn by building BigData apps" export finished.
Github project Learn by building BigData appsprocessing started...
log. created project: 4242388
log. created column "__ DONE Sprint 1 __ 12.11.2020 Sun - 18.11.2020 Sat" with id: 8596061
log. created 2 cards for column: 8596061
log. created column "TODO" with id: 8596062
log. created 7 cards for column: 8596062
log. created column "__ TODO Sprint 1 __ 12.11.2020 Sun - 18.11.2020 Sat" with id: 8596064
log. created 3 cards for column: 8596064
log. created column "In Progress" with id: 8596072
log. created 1 cards for column: 8596072
Github project Learn by building BigData appsprocessing finished.

```

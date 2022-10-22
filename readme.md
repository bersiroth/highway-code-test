# French highway code test

CLI application for french highway code practice.

```bash
Usage: command.py [OPTIONS] COMMAND [ARGS]...

  CLI application for french highway code practice.

Options:
  --help  Show this message and exit.

Commands:
  stats  View statistics.
  test   Answer to a question.
```

## Command 

### list

* question 
  * id (optional)
  * stop-on-failure (optional)
* stats
  * reset (optional)

### Question command

Command to answer a question with optional arguments questions id. 
```bash
Usage: command.py test [OPTIONS]

  Answer to a question.

Options:
  --help  Show this message and exit.

```

### Stats command

Command for render statistics with option for reset.
```bash
Usage: command.py stats [OPTIONS]

  View statistics.

Options:
  --help  Show this message and exit.

```

## Storage

Questions are stored in json file (read only).  
Statistics are stored in a json file (read/write).

## TODO

- [x] dans le cas d'une suite de question exclure la question precedente de la liste
- [x] option pour reset stats
- [x] stats de la session
- [x] ajouter un custom debug https://python-devtools.helpmanual.io/
- [x] ajouter un check static de typage http://mypy-lang.org/
- [x] creation du repo
- [x] ci github action
- [x] choisir l'id d'une question
- [x] gestion des sous text de question
- [x] choix du pays france par default, traduction des messages de l'app 
- [x] migration sur poetry 
- [ ] add code coverage in CI pytest-cov
- [ ] passage en DDD avec python injector
- [ ] profiter du DDD pour passer d'un sockage Json a une base SQLite
- [ ] update documentation (readme)
- [ ] logger
- [ ] renomer l'app en highway code test cli
- [ ] passer en python 3.10
- [ ] semver
- [ ] ajouter un check dynamique de typage https://pydantic-docs.helpmanual.io/

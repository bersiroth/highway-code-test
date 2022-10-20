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
- [ ] choisir l'id d'une question
- [ ] gestion des sous text de question
- [ ] choix du pays france par default, traduction des messages de l'app 
- [ ] renomer l'app en highway code test cli
- [ ] update documentation (readme)
- [ ] passage en DDD
- [ ] migration data json vers BDD
- [ ] ajouter un check dynamique de typage https://pydantic-docs.helpmanual.io/

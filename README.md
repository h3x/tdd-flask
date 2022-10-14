
This project has been taken as part of [this](testdriven.io/course/tdd-flask).

### Useful Pytest Commands
```bash
# normal run
$ docker-compose exec api python -m pytest "src/tests"

# disable warnings
$ docker-compose exec api python -m pytest "src/tests" -p no:warnings

# run only the last failed tests
$ docker-compose exec api python -m pytest "src/tests" --lf

# run only the tests with names that match the string expression
$ docker-compose exec api python -m pytest "src/tests" -k "config and not test_development_config"

# stop the test session after the first failure
$ docker-compose exec api python -m pytest "src/tests" -x

# enter PDB after first failure then end the test session
$ docker-compose exec api python -m pytest "src/tests" -x --pdb

# stop the test run after two failures
$ docker-compose exec api python -m pytest "src/tests" --maxfail=2

# show local variables in tracebacks
$ docker-compose exec api python -m pytest "src/tests" -l

# list the 2 slowest tests
$ docker-compose exec api python -m pytest "src/tests" --durations=2
```
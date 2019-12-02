# Axioms

These are the *axioms* or *rules* for my own development setup.

## Rationale

**Axioms** are postulates that are taken to be true in order to build a mathematical
system. With them, one can build more complex statements. In the same spirit,
[*the humble programmer*](https://www.cs.utexas.edu/~EWD/transcriptions/EWD03xx/EWD340.html)
has the need for the basic building blocks to develop new software, and these should
be always **true**, i.e. robust and reliable.

With this repository, one should be able to have basic building blocks that could enable
the eager developer to produce quality software of any kind.

## Structure

Everything is orchestrated through a [TOML](https://github.com/toml-lang/toml) file
`master-config.toml` where everything I use can be browsed freely, as well as a
Python parser that takes care of installing and updating everything.

All the configuration files are freely available to use under the stipulated license
packaged with this repository.

## Usage

When using for the **first time**, `install.sh` should be used to *bootstrap* everything.

If one simply wants the configuration to be applied, the `tasks.py` file takes care of updating or
installing everything in a modular fashion.

## Target platform

For now, this only works for most of the Ubuntu-based distributions with Pop!_OS being the primary one,
as it is assumed that the `apt` package manager is the default one. Maybe, in the future, could
more package managers be supported.

## Python version and environment

`python 3.8` is **compulsory** as the new [walrus operator](https://www.python.org/dev/peps/pep-0572/)
is employed. For this purpose, a `pyproject.toml` is bundled to be used by [`poetry`](https://poetry.eustace.io/)
or just to be more readable than a `setup.py` or `requirements.txt` files.

## End result

This is what you get with these configuration files:

![terminal](imgs/proof_of_concept.png)

![editor](imgs/editor.png)
# Lever

A simple SQLite ORM build in python for use in personal projects.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contribution](#contribution)
- [License](#license)
- [Contact](#contact)

## Overview

Lever is a simple project that makes it easy to use a SQLite database. The major functionalities, such as table creation, insertion, deletion, ordering, etc., are wrapped by functions.

## Features

- Abstraction: Provides an abstraction layer that allows developers to interact with databases using programming language objects instead of writing raw SQL queries.
- Query Generation: Automatically generates SQL queries based on high-level method calls, reducing the need to write complex queries manually.
- Data Migration: Provides tools for managing database schema changes and versioning, making it easier to update databases as the application evolves.

## Installation

Coming soon. For now, you can clone or download this repo and use the lever folder in your projects like a personal package.

## Usage

First, you need to import the Database class from Lever, which makes all the magic, and pass the sqlite path.

```python
from lever import Database

db = Database('path/to/sqlite')
```

## Contribution

Explain how others can contribute to your project. This could include instructions to clone the repository, create branches, open pull requests, among other guidelines.

## License

Specify the license of your project so others know how they can use, modify, and distribute your code.

## Contact

Provide contact information such as email or links to social media so people can reach out with questions, suggestions, or feedback about the project.

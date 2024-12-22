# JSON Parser

## Overview

This project is a JSON parser implemented in Python. It provides functionality to parse JSON strings into Python dictionaries and validate the structure of JSON data. The parser is designed to handle various JSON structures and report errors for invalid JSON inputs.
This project is a solution to the [WC-lite challenge](https://codingchallenges.fyi/challenges/challenge-json-parser) on Coding Challenges.

## Getting Started

### Prerequisites

- Python 3.9 or higher

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/json-parser.git
    cd json-parser
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```


### Running the Parser

To run the parser, execute the [main.py](http://_vscodecontentref_/9) script:
```sh
python main.py
```

### Running the Tests
To run the unit tests, execute the test.py script:
```sh
python test.py
```

### Usage
The main functionality of the parser is provided by the jparse module. You can use the from_string function to parse a JSON string:
```sh
import jparse
json_str = '{"key": "value", "key2": 123}'
parsed_data = jparse.from_string(json_str)
print(parsed_data)
```

### Error Handling
The parser raises exceptions for invalid JSON inputs. The unit tests in test.py cover various scenarios of valid and invalid JSON data to ensure the correctness of the parser
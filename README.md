# Generative Playground

## Prerequisites

1. Make sure you have `python3` and `vertualenv` installed
2. Make sure you have `.env` file in the root directory with the following variables:
```bash
OPENAI_API_KEY=YOUR_API_KEY
GITHUB_TOKEN=YOUR_GITHUB_TOKEN
GITHUB_REPOSITORY=YOUR_GITHUB_REPOSITORY
```

<br/>

## Installation
1. Clone the repo
```bash
git clone https://github.com/diegofiori/generative-playground.git
```

2. cd to the project root directory and create a virtual environment
```bash
virtualenv env
```
3. Activate the virtual environment
```bash
source env/bin/activate
```
4. Install the dependencies
```bash
pip install -r requirements.txt
```

<br/>


## Usage

1. Run the main interactive console interface
```
python src/main.py 
```

2. Run voice2image 
```
python src/main.py --v
```

3. Run real-time-translate
```
python src/main.py --t
```

4. View the help menu for more options
```
python src/main.py --h
```





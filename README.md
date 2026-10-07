# ASE_Project

## Team
Hrushabhsingh Chouhan, Vasu Agrawal, Apoorva Chauhan  

![License](https://img.shields.io/github/license/apoorvacha/ASE_HW2)
![License](https://app.travis-ci.com/apoorvacha/ASE_HW1.svg?branch=master)
![License](https://img.shields.io/github/issues/apoorvacha/ASE_HW2?style=plastic)
![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7562628.svg)
[![Python application](https://github.com/apoorvacha/ASE_Project/actions/workflows/main.yml/badge.svg)](https://github.com/apoorvacha//actions/workflows/main.yml)



## Instructions to run the project 
Inside the src folder there are files for all the project which contains a Start.py for all the test cases.  To run the Project follow the steps given below
1. Clone the repository
2. Navigate to the source folder in the ASE_project from terminal that needs to execute using <br>
cd source <br>
4. Run the following command to run all the test cases
python3 Start.py -g 
etc/data/file name 

Note : enter the file path on the next line after "python3 Start.py -g" and give the exact location such as "etc/data/auto93.csv"


### Github Actions
You can also check the result in Github Actions for the file you uploaded. 


## LLM analysis extension

The project includes an optional LLM explanation layer in `source/LLMAnalyzer.py`. It accepts structured results produced by the optimization/ML pipeline and requests a concise explanation that is grounded only in those supplied results.

### Configuration

No API key is stored in the repository. Configure the provider at runtime:

```bash
export LLM_API_KEY="..."
export LLM_BASE_URL="https://api.openai.com/v1"   # any compatible endpoint
export LLM_MODEL="gpt-4o-mini"
```

The client uses a streaming chat-completions request and records:
- time to first token (TTFT)
- total response latency
- completion token count
- output token throughput (tokens/second)
- request success/failure and provider errors

### QA strategy

`source/test_llm_analyzer.py` mocks the provider, so CI requires neither credentials nor paid API calls. Tests verify prompt grounding, missing-credential behavior, streamed output and metrics, and provider-failure handling.

Run:

```bash
cd source
pytest Examples.py test_llm_analyzer.py --cov=. --cov-report=term-missing
```

GitHub Actions runs the same suite for pushes and pull requests.

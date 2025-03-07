# Third_Wish_Test by Pablo Sancho

Welcome to my proposed solution to the requested task by the company **Third Wish**.  
You can see full details of the proposed problem in the file **Test (7).pdf**.

## Project Overview
This project is designed to **process, mutate, and evaluate problems** using an AI-based approach.  
It includes:
- **Problem mutation** (rephrasing, expansion, simplification, adding constraints).
- **Leaderboard management** to track top problems.
- **Integration with OpenAI API** for problem evaluation.
- **Logging and error handling** to ensure smooth execution.

---

## Setup & Installation

### **1. Clone the repository**
```sh
git clone https://github.com/Pabliiiich07/Third_Wish_Test.git
cd Third_Wish_Test
```

### **2. Run installation script or do it manually**
Run **setup_and_run.sh** file:
```sh
sh ./scripts/setup_and_run.sh
```

Or do it manually by putting:
```sh
sh ./scripts/setup_and_run.sh
source venv/bin/activate
pip install -r requirements.txt
```

### **3. Set up environment variables**
Create a **.env** file and add your OpenAI API key:
```sh
OPENAI_API_KEY=your_api_key_here
```

### **4. Input Parameters**
- `--strategy`: **Required**. Choose from `rephrase`, `expand`, `simplify`, or `add_constraints` for mutation.
- `--num_rounds`: **Optional**. Number of rounds (default: `1`).
- `--output`: **Optional**. Output file name (default: `mutated_problems`).
- `--agent`: **Optional**. NLP model to use (default: `gpt-4o-mini`).
- `--num_problems`: **Optional**. Number of problems per round (default: `2`).
- `--topk_problems`: **Optional**. Number of top problems to keep per round (default: `4`).
- `--clean_output`: **Optional**. Whether to clean the output folder before execution (`yes` or `no`, default: `yes`).

## Example
```sh
python script.py --strategy rephrase --num_rounds 3 --output mutated_output --agent gpt-4o-mini --num_problems 5 --topk_problems 3 --clean_output yes
```
## Project Directory Structure

- `problems/`: 
  - Contains the `problems.txt` file and any other relevant data files that will be processed and mutated. This folder stores the original problems that will be worked on.

- `output/`: 
  - Stores the processed and mutated versions of the problems after the mutation strategies have been applied. This is where the final results are saved.

- `prompts/`: 
  - Contains the prompt templates that guide how the mutations should be applied to the problems. These templates are used to define how the problems should be reformulated, expanded, simplified, or have constraints added.

- `scripts/`: 
  - Houses auxiliary scripts, which could include shell scripts or other helper scripts needed to support the main functionality of the project.


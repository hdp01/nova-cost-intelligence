# 🤖 Nova Cost Intelligence: AI-Powered AWS FinOps Suite

A sophisticated cloud financial management tool that bridges the gap between raw AWS billing data and actionable business intelligence. This utility leverages the **Boto3 SDK** to aggregate multi-service cost metrics and utilizes the **Amazon Nova Micro** LLM via **Amazon Bedrock** to generate strategic optimization reports.

---

## 🌟 Key Features

- **Global Spend Visibility:** Aggregates daily cost data across all AWS services for a comprehensive 30-day financial snapshot, including a calculated **Grand Total**.
- **Deep Resource Auditing:** Specifically targets the "Big Three" of cloud waste:
  - **Compute (EC2):** Identifies unattached and idle EBS volumes.
  - **Database (RDS):** Monitors instance status and identifies potential idle DBs.
  - **Storage (S3):** Flags buckets missing Lifecycle Policies to prevent indefinite storage costs.
- **AI-Powered Strategy:** Uses **Amazon Nova Micro** to act as a Virtual CFO, providing:
  - Context-aware "Quick Win" suggestions when waste is detected.
  - Advanced "Growth Strategies" (Graviton, Savings Plans) when the account is already optimized.
  - Dynamic Risk Scoring (1–10) for infrastructure hygiene.
- **Professional CLI Dashboard:** Utilizes the `Rich` library for a high-end, terminal-based user interface with real-time status spinners and formatted tables.

---

## 🏗️ Architecture

The project follows a modular **Collector-Brain-Orchestrator** pattern:

1. **Collector (`src/collector.py`):** The data ingestion engine that interfaces with AWS Cost Explorer, EC2, RDS, and S3 APIs.
2. **Brain (`src/brain.py`):** The reasoning engine that processes raw JSON data and applies prompt engineering to the Amazon Nova LLM.
3. **Orchestrator (`main.py`):** The application entry point that manages data flow, state aggregation, and terminal rendering.

---

## 🛠️ Tech Stack

| Component          | Technology                         |
|--------------------|------------------------------------|
| **Language**       | Python 3.9+                        |
| **Cloud SDK**      | Boto3 (AWS SDK for Python)         |
| **AI Model**       | Amazon Nova Micro (via Bedrock)    |
| **UI Framework**   | Rich (Terminal formatting)         |
| **Environment**    | python-dotenv (Credential mgmt)    |

---

## 🚀 Getting Started

### Prerequisites

1. **AWS Account:** Ensure you have an active AWS account.
2. **Model Access:** Enable access to **Amazon Nova Micro** in the **Amazon Bedrock** console (typically in `us-east-1` or `us-west-2`).
3. **IAM Permissions:** Your IAM user needs `ReadOnly` access to Billing, EC2, RDS, and S3, plus `InvokeModel` permissions for Bedrock.
4. **Cost Explorer:** Manually "Launch" or "Enable" Cost Explorer in the AWS Billing console (Note: Data can take 24 hours to populate initially).

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/YOUR_USERNAME/nova-cost-intelligence.git
   cd nova-cost-intelligence
   ```

2. **Set up a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup:**

   The script automatically uses credentials from `aws configure`. If you prefer environment variables, create a `.env` file based on the provided template:

   ```bash
   cp .env.example .env
   ```

   Then fill in your credentials:

   ```text
   AWS_ACCESS_KEY_ID=your_key
   AWS_SECRET_ACCESS_KEY=your_secret
   AWS_DEFAULT_REGION=us-east-1
   ```

### Running the Audit

Execute the main orchestrator to start the scan:

```bash
python main.py
```

---

## 🛡️ Security & Best Practices

- **Zero Hardcoding:** No AWS keys are stored in the source code.
- **Git Safety:** The `.env` file and `venv/` directory are strictly excluded via `.gitignore`.
- **Least Privilege:** The application is designed to operate entirely on `ReadOnly` permissions.

---

## 📂 Project Structure

```text
nova-cost-intelligence/
├── src/
│   ├── __init__.py       # Package initializer
│   ├── collector.py      # AWS Resource & Cost data logic
│   └── brain.py          # AI Logic & Prompt Engineering
├── .env.example          # Template for local secrets
├── .gitignore            # Security filters for Git
├── main.py               # Application Entry Point & UI
└── requirements.txt      # Project dependencies
```

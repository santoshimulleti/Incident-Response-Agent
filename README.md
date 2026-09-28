# 🚨 AI-Powered Incident Response Agent

An AI-powered Incident Response Agent that combines **Groq AI** for intelligent reasoning with **Hindsight** for persistent incident memory.

The system helps investigate security incidents by recalling relevant previous incidents, analyzing the current incident using historical context, recommending response actions, and storing the final resolution for future investigations.

---

## 🎯 Problem Statement

Security teams often encounter similar incidents repeatedly. Previous investigation results and resolutions may not always be available when a new incident occurs.

This can lead to repeated investigation work and inconsistent response processes.

---

## 💡 Proposed Solution

The **AI Incident Response Agent** uses artificial intelligence and persistent memory to make incident investigation more knowledge-driven.

When a new incident is reported:

1. The system recalls related incidents from Hindsight.
2. Groq analyzes the current incident using the recalled information.
3. The agent provides possible root causes and investigation steps.
4. Recommended immediate response actions are generated.
5. The final investigation and resolution are stored in Hindsight.
6. Future similar incidents can use this stored knowledge.

---

## 🔄 Workflow

**Report → Recall → Reason → Resolve → Retain**

### 1. Report

The user provides incident details such as title, severity, affected system, and description.

### 2. Recall

Hindsight searches its persistent memory for relevant previous incidents and resolutions.

### 3. Reason

Groq analyzes the current incident using the recalled historical context.

### 4. Resolve

The agent provides investigation steps, possible root causes, and recommended actions.

### 5. Retain

The investigation and final resolution are stored back into Hindsight for future use.

---

## ✨ Key Features

* 🤖 AI-powered incident analysis
* 🧠 Persistent incident memory using Hindsight
* 🔎 Similar incident retrieval
* 🔍 Possible root-cause analysis
* 📋 Investigation steps
* ⚡ Immediate recommended actions
* 💾 Incident resolution storage
* 🔄 Historical knowledge reuse
* 📊 Before vs After Hindsight demonstration
* 🖥️ Interactive Streamlit interface

---

## 🧠 Persistent Memory

A major feature of this project is the use of **Hindsight persistent memory**.

Instead of analyzing every incident without historical context, the agent can recall related previous incidents and their resolutions.

For example:

**Previous Incident**

> Production database connectivity failure caused by an incorrect firewall rule.

The resolution is stored in Hindsight.

When a similar database incident occurs later, the system can recall the previous incident and provide investigation guidance using that historical knowledge.

---

## 🤖 AI Reasoning

The project uses **Groq AI** to analyze incident information.

The AI can provide:

* Possible Root Cause
* Investigation Steps
* Immediate Recommended Actions
* Relevant Previous Incident or Lesson
* Confidence Level

The AI analysis is enhanced by the relevant memories retrieved from Hindsight.

---

## 🖥️ Application Interface

The application is built using Streamlit and provides:

* Connection status for Groq and Hindsight
* Incident reporting form
* Severity selection
* Affected system details
* Incident description
* Previous incident retrieval
* AI-generated investigation analysis
* Incident resolution storage
* Before vs After Hindsight demonstration

---

## 🛠️ Technology Stack

| Technology    | Purpose                           |
| ------------- | --------------------------------- |
| Python        | Application development           |
| Streamlit     | Web interface                     |
| Groq AI       | AI-powered reasoning and analysis |
| Hindsight     | Persistent incident memory        |
| python-dotenv | Environment variable management   |

---

## 🏗️ Architecture

```text
                  ┌─────────────────────┐
                  │       User          │
                  │  Reports Incident   │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │     Streamlit       │
                  │    Application      │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │     Hindsight      │
                  │  Recall Memories   │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │      Groq AI        │
                  │ Analyze Incident    │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Investigation &     │
                  │ Recommendations     │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │   Incident          │
                  │   Resolution        │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │     Hindsight       │
                  │  Retain Knowledge  │
                  └─────────────────────┘
```

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/santoshimulleti/Incident-Response-Agent.git
```

### 2. Open the project directory

```bash
cd Incident-Response-Agent
```

### 3. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Create a `.env` file

Add your API keys:

```env
GROQ_API_KEY=your_groq_api_key
HINDSIGHT_API_KEY=your_hindsight_api_key
```

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🔐 Security

API keys should never be committed to the GitHub repository.

Store sensitive credentials in the `.env` file and make sure `.env` is included in `.gitignore`.

**Never publish real API keys in the repository.**

---

## 🎥 Demo Flow

The project demonstrates the following workflow:

```text
New Incident
     ↓
Recall Previous Incidents
     ↓
AI Analysis with Historical Context
     ↓
Investigation & Recommendations
     ↓
Resolve Incident
     ↓
Store Resolution
     ↓
Recall Knowledge During Future Incidents
```

---

## 🌟 Project Highlights

The key idea of this project is not just generating an AI response for an incident.

It creates a **persistent incident knowledge loop** where previous investigations and resolutions can be recalled and reused during future incidents.

This combines:

**AI Reasoning + Persistent Memory + Incident Response**

---

## 🔮 Future Scope

* Automated incident severity classification
* Integration with SIEM platforms
* Automated security alert ingestion
* Incident timeline generation
* PDF incident reports
* Team collaboration and incident tracking
* Integration with security monitoring tools
* Advanced incident correlation

---

## 👩‍💻 Project

**AI-Powered Incident Response Agent with Persistent Memory**

Built as a cybersecurity and AI hackathon project.

**GitHub:**
https://github.com/santoshimulleti/Incident-Response-Agent

# ECE 30861/46100 – Software Engineering
**Project Phase 1: A CLI for Trustworthy Pre-Trained Model Re-Use**  
_Last modified: 30 August 2025_

---

## Assignment Goal
This assignment will help you learn to work as a team on a small software engineering project. It is also intended to expose you to the benefits and risks of reusing open-source software and machine learning models.

---

## Relevant Course Outcomes
A student who successfully completes this assignment will have demonstrated the ability to:

- **Outcome I**
  - Identify and follow an appropriate software engineering process for this context.
- **Outcome II**
  - Convert requirements into project specifications.
  - Design the software project based on two UML diagrams.
  - Implement the project.
  - Validate the project.
  - Consider aspects of software re-use, including security risks.
- **Outcome III**
  - Experience social aspects of software engineering (communication, teamwork).

---

## Resources
- **UML diagrams**
  - [IEEE 1016-2009 Standard](https://ieeexplore.ieee.org/document/5167255)  
  - [UML (Wikipedia)](https://en.wikipedia.org/wiki/Unified_Modeling_Language)

- **REST APIs**
  - [Fielding’s Dissertation (Chapter 5: REST)](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)  
  - [20 years later commentary](https://twobithistory.org/2020/06/28/rest.html)  
  - [GitHub REST API docs](https://docs.github.com/en/rest)  
  - [Prof. Davis’ paper with Purdue students](https://docs.lib.purdue.edu/cgi/viewcontent.cgi?article=1179&context=ecepubs)

- **GraphQL APIs**
  - [GraphQL tutorial](https://graphql.org/learn/)  
  - [GitHub API intro](https://github.blog/2016-09-14-the-github-graphql-api/)  
  - [Prof. Davis GraphQL publications](https://davisjam.github.io/publications/)

- **Hugging Face**
  - [Quick Start Guide](https://huggingface.co/docs/transformers/en/quicktour)  
  - [Hugging Face Course](https://huggingface.co/learn/llm-course/chapter1/1)  
  - [API Guides](https://huggingface.co/docs/huggingface_hub/guides/overview)  

- **Security & Licensing**
  - [Empirical Study of Pre-Trained Model Reuse](https://arxiv.org/pdf/2303.02552)  
  - [PickleBall: Secure Deserialization](https://davisjam.github.io//files/publications/KellasChristouJiangLiSimonDavidKemerlisDavisYang-PickleBall-CCS2025.pdf)  
  - [ModelGo: License Analysis Tool](https://dl.acm.org/doi/pdf/10.1145/3589334.3645520)  
  - [Backdoor Learning Survey](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9802938)

- **Other**
  - [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects)  
  - [Scorecard Project](https://github.com/ossf/scorecard)  
  - [Postmortems at Google](https://sre.google/sre-book/postmortem-culture/)  
  - [Error Message Design](https://xd.adobe.com/ideas/process/information-architecture/error-message-design-ux/)  
  - [Commit Messages](https://reflectoring.io/meaningful-commit-messages/)

---

## Assignment Introduction
Your team is a subcontractor for **ACME Corporation**, which operates the ACME Web Service. They are building internal AI/ML services and want a catalogue of available AI/ML models that can be integrated. They are particularly interested in:

- Documentation quality (low ramp-up time).
- Standards of quality for open-source models.
- Documentation of datasets used to train models.
- Availability of example scripts for training/testing.
- Maintainer responsiveness for bug fixes.
- Flexibility to add new requirements later.

Additionally:
- ACME offers services through a REST API.
- They plan to release a **self-hosted, open-source version** in 3 years.
- They use the **LGPL v2.1 license**, so all integrated models must be license-compatible.

---

## Sarah’s Initial Project Specification

### System Input
- Support input from command line arguments.

### System Implementation
- Majority Python.
- All code must include type annotations.
- Use:
  - [Flake8](https://flake8.pycqa.org/) (linting & style)
  - [isort](https://pycqa.github.io/isort/) (import sorting)
  - [mypy](https://mypy-lang.org/) (type checking)

### System Output
- Print all output to `stdout`.
- Each model must show:
  - Overall score
  - Sub-scores: size, license, ramp-up time, bus factor, dataset/code availability, dataset quality, code quality, performance claims
- Support linked dataset/code objects.

### Other Requirements
- Show latency results for representative models.
- Metrics should run in parallel where possible.

---

## Auto-Grader API

- Project must include an executable file named **`run`** at the root.
- CLI commands:
  - `./run install`
  - `./run URL_FILE`
  - `./run test`

- Test requirements:
  - At least 20 distinct test cases.
  - At least 80% code coverage.
  - Output format:  
    ```
    X/Y test cases passed. Z% line coverage achieved.
    ```

- Logging:
  - Controlled via `$LOG_FILE` and `$LOG_LEVEL`.

---

## Metrics

- At least one metric must use **Hugging Face Hub API**.
- At least one metric must analyze repos **without the API** (local clone + analysis).
- Required fields include:
  - `net_score`
  - `ramp_up_time`
  - `bus_factor`
  - `performance_claims`
  - `license`
  - `size_score`
  - `dataset_and_code_score`
  - `dataset_quality`
  - `code_quality`

(All scored between `0–1`, with latencies measured in ms.)

---

## Project Management
- Use GitHub Project Boards for tracking.
- Weekly milestone updates required.
- Must justify software re-use choices.
- Reuse of **Stack Overflow snippets allowed with citation**.
- **Direct copy-pasting from open-source repos not allowed.**

---

## LLM Usage
- Required: analyze README/metadata with an LLM (e.g., SageMaker, Purdue GenAI API).
- Required: use LLM-assisted coding tools (e.g., GitHub CoPilot).
- Optional: use chat LLMs for planning/design.

---

## Timeline & Deliverables
- **Week 1**: Planning and Design (Project Plan Document).
- **Weeks 2-3**: Implementation and updates.
- **Week 4**: Delivery of software + report.
- **Week 5**: Postmortem report.

---

## Grading Rubric
- 20%: Design & Planning
- 10%: Milestones
- 60%: Working delivery
  - 30% runs & matches auto-grader
  - 10% test suite + coverage
  - 10% engineering practices
- 5%: Hand-off
- 5%: Postmortem

---

## Budget & Workload
- 40 hours per person max. (~8 hrs/week for 5 weeks).
- Plan for incremental delivery.
- Revised plan required if deviating from schedule.

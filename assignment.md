# Recruitment Assignment - Unit Test Agent and Agentic Workflow

## Context

The base repository, [https://github.com/cloudfidecareers/taskly-app](https://github.com/cloudfidecareers/taskly-app), contains a sample full-stack application built with:

- **Frontend:** React + TypeScript
- **Backend:** Python + FastAPI
- **Source control:** Git / GitHub

The project contains both code that already has unit tests and code for which unit tests have not yet been written.

**Before starting the assignment, create your own public repository on GitHub and add the code from the base repository as your starting point. Do not include the assignment instructions you received in your repository.**

Complete the entire assignment in your own repository. **You have a maximum of 3 days from receiving the assignment to complete it.** Once finished, email a link to your repository to [careers@cloudfide.com](mailto:careers@cloudfide.com).

## Task

The goal is to build a **custom agent with reusable skills**, running in an agent environment of your choice, and use them to:

- add missing unit tests and improve code coverage in the existing application, across both the frontend and backend,
- create an **automated workflow for pull requests** that supports creating and updating tests for changed code.

The agent should analyze the changes introduced in a pull request and, when it determines this is appropriate, **create or update unit tests for the changed code**.

The solution should:

- support both the frontend and backend,
- run automatically for pull requests,
- verify the generated or updated tests by running them,
- make the results available in the context of the pull request.

## Expected Implementation

The solution should include an **agentic workflow, a custom agent, and reusable skills** used during execution.

**The solution must be implemented on GitHub:** the repository, pull requests, and automated PR workflow must operate on GitHub, and the agent's results must be available in the context of the relevant GitHub pull request. The choice of agent environment, other tools, architecture, and project structure is **up to you**.

**An additional advantage would be to create an example pull request that adds a new feature and demonstrate the agentic workflow on that PR** — from analyzing the changes, through creating or updating tests and running them, to sharing the results in the context of the pull request.

## Evaluation Criteria

**The greatest weight in the evaluation goes to the custom agent, reusable skills, and agentic workflow, and to how well the solution follows best practices for security, reliability, and producing correct, useful results.**

## Documentation

Include a short `SOLUTION.md` file describing:

- the main technical decisions and their rationale,
- how to run the PR workflow and which prerequisites must be met,
- where the custom agent and skills are defined and how they are used during execution,
- an example run, including the agent's decisions, the skills used, and the test execution results,
- your assumptions,
- the solution's limitations,
- what you would extend or change for a production version.

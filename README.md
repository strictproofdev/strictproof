# StrictProof — Execution-Control Gateway for Agentic Systems

StrictProof is an execution-control gateway for agentic systems. It is designed to evaluate an action proposal before tool execution by applying identity, authorization, policy, and state-version checks.

The project also includes a receipt mechanism intended to provide independently verifiable evidence of an evaluated action.

## Current Status

This repository contains the current StrictProof core implementation.

Runtime verification and deployment claims are documented only when supported by reproducible test evidence.

Cloud Run and Firestore are deployment/integration targets unless their runtime use is explicitly demonstrated by repository evidence.

## Architecture

The intended execution-control boundary is:

Agent → ActionProposal → StrictProof Gateway → State/Policy Checks → Tool Layer → Receipt → Verifier

The repository separates proposal validation, authorization, policy evaluation, optimistic concurrency control, tool execution, and receipt verification.

## Local Development

### Requirements

- Python 3.11+
- uv or pip

### Installation

```bash
git clone https://github.com/strictproofdev/strictproof.git
cd strictproof
uv sync
```

Testing instructions will be expanded as the executable test suite is added.

## Security Boundary

Agent-generated output is treated as an action proposal rather than direct execution authority.

The gateway is responsible for evaluating the proposal before it reaches the tool-execution layer.

## Repository Status

The implementation is under active development. Components are added and verified incrementally to keep the repository consistent with reproducible evidence.

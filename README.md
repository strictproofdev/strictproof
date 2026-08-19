# StrictProof — Execution-Control Gateway for Agentic Systems

StrictProof is an execution-control gateway for agentic systems. It is designed to evaluate an action proposal before tool execution by applying identity, authorization, policy, and state-version checks.

The project also includes a receipt mechanism intended to provide independently verifiable evidence of an evaluated action.

## Current Status

This repository is under active development.

Runtime verification and deployment claims are documented only when supported by reproducible evidence.

Cloud Run and Firestore are deployment/integration targets unless their runtime use is explicitly demonstrated by repository evidence.

## Architecture

The intended execution-control boundary is:

Agent → ActionProposal → StrictProof Gateway → State/Policy Checks → Tool Layer → Receipt → Verifier

## Security Boundary

Agent-generated output is treated as an action proposal rather than direct execution authority.

The gateway is responsible for evaluating the proposal before it reaches the tool-execution layer.

## Development Status

Executable installation and testing instructions will be added together with the corresponding project configuration and test suite.

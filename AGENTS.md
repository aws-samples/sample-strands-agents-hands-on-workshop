# AGENTS.md

## What this is

Sample code for the Strands Agents hands-on workshop: one customer service agent built up across 7
modules (agent loop and tools, hooks, skills and steering, session managers, deploy to Amazon Bedrock
AgentCore Runtime, multi-agent, evals). Each module is a notebook plus a terminal `chat.py`.

## Layout

```
samples/
  01-agent-loop-tools/ 02-hooks/ 03-skills-steering/ 04-session-managers/
  05-deploy/ 06-multi-agent/ 07-evals/
  shared/                       Code shared across modules
  <module>/module-NN-*.ipynb    Walkthrough notebook (source of truth for explanations)
  <module>/chat.py              Interactive multi-turn terminal chat
  <module>/requirements.txt     Per-module dependencies
05-deploy/main.py               AgentCore entrypoint (BedrockAgentCoreApp + @app.entrypoint)
```

## Commands

```bash
cd samples/<module>
pip install -r requirements.txt     # or: uv pip install -r requirements.txt
python chat.py                      # terminal chat
jupyter nbconvert --to notebook --execute --output /tmp/out.ipynb module-NN-*.ipynb   # run a notebook end to end
```

Module 5 deploys with the AgentCore CLI (npm, Node.js 20+), tested with **1.0.1**:

```bash
sudo npm install -g @aws/agentcore@1.0.1 --ignore-scripts
agentcore create --name csdeploy --template empty
cd csdeploy && agentcore add runtime --name MyAgent --language python
# copy main.py, tools, steering, skills into app/MyAgent/, then uv init --bare + uv add
agentcore deploy
agentcore invoke --runtime MyAgent --payload '{"prompt": "..."}'
agentcore remove all --yes && agentcore deploy --yes   # cleanup
```

Requires AWS credentials with Amazon Bedrock access (region `us-east-1`). Never commit generated
`agentcore/` or `app/MyAgent/` folders; they hold account-specific state (see `.gitignore`).

## Conventions

- Follow the current Strands docs (strandsagents.com/docs/user-guide/sdk/...) and the AgentCore
  Developer Guide; don't use undocumented APIs.
- Notebooks keep `source` as a single string, `indent=1`, non-ASCII preserved, no trailing newline.
- The workshop prose lives in a separate Workshop Studio repo; a change here that alters commands or
  code shown to participants must be mirrored there.
- Minimum-version pins (`>=`) in `requirements.txt`; run `pip-audit` on the resolved tree before pushing.

## Gotchas

- `context_manager` can't be combined with `FileSessionManager`/`S3SessionManager` (strands-agents
  1.63+ raises `ValueError`). Module 4 uses `SnapshotSessionManager` + `context_manager="auto"`.
- AgentCore session IDs need 33+ characters.
- An `LLMSteeringHandler` can pause `process_refund` with an interrupt. `05-deploy/main.py` returns
  `{"status": "interrupted", "interrupts": [...]}` and resumes on
  `{"interrupt_responses": [{"interruptId": "...", "response": true}]}` (same session);
  `03-skills-steering/chat.py` asks y/N in the terminal. Both follow the Strands interrupts docs.

## Recent changes

- Module 4 moved to `SnapshotSessionManager` + `context_manager="auto"`; `snapshot_chat.py` merged
  into `chat.py`; `strands-agents>=1.64.0`.
- Module 5 updated to AgentCore CLI 1.0.1 commands (create/add runtime/invoke/cleanup).
- Steering interrupts are handled in `05-deploy/main.py` and `03-skills-steering/chat.py`; before,
  the next prompt after an interrupt failed with `must resume from interrupt`.

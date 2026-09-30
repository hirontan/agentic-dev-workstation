#!/usr/bin/env bash
set -u
agent_path=$1
printf 'Agent working directory: %s\n' "$PWD"
echo 'Read AGENTS.md and provide the Issue acceptance criteria inside the Agent.'
"$agent_path"
result=$?
printf '\nAgent exited with code %s. This window now provides a Bash shell.\n' "$result"
echo 'To restart, run the Agent command again. To stop the window, exit this shell.'
exec bash -i

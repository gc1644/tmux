#!/usr/bin/env bash

SESSION="main"

tmux kill-session -t $SESSION 2>/dev/null || true

tmux new-session -d -s $SESSION -n "shell" "/bin/update.sh"

tmux new-window -t $SESSION:2 -n "nvim"
tmux send-keys -t $SESSION:2 "nvim" C-m

tmux new-window -t $SESSION:3 -n "remote"
tmux send-keys -t $SESSION:3 "ssh root@"

tmux select-window -t $SESSION:1

tmux attach-session -t $SESSION

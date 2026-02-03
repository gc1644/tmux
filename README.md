user@local ~ $ tmux
───────────────────────────────────────────────────────────────────────────────────────────────
│ [0] user@server1:~/projects   │ top - 14:37:22 up 42 days,  3:12,  3 users,  load average: 0.42 │
│ user@server1$                 │ Tasks: 187 total,   1 running, 186 sleeping,   0 stopped,   0 zombie │
│ > vim src/main.go             │ %Cpu(s):  3.2 us,  1.1 sy,  0.0 ni, 95.4 id,  0.3 wa,  0.0 hi,  0.0 si │
│ package main                  │ MiB Mem :  32000.0 total,   4200.0 free,  15800.0 used,  12000.0 buff/cache │
│ import "fmt"                  │ MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.  14800.0 avail Mem  │
│ func main() {                 │   PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND     │
│     fmt.Println("hacker")     │  1234 user     20   0  2.3Gi  1.1Gi  420k S   4.2   3.5   12:34.56 node       │
│ }                             │  5678 user     20   0  1.8Gi  890Mi  310k S   2.1   2.8    8:12.90 python     │
│                               └───────────────────────────────────────────────────────────────┘
│ tail -f /var/log/nginx/access.log                                                            │
│ 192.168.1.77 - - [03/Feb/2026:14:37:10 +0000] "GET /api/v1/users HTTP/2" 200 142 "-" "curl/8.5.0" │
│ 45.79.123.45 - - [03/Feb/2026:14:37:11 +0000] "POST /deploy HTTP/1.1" 201 89 "-" "GitHub-Hookshot" │
───────────────────────────────────────────────────────────────────────────────────────────────
Status line: [main] 0: bash  1: ssh user@prod-server  2: htop  3: logs

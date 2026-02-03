───────────────────────────────────────────────────────────────────────────────────────────────
│ nvim main.go                  │ ssh user@prod-server.example.com                                 │
│ package main                  │ user@prod:~$ htop                                                    │
│ import "fmt"                  │ Tasks: 187 total,   1 running...                                     │
│ func main() {                 │ %Cpu(s):  3.2 us, 95.4 id...                                         │
│     fmt.Println("1337")       │ PID USER %CPU MEM ...                                                │
│ }                             │                                                                      │
├───────────────────────────────┼──────────────────────────────────────┤
│ tail -f /var/log/nginx.log    │ Monitoring pane – watching metrics                                   │
│ 8.8.8.8 GET /api 200      │                                                                      │
───────────────────────────────────────────────────────────────────────────────────────────────
[0] 0:nvim  1:ssh  2:htop  3:logs

#!/usr/bin/env python3
"""
GitHub Achievements Hunter & Automation Suite
Dibuat khusus untuk akun lordbarry21 buat unlock & naikin tier achievement GitHub.
"""

import subprocess
import json
import sys
import time

REPO_NAME = "lordbarry21/github-achievements-lab"

def run_cmd(cmd, cwd=None):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd, check=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"[Error] Command failed: {cmd}\nOutput: {e.stderr.strip()}", file=sys.stderr)
        return None

def trigger_quickdraw():
    print("\n[🎯] Triggering Quickdraw Achievement...")
    print("    Syarat: Buka issue lalu close dalam < 5 menit.")
    timestamp = int(time.time())
    title = f"Quickdraw Badge Trigger #{timestamp}"
    body = "Automated quick issue creation and immediate closure."
    
    issue_url = run_cmd(f'gh issue create --repo {REPO_NAME} --title "{title}" --body "{body}"')
    if issue_url:
        print(f"    Issue dibuat: {issue_url}")
        time.sleep(2)
        close_res = run_cmd(f'gh issue close "{issue_url}" --repo {REPO_NAME} --reason "completed"')
        print(f"    Issue berhasil di-close! ({close_res})")
        print("    ✅ Quickdraw triggered!")
    else:
        print("    ❌ Gagal membuat issue.")

def trigger_pair_extraordinaire():
    print("\n[🎯] Triggering Pair Extraordinaire Achievement...")
    print("    Syarat: Merge PR dengan commit yang memiliki co-author (Co-authored-by).")
    timestamp = int(time.time())
    branch = f"feature/pair-collab-{timestamp}"
    
    # Git operations
    run_cmd("git checkout main")
    run_cmd("git pull origin main")
    run_cmd(f"git checkout -b {branch}")
    
    # Modify file
    filename = f"pair_collab_{timestamp}.txt"
    with open(filename, "w") as f:
        f.write(f"Pair programming test at {time.ctime()}\nCo-authored with @octocat\n")
    
    run_cmd(f"git add {filename}")
    commit_msg = f"""feat: collaborative contribution #{timestamp}

Co-authored-by: The Octocat <583231+octocat@users.noreply.github.com>
Co-authored-by: The Octocat <octocat@users.noreply.github.com>"""
    
    run_cmd(f'git commit -m "{commit_msg}"')
    run_cmd(f"git push origin {branch}")
    
    # Create PR
    pr_url = run_cmd(f'gh pr create --repo {REPO_NAME} --title "feat: pair programming #{timestamp}" --body "Automated PR with co-authored commit" --base main --head {branch}')
    if pr_url:
        print(f"    PR dibuat: {pr_url}")
        time.sleep(2)
        merge_res = run_cmd(f'gh pr merge "{pr_url}" --merge --delete-branch')
        print(f"    PR berhasil di-merge! ({merge_res})")
        print("    ✅ Pair Extraordinaire triggered!")
    else:
        print("    ❌ Gagal membuat PR.")

def boost_pull_shark(count=2):
    print(f"\n[🎯] Boosting Pull Shark Tier (+{count} Merged PRs)...")
    print("    Syarat: Setiap merged PR menambah progres Pull Shark (Tier Bronze = 16, Silver = 128).")
    for i in range(count):
        timestamp = int(time.time()) + i
        branch = f"shark-boost-{timestamp}"
        print(f"    [{i+1}/{count}] Processing PR branch {branch}...")
        run_cmd("git checkout main")
        run_cmd("git pull origin main")
        run_cmd(f"git checkout -b {branch}")
        
        fname = f"shark_log_{timestamp}.txt"
        with open(fname, "w") as f:
            f.write(f"Pull Shark boost log entry #{i+1} at {time.ctime()}\n")
            
        run_cmd(f"git add {fname}")
        run_cmd(f'git commit -m "chore(shark): boost merged PR count #{timestamp}"')
        run_cmd(f"git push origin {branch}")
        
        pr_url = run_cmd(f'gh pr create --repo {REPO_NAME} --title "chore: shark boost #{timestamp}" --body "Auto boost PR for Pull Shark tier" --base main --head {branch}')
        if pr_url:
            time.sleep(2)
            run_cmd(f'gh pr merge "{pr_url}" --merge --delete-branch')
            print(f"    ✅ Merged PR #{i+1}: {pr_url}")
        time.sleep(2)

def show_summary():
    print("=" * 60)
    print("🏆 GITHUB ACHIEVEMENTS STATUS & CHEAT SHEET")
    print("=" * 60)
    print("1. 🦈 Pull Shark (Bronze/Silver/Gold):")
    print("   Status: SUDAH ADA (Bisa di-boost tier-nya dengan nambah merged PR)")
    print("2. 🚀 YOLO:")
    print("   Status: SUDAH ADA (Merge PR tanpa review)")
    print("3. 🤠 Quickdraw:")
    print("   Status: SIAP UNLOCK (Tutup issue/PR dalam < 5 menit)")
    print("4. 👯 Pair Extraordinaire:")
    print("   Status: SIAP UNLOCK (Merge PR dengan co-authored commit)")
    print("5. 🧠 Galaxy Brain:")
    print("   Status: Perlu 2 jawaban lu di-accept di GitHub Discussions orang lain / akun kedua.")
    print("6. 🌟 Starstruck:")
    print("   Status: Perlu 16 stars di salah satu repo publik lu.")
    print("7. 💖 Public Sponsor:")
    print("   Status: Perlu sponsorin developer via GitHub Sponsors ($1+).")
    print("=" * 60)

if __name__ == "__main__":
    show_summary()
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "quickdraw":
            trigger_quickdraw()
        elif cmd == "pair":
            trigger_pair_extraordinaire()
        elif cmd == "shark":
            n = int(sys.argv[2]) if len(sys.argv) > 2 else 2
            boost_pull_shark(n)
        elif cmd == "all":
            trigger_quickdraw()
            trigger_pair_extraordinaire()
    else:
        print("\nCara penggunaan:")
        print("  python hunter.py quickdraw   # Unlock badge Quickdraw")
        print("  python hunter.py pair        # Unlock badge Pair Extraordinaire")
        print("  python hunter.py shark 3     # Boost Pull Shark (merge 3 PRs)")
        print("  python hunter.py all         # Jalankan semua trigger otomatis")

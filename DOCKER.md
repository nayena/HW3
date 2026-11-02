# Setting Up Your Development Environment (Docker)

Every assignment in this course runs inside a **container**: a small Linux
computer, defined by this repository, that runs on top of your own machine. It
has the exact versions of Python, pytest, Hypothesis, mutmut, and ruff that
GitHub Actions and Gradescope use. If a check passes in your container, it will
pass there too, whether your laptop runs macOS, Windows, or Linux.

You only need to do this setup **once** for the semester. If you already set it up
for HW1, skip to [Step 3](#step-3-open-the-assignment-in-the-container); the
first time you open HW3, VS Code downloads its image.

**You do not need a Docker account.** Docker Desktop may ask you to sign in.
Skip it. Everything in this course works without signing in. You *do* need
the GitHub account you're already using for this course.

**Recommended: [Docker Desktop + VS Code](#recommended-docker-desktop--vs-code)** on
your own computer. It takes about 20 minutes to set up once, works offline, and you'll
use it for the rest of the semester.

**Fallback: [GitHub Codespaces](#fallback-github-codespaces-no-install)**, the same
container running in your browser. Use it if Docker won't run on your computer
(for example, an older laptop, very little free disk space, or virtualization
you can't enable), or to keep working while you sort out a Docker problem. If
you end up needing it, let course staff know what went wrong so we can help. Codespaces
is free up to a monthly usage limit on your GitHub account, and requires an internet
connection.

Your code lives in your GitHub repository either way, so you can switch at any
time. **Don't let setup problems stop you from starting the assignment.**

---

## Recommended: Docker Desktop + VS Code

### Step 1: Install Docker Desktop

Download Docker Desktop from **<https://www.docker.com/products/docker-desktop/>**.
Docker Desktop is free for students and educational use.

<details>
<summary><b>macOS</b></summary>

1. Choose the download that matches your Mac: **Apple Silicon** (M1/M2/M3/M4…)
   or **Intel**. Not sure? Apple menu → **About This Mac** → look at "Chip".
2. Open the `.dmg` and drag Docker into Applications.
3. Open Docker from Applications. Accept the license agreement and use the
   **recommended settings**. It may ask for your Mac password.
4. When asked to sign in, choose **Skip** / **Continue without signing in**. You
   can also skip the survey.
</details>

<details>
<summary><b>Windows</b></summary>

Requires Windows 10 (22H2 or later) or Windows 11.

1. Run the installer. Leave **"Use WSL 2 instead of Hyper-V"** checked.
2. Restart your computer when it asks.
3. Open Docker Desktop from the Start menu. Accept the license agreement.
4. When asked to sign in, choose **Skip** / **Continue without signing in**. You
   can also skip the survey.
5. If Docker says **WSL needs updating**, open PowerShell and run `wsl --update`,
   then restart Docker Desktop.
6. If Docker says **virtualization is disabled**, it has to be turned on in
   your computer's BIOS/UEFI settings. Search "enable virtualization" plus your
   laptop's brand for instructions, or use the Codespaces fallback for now and ask course staff.
</details>

<details>
<summary><b>Linux</b></summary>

Install **Docker Engine** for your distribution:
<https://docs.docker.com/engine/install/>. Then let your user run Docker without
`sudo`:

```bash
sudo usermod -aG docker "$USER"
```

Log out and back in for that to take effect. (Docker Desktop for Linux also
works, but isn't required.)
</details>

**Check that Docker works.** Docker Desktop must be running (whale icon in your
menu bar / system tray). Then, in a terminal (Terminal on macOS, PowerShell on Windows):

```bash
docker run --rm hello-world
```

You should see `Hello from Docker!`. If you get an error, see
[Troubleshooting](#troubleshooting).

### Step 2: Install VS Code and the Dev Containers extension

1. Install **Visual Studio Code**: <https://code.visualstudio.com/>
2. Open VS Code, go to the Extensions panel (the four-squares icon on the left), search
   for **Dev Containers** (published by Microsoft), and click **Install**.

### Step 3: Open the assignment in the container

1. Clone your own HW3 repository (see *Getting your repository* in README.md) and open the folder in VS Code
   (**File → Open Folder…**).
2. VS Code will pop up *"Folder contains a Dev Container configuration file."*
   Click **Reopen in Container**.
   (Missed it? Press `Ctrl+Shift+P` / `Cmd+Shift+P` and run
   **Dev Containers: Reopen in Container**.)
3. The first time, VS Code downloads the course image (about 1 GB; allow a few
   minutes on campus Wi-Fi). After that it opens in seconds.
4. Open a terminal inside VS Code (**Terminal → New Terminal**). The prompt
   should look something like `vscode ➜ /workspaces/hw3 (main) $`. That
   means you're inside the container. Check:
   ```bash
   make help
   search --help
   mutmut --version
   ```

**Things to know:**
- Your files live on your own computer. The container just works on
  them. Editing, saving, and `git` all work normally from VS Code.
- Run all course commands (`make ...`, `search ...`, `python`, ...) in the VS Code
  terminal **inside the container**, not in a separate terminal on your computer.
- To go back to working outside the container: `Ctrl+Shift+P` / `Cmd+Shift+P` →
  **Dev Containers: Reopen Folder Locally**.

<details>
<summary><b>Not using VS Code?</b> (plain Docker command line)</summary>

From your repository folder, start a shell in the course image:

```bash
# macOS / Linux
docker run --rm -it -v "$PWD":/workspaces/hw3 -w /workspaces/hw3 \
    -e PYTHONPATH=/workspaces/hw3/src ghcr.io/brandeis-cosi-106b/hw3-fa26:latest bash

# Windows PowerShell
docker run --rm -it -v "${PWD}:/workspaces/hw3" -w /workspaces/hw3 `
    -e PYTHONPATH=/workspaces/hw3/src ghcr.io/brandeis-cosi-106b/hw3-fa26:latest bash
```

Then use `make ...`, `search ...`, etc. as normal. Edit files with any editor on your own computer. Run `git` from your own computer
too (the container doesn't have your GitHub login). Type `exit` to leave;
`--rm` deletes the container but **not** your files.
</details>

---

## Fallback: GitHub Codespaces (no install)

1. Open **your** HW3 repository on GitHub.
2. Click the green **Code** button → **Codespaces** tab → **Create codespace on main**.
3. Wait for VS Code to open in your browser and the terminal at the bottom to
   finish setting up (a minute or two the first time).
4. In the terminal, check that everything works:
   ```bash
   make help
   search --help
   mutmut --version
   ```

**Things to know:**
- Commit and push your work regularly (the **Source Control** panel on the left,
  or `git` in the terminal). A codespace you haven't used for a while is
  eventually deleted, and anything not pushed is lost with it.
- Codespaces stop automatically after 30 minutes of inactivity. Stopped
  codespaces don't use up your monthly allowance, but their storage does, so delete
  old ones at <https://github.com/codespaces> when you're done with an assignment.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `Cannot connect to the Docker daemon` / `docker: command not found` | Docker Desktop isn't running. Start it, wait for the whale icon to stop animating, and try again. On Linux: `sudo systemctl start docker`. |
| `permission denied ... docker.sock` (Linux) | You skipped the `usermod` step, or haven't logged out and back in since. |
| Docker Desktop asks you to sign in | Skip it. No account is needed. |
| Pulling the image asks for a username/password | You shouldn't need to log in to download the course image. Run `docker logout ghcr.io` and try again. If it still asks, tell course staff. |
| `$'\r': command not found` or `/bin/bash^M: bad interpreter` | Windows line endings got into a file. In the container, run `git add --renormalize . && git status`, or re-clone the repository. |
| Everything is very slow on Windows | Files on the Windows side of a WSL container are slower to access. It's usually fine for this assignment, but if it's painfully slow, use the Codespaces fallback, or clone the repository inside WSL (`wsl` in PowerShell, then `git clone` there and `code .`). |
| Docker is using a lot of disk space | Docker Desktop → **Troubleshoot** / settings → **Clean / Purge data**, or run `docker system prune`. You'll re-download the course image next time. |
| Anything else | Switch to the Codespaces fallback so you're not blocked, and post the full error message (text, not a screenshot) on the course forum. |

---

## What's actually in here? (optional reading)

- [`.devcontainer/Dockerfile`](.devcontainer/Dockerfile) describes the image:
  an Ubuntu 22.04 base plus the tools installed by
  [`.devcontainer/install-tools.sh`](.devcontainer/install-tools.sh), and the Python
  packages at the versions pinned in [`uv.lock`](uv.lock).
- [`.devcontainer/devcontainer.json`](.devcontainer/devcontainer.json) tells VS
  Code and Codespaces which image to use.
- [`.github/workflows/ci.yml`](.github/workflows/ci.yml) runs your CI jobs inside
  that same image. The Gradescope autograder installs the same tools with the
  same `install-tools.sh`.

This is one more example of the course theme of *contracts*: the image is an agreement
between you, CI, and the grader about what "the environment" means.

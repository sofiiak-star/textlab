# Optional steps 3 and 4

These are inactive examples. They are not a deployed workflow or a tested
container. First finish local analysis and the Sphinx exercises.

## 3. GitHub Pages

1. Publish this repository to your GitHub account (not performed by this starter).
2. In Settings > Pages choose GitHub Actions as the source.
3. Copy `next_steps/docs.yml` to `.github/workflows/docs.yml`.
4. Commit and push the file. Open Actions > Documentation.
5. The build job installs Sphinx and creates HTML. The deploy job publishes
   the uploaded Pages artifact after a successful build on main.
6. On pull requests only the documentation build runs; deployment is skipped.
7. Follow the URL returned by the deploy job. Check navigation and one changed
   sentence. A green build alone does not prove the correct content is live.

`contents: read` permits checkout. `pages: write` and `id-token: write` are
limited to the deploy job. `needs: build` prevents deployment after a failed
build. `environment` associates the deployment with github-pages.
The moving action major tags are simple classroom examples, not immutable pins.

Official guide: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## 4. Docker (PowerShell commands)

Check `docker version`: both Client and Server must respond. Start your
installed container runtime if Server is unavailable. Use Linux containers.

```powershell
Copy-Item next_steps/Dockerfile Dockerfile
Copy-Item next_steps/.dockerignore .dockerignore
docker build -t textlab:local .
docker run --rm textlab:local
New-Item -ItemType Directory -Force results | Out-Null
$resultsPath = (Resolve-Path results).Path
docker run --rm --mount "type=bind,source=$resultsPath,target=/app/results" textlab:local python analyze.py documents/flask.md --output results/flask.json
```

The first run prints help. The second uses the document copied into the image
and writes JSON to the mounted host directory. `--rm` removes the stopped
container, not the host result. Use PowerShell here: Git Bash may rewrite
Linux-style container paths.

To use a changed host document without rebuilding the image, also mount the
host `documents` directory at `/app/documents` (prefer readonly). Without that
mount, the container sees the snapshot from image build time.

No published ports are needed: this program writes a file and exits.
Docker isolates the execution environment; it does not itself make input data,
floating base-image tags or dependency versions immutable.

Official guide: https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/

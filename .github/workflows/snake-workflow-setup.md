> Copy this file to `.github/workflows/snake.yml` in your `BlackBeanEagles/BlackBeanEagles` repo.
> It regenerates the contribution snake daily onto an `output` branch (referenced by the README).

```yaml
name: Generate contribution snake

on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:
  push:
    branches: [main]

permissions:
  contents: write

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: Platane/snk@v3
        with:
          github_user_name: BlackBeanEagles
          outputs: |
            dist/github-snake.svg?palette=github-dark&color_snake=#FF006E&color_dots=#161b22,#8338EC,#a855f7,#FF006E,#FFBE0B
      - uses: crazy-max/ghaction-github-pages@v4
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

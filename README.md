# GitHub Action: Supported distribution release matrix generator

Generate a GitHub Action matrix for all supported releases of Debian/Ubuntu.

## Inputs

| Variable               | Default           | Description |
| ---------------------- | ----------------- | ----------- |
| `distros`              | `"debian,ubuntu"` | Comma-separated list of distros to include in the matrix |
| `include-lts`          | `true`            | Set to true if distro release still supported by LTS should be included |
| `include-extended-lts` | `false`           | Set to true if distro release still supported by extended LTS should be included |

## Usage

Here is a basic example showing how to generate a dynamic matrix and use it to run a number of docker containers on different releases:

```yaml
---
name: Tests

on:
  pull_request:
    branches:
      - main

jobs:
  generate-matrix:
    name: Generate matrix
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.generate-matrix.outputs.matrix }}
    steps:
      - name: Generate matrix
        id: generate-matrix
        uses: wanduow/action-supported-distro-releases@v1

  test:
    name: Run tests
    runs-on: ubuntu-latest
    needs: generate-matrix
    container:
      image: ${{ matrix.target }}
    strategy:
      matrix:
        target: ${{ fromJson(needs.generate-matrix.outputs.matrix) }}
    steps:
      - name: Debug
        run: |
          . /etc/os-release
          echo "Hello from ${PRETTY_NAME}"
```

An example of providing configuration to this action (e.g excluding releases which have reached EOL but still under LTS support), would look like this:

```yaml
jobs:
  generate-matrix:
    name: Generate matrix
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.generate-matrix.outputs.matrix }}
    steps:
      - name: Generate matrix
        id: generate-matrix
        uses: wanduow/action-supported-distro-releases@v1
        with:
          include-lts: false
```

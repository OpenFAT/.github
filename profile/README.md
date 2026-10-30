Open-source Fast Analog Tooling (Open-FAT) for analog and mixed-signal IC design, from schematic to sign-off, trying to automate as much as possible, while giving you full controls over every tool with plugins.

OpenFAT covers the steps of an analog design one tool at a time:
- schematic capture in **Schemify**
- SPICE simulation in **EGSpice**, with device models written in Verilog-A and compiled by **VerA**
- layout from a netlist in **Philis**
- DRC, LVS, ERC and PEX in **GPurify**

Each tool also works on its own beside the tools you already use. Schemify writes netlists for ngspice, Xyce, LTspice and HSPICE, and its Interoperate plugin moves designs to and from Cadence Virtuoso and xschem.

```mermaid
flowchart LR
  T["AMTemplate<br/>project template"] --> S["Schemify<br/>schematic"]
  S -->|netlist| E["EGSpice<br/>simulation"]
  V["VerA<br/>Verilog-A models"] --> E
  S -->|netlist| P["Philis<br/>layout"]
  P -->|GDS| G["GPurify<br/>DRC · LVS · PEX"]
```

## Try it

These commands need [Nix](https://nixos.org/download/) or a Linux or macOS shell:

```sh
# Draw: open a cell in the schematic editor
nix run 'github:OpenFAT/Schemify#latest' -- path/to/cell.shcomp

# Simulate a SPICE deck (built from source), or install the release binary
nix run github:OpenFAT/EGSpice -- deck.sp
curl -fsSL https://raw.githubusercontent.com/OpenFAT/EGSpice/main/tools/install.sh | sh
```

To start a whole chip or block, create a repository from [AMTemplate](https://github.com/OpenFAT/AMTemplate) (**Use this template**), then run `make -C .flows CreateProject PROJECT_NAME=my_chip PROJECT_TYPE=mixed`.

## Projects

These tools are young and move quickly. The chart shows how much of each project's tracked work is done and how active it has been lately. A daily job updates it.

<!-- status:start -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="status-dark.svg">
  <img src="status-light.svg" alt="Project status: issues closed and open, and commits per week, for each OpenFAT project. The table below lists the same projects.">
</picture>

| Stage | Project | What it does | Status |
|---|---|---|---|
| Start a project | [AMTemplate](https://github.com/OpenFAT/AMTemplate) | Template for analog and mixed-signal ASIC design on open-source tools | [![CI](https://github.com/OpenFAT/AMTemplate/actions/workflows/ci.yaml/badge.svg)](https://github.com/OpenFAT/AMTemplate/actions/workflows/ci.yaml) ![last commit](https://img.shields.io/github/last-commit/OpenFAT/AMTemplate?label=last%20commit) |
| Schematic | [Schemify](https://github.com/OpenFAT/Schemify) | Schematic Editor, made to be lightweight and plugin-friendly just like vim and vim-plug | [![CI](https://github.com/OpenFAT/Schemify/actions/workflows/ci.yml/badge.svg)](https://github.com/OpenFAT/Schemify/actions/workflows/ci.yml) [![release](https://img.shields.io/github/v/release/OpenFAT/Schemify?label=release)](https://github.com/OpenFAT/Schemify/releases/latest) ![last commit](https://img.shields.io/github/last-commit/OpenFAT/Schemify?label=last%20commit) |
| Schematic | [Interoperate](https://github.com/OpenFAT/Interoperate) | Schemify's Import/Export working with other Schematic Editors so you can use it interchangeably | [![CI](https://github.com/OpenFAT/Interoperate/actions/workflows/ci.yml/badge.svg)](https://github.com/OpenFAT/Interoperate/actions/workflows/ci.yml) ![last commit](https://img.shields.io/github/last-commit/OpenFAT/Interoperate?label=last%20commit) |
| Schematic | [cktImg](https://github.com/OpenFAT/cktImg) | A netlist -> Img tool, agnostic backend (latex, C-ABI) | [![CI](https://github.com/OpenFAT/cktImg/actions/workflows/ci.yml/badge.svg)](https://github.com/OpenFAT/cktImg/actions/workflows/ci.yml) [![release](https://img.shields.io/github/v/release/OpenFAT/cktImg?label=release)](https://github.com/OpenFAT/cktImg/releases/latest) ![last commit](https://img.shields.io/github/last-commit/OpenFAT/cktImg?label=last%20commit) |
| Schematic | [PDK-Manager](https://github.com/OpenFAT/PDK-Manager) | Interface to allow easy usage of PDKs (open-source and propietary over ssh) | [![CI](https://github.com/OpenFAT/PDK-Manager/actions/workflows/ci.yml/badge.svg)](https://github.com/OpenFAT/PDK-Manager/actions/workflows/ci.yml) ![last commit](https://img.shields.io/github/last-commit/OpenFAT/PDK-Manager?label=last%20commit) |
| Schematic | [GmId-Visualizer](https://github.com/OpenFAT/GmId-Visualizer) | A Gm/Id visualizer written in C++ | [![CI](https://github.com/OpenFAT/GmId-Visualizer/actions/workflows/ci.yml/badge.svg)](https://github.com/OpenFAT/GmId-Visualizer/actions/workflows/ci.yml) ![last commit](https://img.shields.io/github/last-commit/OpenFAT/GmId-Visualizer?label=last%20commit) |
| Schematic | [Schemify-Themes](https://github.com/OpenFAT/Schemify-Themes) | spicetify's theme catalogue for Schemify: 16 themes, 115 colour schemes, View → Themes | [![CI](https://github.com/OpenFAT/Schemify-Themes/actions/workflows/gate.yaml/badge.svg)](https://github.com/OpenFAT/Schemify-Themes/actions/workflows/gate.yaml) ![last commit](https://img.shields.io/github/last-commit/OpenFAT/Schemify-Themes?label=last%20commit) |
| Simulation | [EGSpice](https://github.com/OpenFAT/EGSpice) | Fast Spice Simulations, with Verilog-AMS support using VerA | [![CI](https://github.com/OpenFAT/EGSpice/actions/workflows/test.yml/badge.svg)](https://github.com/OpenFAT/EGSpice/actions/workflows/test.yml) ![last commit](https://img.shields.io/github/last-commit/OpenFAT/EGSpice?label=last%20commit) |
| Simulation | [VerA](https://github.com/OpenFAT/VerA) | A Verilog-AMS Compiler with SIMD and GPU support as first-class residents | [![CI](https://github.com/OpenFAT/VerA/actions/workflows/test.yaml/badge.svg)](https://github.com/OpenFAT/VerA/actions/workflows/test.yaml) [![release](https://img.shields.io/github/v/release/OpenFAT/VerA?label=release)](https://github.com/OpenFAT/VerA/releases/latest) ![last commit](https://img.shields.io/github/last-commit/OpenFAT/VerA?label=last%20commit) |
| Simulation | [SpiceRack](https://github.com/OpenFAT/SpiceRack) | A Spice Interface in Python that has universal syntax, emits any SPICE backend of the user's choice | [![CI](https://github.com/OpenFAT/SpiceRack/actions/workflows/test.yaml/badge.svg)](https://github.com/OpenFAT/SpiceRack/actions/workflows/test.yaml) ![last commit](https://img.shields.io/github/last-commit/OpenFAT/SpiceRack?label=last%20commit) |
| Layout | [Philis](https://github.com/OpenFAT/Philis) | Automated ANalog P&R Engine that doesn't use ML | [![CI](https://github.com/OpenFAT/Philis/actions/workflows/ci.yml/badge.svg)](https://github.com/OpenFAT/Philis/actions/workflows/ci.yml) ![last commit](https://img.shields.io/github/last-commit/OpenFAT/Philis?label=last%20commit) |
| Layout | [GPurify](https://github.com/OpenFAT/GPurify) | A SIMD-First DRC, ERC, LVS, PEX engine, built for better checks than propietary work | [![CI](https://github.com/OpenFAT/GPurify/actions/workflows/test.yml/badge.svg)](https://github.com/OpenFAT/GPurify/actions/workflows/test.yml) ![last commit](https://img.shields.io/github/last-commit/OpenFAT/GPurify?label=last%20commit) |
| Verification | [VAMS-Conformance-Suite](https://github.com/OpenFAT/VAMS-Conformance-Suite) | A conformance suite for Verilog-AMS (Containing Verilog-A & IEEE 1364 specifics) | [![CI](https://github.com/OpenFAT/VAMS-Conformance-Suite/actions/workflows/conformance.yml/badge.svg)](https://github.com/OpenFAT/VAMS-Conformance-Suite/actions/workflows/conformance.yml) ![last commit](https://img.shields.io/github/last-commit/OpenFAT/VAMS-Conformance-Suite?label=last%20commit) |
<!-- status:end -->

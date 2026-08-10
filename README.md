# Manufacturing AI

Manufacturing AI is a reusable Codex skill for planning, troubleshooting, and validating physical fabrication from the first idea through an inspected and approved part.

Its primary focus is practical 3D-printing work: model preparation, STL and 3MF review, material selection, slicing strategy, dimensional fit, embedded hardware, calibration, failure recovery, small-batch production, and physical quality control. It can also help choose when resin printing, CNC, laser cutting, molding, assembly, or outsourcing is a better process.

The skill treats a valid model, successful slice, accepted printer job, completed print, physical fit, and final approval as separate evidence gates.

## Install with Codex

Ask Codex to install the skill from this repository:

```text
$skill-installer Install the skill from https://github.com/J-D11/manufacturing-ai/tree/main/skills/manufacturing-ai
```

Codex detects newly installed skills automatically. Restart Codex if it does not appear immediately.

For manual installation, copy `skills/manufacturing-ai` into:

```text
~/.agents/skills/manufacturing-ai
```

Invoke it explicitly with `$manufacturing-ai`, or let Codex select it when your request matches its description.

## Example prompts

```text
Use $manufacturing-ai to review this 3MF before I print it and tell me what evidence is still missing.
```

```text
Use $manufacturing-ai to design the smallest fit test for an NFC-tag pocket before I print the complete part.
```

```text
Use $manufacturing-ai to diagnose this failed PETG print from the model, slicer screenshots, settings, and photos.
```

```text
Use $manufacturing-ai to plan a repeatable 20-part FDM production run with inspection criteria.
```

## What is included

- `SKILL.md`: the core manufacturing workflow, evidence gates, routing, and safety constraints.
- `references/`: focused guidance for process selection, DFM, file formats, materials, slicing, calibration, testing, failures, quality control, and production planning.
- `templates/`: reusable project, test, inspection, production, and specialist-handoff records.
- `agents/openai.yaml`: Codex display metadata and default prompt.

## Optional Bambu companion

When `$bambu-3d-print-troubleshooter` is installed, Manufacturing AI can delegate narrow Bambu Studio, printer, AMS, connectivity, and machine-maintenance diagnosis to it while retaining ownership of the overall manufacturing project. Manufacturing AI remains usable without that companion skill and will state the missing specialist boundary when machine-specific verification is unavailable.

## Safety and proof limits

This skill provides workflow guidance, not engineering certification. Verify current manufacturer guidance before version-sensitive machine work or disassembly. Do not approve safety-critical, structural, food-contact, medical, child-safety, fire-safety, or vehicle components without appropriate material, process, and engineering evidence.

## Contributing

Issues and pull requests are welcome. Keep contributions focused, preserve the distinction between digital preparation and physical proof, and avoid claims about tools or machines that have not been verified.

## License

MIT. See `LICENSE`.

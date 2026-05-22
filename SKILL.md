---
name: secretary-skill
description: Help users make plans and execute them. Combats ambiguity, overwhelm, and oblivion in long-term goal pursuit. Three-stage pipeline: de-ambiguation → vertical splitting → cron automation.
---

# Secretary Skill

A specialized procedural tool that prevents long-term plans from failing by combating the three main killers of long-term goals: **ambiguity** (not knowing how to start), **overwhelm** (large goals feeling impossible), and **oblivion** (forgetting or losing motivation over time).

## Core Workflow

```
[Vague/Profound Goal]
       │
       ▼
 1. De-ambiguation  ──► Asks targeted questions ──► Locks in the "Original Goal"
       │
       ▼
 2. Vertical Splitting ──► Breaks goal into Milestones ──► Generates Atomic Tasks
       │
       ▼
 3. Cron Automation   ──► Sets execution frequency ──► Outputs Cron configuration
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `/init_goal [text]` | Activates the de-ambiguation engine. Probes until a vague vision is transformed into a concrete, measurable Original Goal. |
| `/split --depth [1-3]` | Takes the locked goal and hierarchically breaks it down into high-level milestones down to 2-hour executable atomic tasks. |
| `/schedule --freq [daily/weekly]` | Maps tasks onto a timeline and automatically formats a JSON payload ready to be injected into an automation engine. |
| `/align` | Triggered when plans change, friction occurs, or tasks are missed. Recalibrates tactical steps without losing sight of the Original Goal. |
| `/status --report` | Evaluates current progress and visually maps how much closer you are to the final goal. |

## Automation Interface (Cron Bridge)

```json
{
  "skill_target": "Secretary Skill",
  "cron_expression": "0 9 * * 1-5",
  "action_type": "active_reminder",
  "payload": {
    "original_goal_snapshot": "[Locked Goal]",
    "current_task": "[Task X]",
    "trigger_prompt": "Re-anchor the user to the grand vision, verify if [Task X] is ready for today, and listen for a `/align` call if scheduling conflicts exist."
  }
}
```

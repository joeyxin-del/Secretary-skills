"""
Secretary Skill Core Engine

The 3-Stage Pipeline:
  1. De-ambiguation — turn vague visions into concrete goals
  2. Vertical Splitting — break goals into milestones → atomic tasks
  3. Cron Automation — map tasks to a timeline and produce cron config
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


# ── Data Models ──────────────────────────────────────────────────────


@dataclass
class Goal:
    """A concrete, measurable goal locked by the de-ambiguation engine."""
    raw_text: str
    refined_statement: str
    success_criteria: list[str]
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Milestone:
    """A high-level milestone contributing to a Goal."""
    id: str
    title: str
    description: str
    deadline: Optional[str] = None
    tasks: list["AtomicTask"] = field(default_factory=list)


@dataclass
class AtomicTask:
    """A 2-hour executable atomic task."""
    id: str
    description: str
    duration_minutes: int = 120
    done: bool = False


# ── Stage 1: De-ambiguation ──────────────────────────────────────────


class DeambiguationEngine:
    """
    Probes the user with targeted questions until a vague vision
    is transformed into a concrete, measurable Original Goal.
    """

    PROBES = [
        "What does success look like when this is done?",
        "How will you measure progress?",
        "What's the first tangible outcome you expect?",
        "What's the deadline or time constraint?",
        "Who else is involved or affected?",
    ]

    def __init__(self):
        self.answers: dict[str, str] = {}

    def ask_next(self) -> Optional[str]:
        idx = len(self.answers)
        if idx >= len(self.PROBES):
            return None
        return self.PROBES[idx]

    def record_answer(self, question: str, answer: str):
        self.answers[question] = answer

    def lock_goal(self, raw_text: str) -> Goal:
        criteria = list(self.answers.values())
        deadline_q = "What's the deadline or time constraint?"
        refined = (
            f"{raw_text.strip().rstrip('.')}. "
            f"Deadline: {self.answers.get(deadline_q, 'TBD')}."
        )
        return Goal(
            raw_text=raw_text,
            refined_statement=refined,
            success_criteria=criteria,
        )


# ── Stage 2: Vertical Splitting ──────────────────────────────────────


class VerticalSplitter:
    """
    Takes a locked Goal and hierarchically breaks it down:
    Goal → Milestones → Atomic Tasks (2-hour executable units).
    """

    def __init__(self, goal: Goal, depth: int = 2):
        self.goal = goal
        self.depth = min(max(depth, 1), 3)  # clamp 1-3
        self.milestones: list[Milestone] = []

    def add_milestone(self, title: str, description: str,
                      deadline: Optional[str] = None) -> Milestone:
        ms = Milestone(
            id=f"ms-{len(self.milestones) + 1}",
            title=title,
            description=description,
            deadline=deadline,
        )
        self.milestones.append(ms)
        return ms

    def add_task(self, milestone_id: str, description: str,
                 duration: int = 120) -> Optional[AtomicTask]:
        for ms in self.milestones:
            if ms.id == milestone_id:
                task = AtomicTask(
                    id=f"{ms.id}-t{len(ms.tasks) + 1}",
                    description=description,
                    duration_minutes=duration,
                )
                ms.tasks.append(task)
                return task
        return None


# ── Stage 3: Cron Automation ─────────────────────────────────────────


@dataclass
class CronJob:
    """A scheduled job payload for the automation bridge."""
    skill_target: str = "Secretary Skill"
    cron_expression: str = ""
    action_type: str = "active_reminder"
    payload: dict = field(default_factory=dict)


class CronScheduler:
    """
    Maps tasks onto a timeline and formats JSON payloads
    ready for injection into an automation engine.
    """

    FREQ_MAP = {
        "daily": "0 9 * * 1-5",
        "weekly": "0 9 * * 1",
        "weekdays": "0 9 * * 1-5",
        "weekends": "0 9 * * 0,6",
    }

    def schedule(self, task: AtomicTask, freq: str = "daily",
                 goal_snapshot: str = "") -> CronJob:
        cron_expr = self.FREQ_MAP.get(freq, "0 9 * * 1-5")
        return CronJob(
            cron_expression=cron_expr,
            payload={
                "original_goal_snapshot": goal_snapshot,
                "current_task": task.description,
                "trigger_prompt": (
                    "Re-anchor the user to the grand vision, "
                    "verify if the current task is ready for today, "
                    "and listen for a `/align` call if scheduling "
                    "conflicts exist."
                ),
            },
        )

    def to_json(self, job: CronJob) -> dict:
        return {
            "skill_target": job.skill_target,
            "cron_expression": job.cron_expression,
            "action_type": job.action_type,
            "payload": job.payload,
        }

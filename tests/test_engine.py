"""Tests for the Secretary Skill core engine."""

from src.engine import (
    DeambiguationEngine,
    VerticalSplitter,
    CronScheduler,
    Goal,
)


class TestDeambiguationEngine:

    def test_probes_cycle(self):
        eng = DeambiguationEngine()
        assert eng.ask_next() is not None
        for _ in range(len(eng.PROBES)):
            eng.record_answer(eng.ask_next(), "some answer")
        assert eng.ask_next() is None

    def test_lock_goal(self):
        eng = DeambiguationEngine()
        eng.record_answer("How will you measure progress?", "finish 3 chapters")
        eng.record_answer("What does success look like when this is done?", "pass exam")
        goal = eng.lock_goal("learn Python")
        assert isinstance(goal, Goal)
        assert "learn Python" in goal.refined_statement
        assert "finish 3 chapters" in goal.success_criteria


class TestVerticalSplitter:

    def test_add_milestone(self):
        goal = Goal(raw_text="x", refined_statement="x", success_criteria=[])
        splitter = VerticalSplitter(goal)
        ms = splitter.add_milestone("Phase 1", "first phase", "2026-07-01")
        assert ms.id == "ms-1"
        assert ms.title == "Phase 1"
        assert len(splitter.milestones) == 1

    def test_add_task(self):
        goal = Goal(raw_text="x", refined_statement="x", success_criteria=[])
        splitter = VerticalSplitter(goal)
        ms = splitter.add_milestone("P1", "desc")
        t = splitter.add_task(ms.id, "do something", 60)
        assert t is not None
        assert t.id == "ms-1-t1"
        assert t.duration_minutes == 60

    def test_add_task_invalid_milestone(self):
        goal = Goal(raw_text="x", refined_statement="x", success_criteria=[])
        splitter = VerticalSplitter(goal)
        t = splitter.add_task("nonexistent", "task")
        assert t is None


class TestCronScheduler:

    def test_schedule(self):
        goal = Goal(raw_text="x", refined_statement="Learn Python", success_criteria=[])
        from src.engine import AtomicTask
        task = AtomicTask(id="t1", description="practice loops")
        scheduler = CronScheduler()
        job = scheduler.schedule(task, freq="daily",
                                 goal_snapshot=goal.refined_statement)
        assert job.cron_expression == "0 9 * * 1-5"
        assert job.payload["current_task"] == "practice loops"

    def test_to_json(self):
        scheduler = CronScheduler()
        from src.engine import AtomicTask
        job = scheduler.schedule(AtomicTask(id="t1", description="test"),
                                 goal_snapshot="g")
        data = scheduler.to_json(job)
        assert data["skill_target"] == "Secretary Skill"
        assert "cron_expression" in data

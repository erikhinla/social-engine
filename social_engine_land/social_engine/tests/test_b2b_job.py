"""B2B recognition-tier job sits alongside PROOF. PROOF path stays default."""

from __future__ import annotations

from app.b2b_review import mechanical_b2b_flags
from app.models import B2B_CTA_LINE, B2B_CTA_URL, CTA_LINE, CTA_URL, GrokCopyRequest
from app.prompts import B2B_SYSTEM_PROMPT, SYSTEM_PROMPT, build_messages, fake_copy
from tests.conftest import SECRET_HEADERS, approve_payload


B2B_BRIEF = {
    "job": "b2b",
    "department": "FIN",
    "moniker": "The Reconciliation Loop",
    "accent": "department accent",
    "scene_seed": "invoicing got faster, reconciliation still takes three days",
    "platform": "linkedin",
    "telegram_chat_id": "42",
}


def test_proof_job_is_default_and_keeps_locked_cta(harness):
    created = harness.client.post("/briefs", json={"brief": "handoffs still need a chaperone"})
    assert created.status_code == 200
    copy = created.json()["copy"]
    assert copy["job"] == "proof"
    assert CTA_LINE in copy["linkedin"]
    assert CTA_URL in copy["linkedin"]
    assert "Map Business Momentum" in copy["linkedin"]
    assert "/proof" in copy["linkedin"]
    assert B2B_CTA_LINE not in copy["linkedin"]
    assert "/bbai" not in copy["linkedin"]


def test_proof_build_messages_unchanged():
    messages = build_messages(GrokCopyRequest(brief="find the fog", mode="generate"))
    assert messages[0].content == SYSTEM_PROMPT
    assert "Write a fresh PROOF package" in messages[1].content
    assert "Map Business Momentum" in messages[1].content
    assert "https://transformby10x.ai/proof" in messages[1].content


def test_b2b_linkedin_uses_recognition_cta_not_proof(harness):
    created = harness.client.post("/briefs", json=B2B_BRIEF)
    assert created.status_code == 200
    copy = created.json()["copy"]
    assert copy["job"] == "b2b"
    assert copy["platform"] == "linkedin"
    assert copy["department"] == "FIN"
    post = copy["linkedin"]
    assert B2B_CTA_LINE in post
    assert post.strip().endswith(B2B_CTA_LINE)
    assert "Map Business Momentum" not in post
    assert "/proof" not in post
    assert CTA_LINE not in post
    assert post.count("(") == 1
    assert len(post.split()) <= 90
    assert copy["visual_prompt"]
    assert B2B_BRIEF["scene_seed"] in copy["visual_prompt"]
    assert "department accent" in copy["visual_prompt"]
    assert post not in copy["visual_prompt"]
    assert mechanical_b2b_flags(post, B2B_BRIEF["scene_seed"]) == []
    assert harness.telegram.messages
    preview = harness.telegram.messages[-1].text
    assert B2B_CTA_URL in preview
    assert "Map Business Momentum" not in preview
    assert "1. Explained." in preview
    assert harness.grok.calls[-1].job == "b2b"


def test_b2b_x_uses_beats_1_2_5_only(harness):
    payload = dict(B2B_BRIEF)
    payload["platform"] = "x"
    created = harness.client.post("/briefs", json=payload)
    assert created.status_code == 200
    copy = created.json()["copy"]
    post = "\n\n".join(copy["x"])
    assert copy["platform"] == "x"
    assert B2B_CTA_LINE in post
    assert post.strip().endswith(B2B_CTA_LINE)
    assert "A person in this department" not in post
    assert len(post.split()) <= 45
    assert "Map Business Momentum" not in post
    assert "/proof" not in post


def test_b2b_requires_brief_fields(harness):
    response = harness.client.post("/briefs", json={"job": "b2b", "brief": "missing the schema"})
    assert response.status_code == 422


def test_b2b_fake_path_does_not_break_proof_fake():
    proof = fake_copy(GrokCopyRequest(brief="the extra job", mode="generate"))
    assert proof.job == "proof"
    assert CTA_LINE in proof.linkedin
    b2b = fake_copy(
        GrokCopyRequest(
            brief=B2B_BRIEF["scene_seed"],
            job="b2b",
            department="FIN",
            scene_seed=B2B_BRIEF["scene_seed"],
            platform="linkedin",
        )
    )
    assert b2b.job == "b2b"
    assert B2B_CTA_LINE in b2b.linkedin
    assert CTA_LINE not in b2b.linkedin


def test_b2b_build_messages_uses_five_beat_prompt():
    messages = build_messages(
        GrokCopyRequest(
            brief=B2B_BRIEF["scene_seed"],
            job="b2b",
            department="FIN",
            moniker="The Reconciliation Loop",
            accent="department accent",
            scene_seed=B2B_BRIEF["scene_seed"],
            platform="linkedin",
        )
    )
    assert messages[0].content == B2B_SYSTEM_PROMPT
    assert messages[0].content != SYSTEM_PROMPT
    assert "There's a name for what's happening here." in messages[0].content
    assert "90 words" in messages[1].content
    assert "scene_seed: invoicing got faster, reconciliation still takes three days" in messages[1].content
    assert B2B_CTA_URL in messages[1].content


def test_b2b_mechanical_reject_flags():
    seed = "invoicing got faster, reconciliation still takes three days"
    good = (
        "Invoicing got faster.\n\n"
        "(Reconciliation still takes three days.)\n\n"
        "A person in this department now does the leftover work by hand.\n\n"
        f"{B2B_CTA_LINE}"
    )
    assert mechanical_b2b_flags(good, seed) == []
    leaked = good.replace(B2B_CTA_LINE, f"PROOF\n\n{B2B_CTA_LINE}")
    assert "6. Product leak." in mechanical_b2b_flags(leaked, seed)
    drifted = good.replace(B2B_CTA_LINE, "There's a name for this.")
    assert "8. Handoff drift." in mechanical_b2b_flags(drifted, seed)
    numbered = good.replace("Invoicing got faster.", "Invoicing got 40% faster.")
    assert "4. A number appeared." in mechanical_b2b_flags(numbered, seed)
    asked = good.replace(B2B_CTA_LINE, f"Want the name?\n\n{B2B_CTA_LINE}")
    assert "7. Question CTA." in mechanical_b2b_flags(asked, seed)


def test_b2b_approve_stages_only_selected_platform(harness):
    created = harness.client.post("/briefs", json=B2B_BRIEF).json()
    harness.client.post(
        "/telegram/webhook",
        headers=SECRET_HEADERS,
        json=approve_payload(88, created["draft_id"], created["version"]),
    )
    draft = harness.client.get(f"/drafts/{created['draft_id']}").json()
    assert draft["status"] == "staged"
    assert harness.postiz.called is True
    last = harness.postiz.last_create
    assert last is not None
    assert last.type == "draft"
    assert len(last.posts) == 1
    assert last.posts[0].settings.get("url") == B2B_CTA_URL
    assert B2B_CTA_LINE in last.posts[0].value[0].content
    assert "Map Business Momentum" not in last.posts[0].value[0].content

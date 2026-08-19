from strictproof.domain.models import ActionProposal, StateDocument
from strictproof.persistence.occ import OCCHandler


def make_proposal(agent_id: str, expected_version: int) -> ActionProposal:
    return ActionProposal(
        agent_id=agent_id,
        session_id=f"session-{agent_id}",
        action_type="MODIFY_CONFIG",
        target_resource="service/prod-api",
        desired_state={"public_access": False},
        state_id="state-prod-api",
        expected_state_version=expected_version,
        policy_id="test-policy",
        policy_version=1,
        rationale="Test state transition",
    )


def test_occ_accepts_current_version():
    occ = OCCHandler()

    occ._states["state-prod-api"] = StateDocument(
        state_id="state-prod-api",
        resource_id="service/prod-api",
        version=0,
        state_hash="",
        state={"public_access": True},
        policy_id="test-policy",
        updated_by="system",
    )

    proposal = make_proposal("agent-1", 0)
    result = occ.commit(proposal)

    assert result.committed is True
    assert result.observed_version == 0
    assert result.new_version == 1
    assert occ._states["state-prod-api"].version == 1


def test_occ_rejects_stale_version():
    occ = OCCHandler()

    occ._states["state-prod-api"] = StateDocument(
        state_id="state-prod-api",
        resource_id="service/prod-api",
        version=1,
        state_hash="mock_hash_1",
        state={"public_access": False},
        policy_id="test-policy",
        updated_by="agent-1",
    )

    stale_proposal = make_proposal("agent-2", 0)
    result = occ.commit(stale_proposal)

    assert result.committed is False
    assert result.observed_version == 1
    assert result.new_version == 1
    assert "Version mismatch" in result.error_message

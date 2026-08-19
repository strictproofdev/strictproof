from datetime import datetime, timezone
from typing import Any, Dict, Literal, Optional
from uuid import uuid4

from pydantic import BaseModel, Field, model_validator


class ReasonCode:
    IDENTITY_INVALID = "IDENTITY_INVALID"
    POLICY_DENIED = "POLICY_DENIED"
    STATE_NOT_FOUND = "STATE_NOT_FOUND"
    STATE_VERSION_MISMATCH = "STATE_VERSION_MISMATCH"
    RESOURCE_MISMATCH = "RESOURCE_MISMATCH"
    ACTION_NOT_PERMITTED = "ACTION_NOT_PERMITTED"
    POLICY_VERSION_MISMATCH = "POLICY_VERSION_MISMATCH"
    COMMIT_SUCCESS = "COMMIT_SUCCESS"
    TOOL_EXECUTION_FAILED = "TOOL_EXECUTION_FAILED"
    OCC_ABORTED = "OCC_ABORTED"
    TRANSACTION_FAILED = "TRANSACTION_FAILED"


class ActionProposal(BaseModel):
    proposal_id: str = Field(default_factory=lambda: str(uuid4()))
    agent_id: str
    session_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    action_type: str
    target_resource: str
    desired_state: Dict[str, Any]
    delta: Optional[Dict[str, Any]] = None
    state_id: str
    expected_state_version: int = Field(ge=0)
    policy_id: str
    policy_version: int = Field(ge=1)
    rationale: str
    evidence_uri: Optional[str] = None


class StateDocument(BaseModel):
    state_id: str
    resource_id: str
    version: int = Field(ge=0)
    state_hash: str
    state: Dict[str, Any]
    policy_id: str
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_by: str


class StateTransition(BaseModel):
    state_id: str
    from_version: int
    to_version: int
    previous_state_hash: str
    new_state_hash: str
    proposal_id: str
    committed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @model_validator(mode="after")
    def validate_version_increment(self):
        if self.to_version != self.from_version + 1:
            raise ValueError("to_version must equal from_version + 1")
        return self


class ExecutionStatus(BaseModel):
    attempted: bool = False
    status: Literal["NOT_EXECUTED", "SUCCEEDED", "FAILED"] = "NOT_EXECUTED"
    tool_name: Optional[str] = None
    error_code: Optional[str] = None


class StrictProofReceipt(BaseModel):
    receipt_id: str = Field(default_factory=lambda: str(uuid4()))
    receipt_type: Literal["ALLOW", "DENY"]
    issued_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    proposal_id: str
    agent_id: str
    target_resource: str
    action_type: str
    state_id: str
    expected_state_version: int
    observed_state_version: int
    policy_id: str
    policy_version: int
    identity_verified: bool
    authorization_granted: bool
    state_version_match: bool
    policy_compliant: bool
    verdict: Literal["COMMIT", "REJECT"]
    reason_code: str
    reason: str
    transition: Optional[StateTransition] = None
    execution: ExecutionStatus = Field(default_factory=ExecutionStatus)
    payload_hash: str
    signature: Optional[str] = None

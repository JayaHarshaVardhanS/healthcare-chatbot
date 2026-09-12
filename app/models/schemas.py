from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class LabValue(BaseModel):
    name: str
    value: float
    unit: str
    reference_range: Optional[str] = None


class ReportAnalysis(BaseModel):
    report_date: str
    conditions: List[str] = Field(default_factory=list)
    medications: List[str] = Field(default_factory=list)
    symptoms: List[str] = Field(default_factory=list)
    lab_values: List[LabValue] = Field(default_factory=list)
    important_findings: List[str] = Field(default_factory=list)


class HistoricalDocument(BaseModel):
    content: str
    metadata: Dict


class ComparisonFinding(BaseModel):
    parameter: str
    current_value: Optional[str] = None
    historical_value: Optional[str] = None
    trend: str
    explanation: str


class ComparisonResult(BaseModel):
    findings: List[ComparisonFinding] = Field(default_factory=list)
    overall_summary: str


class RecommendationResult(BaseModel):
    observations: List[str] = Field(default_factory=list)
    discussion_points: List[str] = Field(default_factory=list)
    general_guidance: List[str] = Field(default_factory=list)
    attention_items: List[str] = Field(default_factory=list)

    disclaimer: str
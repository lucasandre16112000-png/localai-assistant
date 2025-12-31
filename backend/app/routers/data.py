"""
LocalAI Assistant - Data Router
API endpoints for data analysis and insights
Author: Manus AI
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Union, List, Dict, Any
from ..services.data_analyzer import data_analyzer

router = APIRouter(prefix="/data", tags=["Data Analysis"])


class DataAnalysisRequest(BaseModel):
    """Model for data analysis request"""
    data: Union[List[Dict], List[List], str]
    data_type: str = "json"


class DataComparisonRequest(BaseModel):
    """Model for data comparison request"""
    dataset1: Union[List[Dict], str]
    dataset2: Union[List[Dict], str]


@router.post("/analyze")
async def analyze_data(request: DataAnalysisRequest):
    """
    Perform comprehensive data analysis.
    
    - **data**: Dataset to analyze (JSON, CSV, or list)
    - **data_type**: Type of data (json, csv)
    """
    if not request.data:
        raise HTTPException(status_code=400, detail="Data cannot be empty")
    
    result = await data_analyzer.analyze_dataset(request.data, request.data_type)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@router.post("/compare")
async def compare_datasets(request: DataComparisonRequest):
    """
    Compare two datasets.
    
    - **dataset1**: First dataset
    - **dataset2**: Second dataset
    """
    result = await data_analyzer.compare_datasets(request.dataset1, request.dataset2)
    return result


@router.post("/insights")
async def generate_insights(analysis: Dict[str, Any]):
    """
    Generate insights from analysis results.
    
    - **analysis**: Analysis results from /analyze endpoint
    """
    insights = await data_analyzer.generate_insights(analysis)
    return {"insights": insights, "count": len(insights)}

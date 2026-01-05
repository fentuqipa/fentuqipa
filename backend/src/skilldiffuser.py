"""
SkillDiffuser - Extract persuasion and communication skills from call transcriptions.

This module processes donation call transcriptions to identify and extract
communication skills used by staff to persuade customers to donate.
"""

from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field


class Skill(BaseModel):
    """Represents an extracted skill from a call transcription."""
    name: str = Field(description="Name of the skill identified")
    description: str = Field(description="Description of how the skill was used")
    quote: str = Field(description="Quote from the transcript demonstrating this skill")
    timestamp: str = Field(default="", description="Timestamp or line number where skill was observed")
    effectiveness: str = Field(description="Assessment of skill effectiveness (high/medium/low)")


class CallAnalysis(BaseModel):
    """Complete analysis of a call transcription."""
    call_id: str = Field(description="Unique identifier for the call")
    skills: List[Skill] = Field(description="List of skills identified in the call")
    overall_assessment: str = Field(description="Overall assessment of the call effectiveness")
    key_insights: List[str] = Field(description="Key insights from the call")


class SkillDiffuser:
    """
    Main class for extracting skills from donation call transcriptions.
    
    This class uses LLM-based analysis to identify persuasion techniques,
    communication skills, and effective strategies used during donation calls.
    """
    
    def __init__(self, api_key: str, model_name: str = "gpt-4"):
        """
        Initialize SkillDiffuser with OpenAI API credentials.
        
        Args:
            api_key: OpenAI API key
            model_name: Name of the model to use (default: gpt-4)
        """
        self.llm = ChatOpenAI(api_key=api_key, model=model_name, temperature=0.3)
        self.parser = JsonOutputParser(pydantic_object=CallAnalysis)
        
    def _create_analysis_prompt(self) -> ChatPromptTemplate:
        """Create the prompt template for analyzing call transcriptions."""
        system_message = """You are an expert in analyzing sales and donation calls to identify 
persuasion techniques and communication skills. Your task is to analyze call transcriptions 
between donation company staff and customers to extract the skills and techniques used.

Focus on identifying:
1. Persuasion techniques (e.g., social proof, urgency, reciprocity)
2. Active listening and empathy
3. Building rapport and trust
4. Handling objections
5. Storytelling and emotional appeal
6. Clear value proposition
7. Closing techniques
8. Question framing and discovery

For each skill identified, provide:
- The skill name
- A description of how it was used
- A direct quote from the transcript
- An effectiveness rating (high/medium/low)

{format_instructions}"""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", "Call ID: {call_id}\n\nTranscript:\n{transcript}\n\nPlease analyze this call and extract the skills used.")
        ])
        
        return prompt.partial(format_instructions=self.parser.get_format_instructions())
    
    def analyze_call(self, call_id: str, transcript: str) -> CallAnalysis:
        """
        Analyze a single call transcription and extract skills.
        
        Args:
            call_id: Unique identifier for the call
            transcript: The full text transcript of the call
            
        Returns:
            CallAnalysis object containing extracted skills and insights
        """
        prompt = self._create_analysis_prompt()
        chain = prompt | self.llm | self.parser
        
        result = chain.invoke({
            "call_id": call_id,
            "transcript": transcript
        })
        
        return CallAnalysis(**result)
    
    def analyze_multiple_calls(self, calls: List[Dict[str, str]]) -> List[CallAnalysis]:
        """
        Analyze multiple call transcriptions.
        
        Args:
            calls: List of dictionaries with 'call_id' and 'transcript' keys
            
        Returns:
            List of CallAnalysis objects
        """
        results = []
        for call in calls:
            analysis = self.analyze_call(call['call_id'], call['transcript'])
            results.append(analysis)
        return results
    
    def get_skill_summary(self, analyses: List[CallAnalysis]) -> Dict[str, Any]:
        """
        Generate a summary of skills across multiple call analyses.
        
        Args:
            analyses: List of CallAnalysis objects
            
        Returns:
            Dictionary containing skill frequency and effectiveness statistics
        """
        skill_counts = {}
        skill_effectiveness = {}
        
        for analysis in analyses:
            for skill in analysis.skills:
                skill_name = skill.name
                if skill_name not in skill_counts:
                    skill_counts[skill_name] = 0
                    skill_effectiveness[skill_name] = []
                
                skill_counts[skill_name] += 1
                skill_effectiveness[skill_name].append(skill.effectiveness)
        
        # Calculate average effectiveness for each skill
        skill_stats = {}
        for skill_name, counts in skill_counts.items():
            effectiveness_values = skill_effectiveness[skill_name]
            high_count = effectiveness_values.count('high')
            medium_count = effectiveness_values.count('medium')
            low_count = effectiveness_values.count('low')
            
            skill_stats[skill_name] = {
                'frequency': counts,
                'effectiveness_distribution': {
                    'high': high_count,
                    'medium': medium_count,
                    'low': low_count
                },
                'avg_effectiveness': high_count / counts if counts > 0 else 0
            }
        
        return {
            'total_calls_analyzed': len(analyses),
            'unique_skills_found': len(skill_counts),
            'skill_statistics': skill_stats
        }


def load_transcriptions_from_file(file_path: str) -> List[Dict[str, str]]:
    """
    Load call transcriptions from a text file.
    
    Expected format:
    ---CALL_ID: <id>---
    <transcript text>
    ---END---
    
    Args:
        file_path: Path to the file containing transcriptions
        
    Returns:
        List of dictionaries with 'call_id' and 'transcript' keys
    """
    calls = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Split by call markers
    call_sections = content.split('---CALL_ID:')
    
    for section in call_sections[1:]:  # Skip the first empty split
        if '---END---' in section:
            parts = section.split('---', 1)
            call_id = parts[0].strip()
            
            transcript_part = parts[1] if len(parts) > 1 else ""
            transcript = transcript_part.replace('---END---', '').strip()
            
            calls.append({
                'call_id': call_id,
                'transcript': transcript
            })
    
    return calls


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.environ.get('OPENAI_API_KEY')
    
    # Example usage
    diffuser = SkillDiffuser(api_key=api_key)
    
    # Example transcript
    example_transcript = """
    Staff: Hello! Thank you for taking my call today. I'm calling from Hope Foundation. 
    How are you doing today?
    
    Customer: I'm doing well, thanks. What is this about?
    
    Staff: That's wonderful to hear! I'm reaching out because you've been such a valued 
    supporter of our work in the past. Last year, your donation helped us provide clean 
    water to over 500 families. I wanted to personally thank you for that amazing impact.
    
    Customer: Oh, that's nice to hear. I'm glad it helped.
    
    Staff: It truly did! And I have some exciting news - we're launching a new initiative 
    this month, and we're hoping our most dedicated supporters like you will join us. 
    For just $50 a month, you can sponsor a child's education for an entire year. 
    Can you imagine the difference that would make?
    
    Customer: Well, I'm not sure... $50 is quite a bit.
    
    Staff: I completely understand your concern. Many of our supporters felt the same way 
    initially. But let me put it in perspective - that's less than $2 a day, about the 
    cost of a coffee. And in return, you're giving a child the chance to break the cycle 
    of poverty through education. Would you be open to trying it for just three months 
    to see the impact?
    
    Customer: When you put it that way... okay, I can try it for three months.
    
    Staff: That's fantastic! Your generosity is going to change a life. Let me get your 
    information to set this up...
    """
    
    analysis = diffuser.analyze_call("CALL_001", example_transcript)
    print(f"Analysis for call {analysis.call_id}:")
    print(f"Skills found: {len(analysis.skills)}")
    for skill in analysis.skills:
        print(f"\n- {skill.name}")
        print(f"  Description: {skill.description}")
        print(f"  Effectiveness: {skill.effectiveness}")

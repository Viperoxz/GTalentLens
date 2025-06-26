import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv
from .base import BaseLLM

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = os.getenv("GEMINI_API_URL")

class GeminiLLM(BaseLLM):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or GEMINI_API_KEY

    def extract_entities(self, prompt: str, text: str) -> Dict:
        headers = {
            "Content-Type": "application/json"
        }
        params = {
            "key": self.api_key
        }
        data = {
            "contents": [
                {
                    "parts": [
                        {"text": f"{prompt}\n{text}"}
                    ]
                }
            ]
        }
        response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        try:
            content = result["candidates"][0]["content"]["parts"][0]["text"]
            # Remove markdown code block
            if content.strip().startswith("```"):
                content = content.strip().lstrip("`json").strip("`").strip()
                # Use regex to make sure:
                import re
                content = re.sub(r"^```(?:json)?\n?", "", content)
                content = re.sub(r"\n?```$", "", content)
            import json
            return json.loads(content)
        except Exception as e:
            raise RuntimeError(f"Gemini response parse error: {e}, raw: {result}")

if __name__ == "__main__":
    prompt = (
        "You are an expert HR assistant. Extract structured data from the provided resume text. "
        "Return the result in JSON with the following fields: name, email, phone, summary, education, "
        "skills, work_experience, total_work_experience, certifications, achievements. "
        "Only rely on the provided resume text. Return in valid JSON format."
    )
    sample_text = """
    0933534980
nguyenthiyen252513@gmail.com
Tan Binh District , HCM City
Bachelor of Marketing
Management
University of Finance - Marketing
2019 - 2023
EDUCATION
Performance Marketing Plan
 PPC Campaigns (Google Ads
, Facebook Ads, Tiktok Ad
s) Content Creat
ion Social Media Manage
ment Email Marketing
KEY SKILLS:
SUMMARY
With approximately 2 years of experience in developing and executing
 marketing activities, including performance and social media marketing, 
I a m seekin g a challengin g positio n t o furthe r enhanc e m y plannin g a
nd analytic al skill s. My long-te rm go al is to beco me  a Marketi ng Mana
ger within the next 5 years.
WORK EXPERIENCE
English:  TOIEC: 850
LANGUAGE
YẾN NGUYỄN
M a r k e t i n g  E x e c u t i v e
Develop and execute digital marketing campaigns across
 platforms: Google Ads, Facebook Ads and Tiktok Ads.
Tracking and optimizing campaigns to meet KPIs, updating
 weekly/  final  report  to  maximize  results  and  lessons  learnt  fo
r next campaigns
Deploy weekly email marketing campaigns
Utilized analytics tools (GA4, Facebook insight) to monitor and
 report on campaign performance, providing actionable insight
s for continuous improvement.
Create a multi-channel digital marketing plan that fits the
 client's budget
Digital Marketing Excutive
Nov 2022- Present
Hotdeal e-commerce company
Social Media Leader
Oct 2023 - Present 
Vinabook company
14/03/2001
Team management: Manage team of 4 members
Content Planning: Orient and plan content for TikTok and
FFanpage  channel.  Collaborate  with  the  sales  department  t
o implement push sale campaigns (Facebook visit rate increas
ed by 45%)
Market Research: Conduct market research to discover market
 insight, consumer segmentation/ pain & gain/ insight
E-commerce development: Create promotion programs and
 carry out growth tasks
    """

    llm = GeminiLLM()
    try:
        result = llm.extract_entities(prompt, sample_text)
        print("Gemini API result:")
        print(result)
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        print("Please check your API key and network connection.")
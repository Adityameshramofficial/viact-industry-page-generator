import os
import pathlib
import google.generativeai as genai


def generate_page(industry_name: str, api_key: str) -> str:
    sop_path = pathlib.Path(__file__).parent.parent / "workflows" / "generate_industry_page.md"
    system_prompt = sop_path.read_text(encoding="utf-8")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_prompt,
    )

    response = model.generate_content(f"Generate page for {industry_name}")
    return response.text


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    key = os.getenv("GEMINI_API_KEY", "")
    if not key:
        print("Error: GEMINI_API_KEY not set in .env")
    else:
        print(generate_page("Mining", key))

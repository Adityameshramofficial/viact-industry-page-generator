import os
import pathlib
from groq import Groq

_BASE = pathlib.Path(__file__).parent.parent / "workflows"


def _load_agent_prompt(agent_file: str) -> str:
    """Combine agent persona with shared SOP rules into one system prompt."""
    persona = (_BASE / agent_file).read_text(encoding="utf-8")
    sop = (_BASE / "generate_industry_page.md").read_text(encoding="utf-8")
    return f"{persona}\n\n{'─' * 60}\n\nSTRUCTURE & FORMAT RULES (mandatory — follow exactly):\n\n{sop}"


def _call_groq(api_key: str, system_prompt: str, user_message: str,
               max_tokens: int = 4096, temperature: float = 0.7) -> str:
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response.choices[0].message.content


def generate_sections(industry_name: str, api_key: str,
                      context: str = "", custom_instructions: str = "") -> str:
    """Agent 01 — Aria Singh: SEO Webpage Dynamic Sections."""
    system = _load_agent_prompt("agent_content.md")

    ctx_block = f"\n\nREFERENCE CONTEXT (ground your content in this):\n{context}" if context.strip() else ""
    custom_block = f"\n\nUSER CUSTOM INSTRUCTIONS (highest priority — follow precisely):\n{custom_instructions}" if custom_instructions.strip() else ""

    user_msg = f"""Generate ONLY PART 1: WEBPAGE CONTENT (DYNAMIC SECTIONS ONLY) for the industry: {industry_name}

Output exactly these 8 sections in strict order with all H-tags, bold formatting, and word limits:
  1. Hero Section — [H1] "AI for Safety & Productivity in {industry_name}" (eyebrow label, plain — no bold), [H2] **bold % metric headline** (max 20 words, specific stat like "25% Reduction in Accidents"), [H3] description (35-45 words),
     YouTube Video URL: [use URL from context if provided, else write: ADD_YOUTUBE_URL_HERE]
  2. One Intelligent Platform — [H2] "One Intelligent Platform — [Industry-Specific Subtitle max 7 words]", description (25-35 words, mentions AI CCTV + IoT + edge + wearables + SIF prevention)
  3. Proven Impact Metrics — exactly 3 blocks: [Number]%[↑/↓], [H3] title (max 4 words), description (10-15 words with real numbers)
  4. AI CCTV Use Cases — exactly 6 blocks: [H3] title (max 5 words) (Red color, centered), description (20-30 words naming hazard + consequence prevented)
  5. Pre-Built AI Safety Solutions — [H2] "Pre-Built AI Safety Solutions for Every {industry_name} Risk", description (15-20 words, ready-to-deploy packages, {industry_name}-specific environment)
  6. viGent: AI AGENT FOR {industry_name.upper()} — description (30-40 words, continuous safety data + HSE manager empowerment)
  7. Voices from the Field — exactly 5 testimonials: **"..."** review (35-50 words), Job Title & Country
  8. CTA Section — [H2] headline, description (20-30 words)

STRICT RULES:
- [H1] on hero eyebrow label only (ONE per page). [H2] on hero % metric headline (bold) and all section titles. [H3] on hero description, metric titles, and use case titles.
- Hero [H2] metric headline and all review texts wrapped in **bold** — no other bold in Part 1.
- Hero section uses a YouTube video (not an image) — include the YouTube Video URL field.
- DO NOT include image prompts or SEO metadata here.{ctx_block}{custom_block}"""

    return _call_groq(api_key, system, user_msg, max_tokens=6000, temperature=0.8)


def generate_seo_metadata(industry_name: str, api_key: str,
                          context: str = "", custom_instructions: str = "") -> str:
    """Agent 02 — Marcus Webb: On-Page SEO Metadata & Alt Texts."""
    system = _load_agent_prompt("agent_seo.md")

    ctx_block = f"\n\nREFERENCE CONTEXT:\n{context}" if context.strip() else ""
    custom_block = f"\n\nUSER CUSTOM INSTRUCTIONS (highest priority — follow precisely):\n{custom_instructions}" if custom_instructions.strip() else ""

    user_msg = f"""Generate ONLY PART 3: ON-PAGE SEO METADATA for the industry: {industry_name}

Output the complete SEO package in this exact format:

URL: https://www.viact.ai/industry/[slug]

Meta Title: [≤60 chars — primary keyword + | viAct.ai]
Meta Description: [150-160 chars exactly — pain point first, mention CCTV + IoT/Edge/Wearables, soft CTA]

Keywords:
1. [long-tail keyword 1]
2. [long-tail keyword 2]
3. [long-tail keyword 3]
4. [long-tail keyword 4]
5. [long-tail keyword 5]
6. [long-tail keyword 6]

Video Title: [50-70 chars, YouTube SEO optimized]
Video Description: [100-150 words, YouTube SEO optimized, includes primary keyword]

Image Alt Texts:
Use Case 1: [alt text ≤125 chars]
Use Case 2: [alt text ≤125 chars]
Use Case 3: [alt text ≤125 chars]
Use Case 4: [alt text ≤125 chars]
Use Case 5: [alt text ≤125 chars]
Use Case 6: [alt text ≤125 chars]
Reviewer 1: [alt text ≤125 chars]
Reviewer 2: [alt text ≤125 chars]
Reviewer 3: [alt text ≤125 chars]
Reviewer 4: [alt text ≤125 chars]
Reviewer 5: [alt text ≤125 chars]
viGent Dashboard: [alt text ≤125 chars]
CTA Section: [alt text ≤125 chars]

IMPORTANT: Do NOT include Schema Markup. Do NOT include webpage content sections or image generation prompts.{ctx_block}{custom_block}"""

    return _call_groq(api_key, system, user_msg, max_tokens=2500, temperature=0.4)


def generate_image_prompts(industry_name: str, api_key: str,
                           context: str = "", custom_instructions: str = "") -> str:
    """Agent 03 — Dani Cruz: Nano Banana AI Image Prompts."""
    system = _load_agent_prompt("agent_images.md")

    ctx_block = f"\n\nREFERENCE CONTEXT:\n{context}" if context.strip() else ""
    custom_block = f"\n\nUSER CUSTOM INSTRUCTIONS (highest priority — follow precisely):\n{custom_instructions}" if custom_instructions.strip() else ""

    user_msg = f"""Generate ONLY PART 2: NANO BANANA IMAGE PROMPTS for the industry: {industry_name}

⚠️ IMPORTANT: The hero section uses a YouTube video embed — NO hero image is needed.
Do NOT generate a hero image prompt. Generate exactly 12 prompts.

Each prompt must embed the pixel dimensions inside the prompt string and be immediately followed by an Alt Text line.

Format for every prompt:
[IMAGE PROMPT FOR NANO BANANA - SECTION NAME]: "full prompt text including (WxH px) inside the string"
Alt Text: "SEO-optimized alt text ≤125 characters"

Prompts required (in this exact order, 11 total):
1.  Use Case 1 (520x327 px) — CCTV field view matching use case 1 scenario
2.  Use Case 2 (488x293 px) — CCTV field view matching use case 2 scenario
3.  Use Case 3 (520x303 px) — CCTV field view matching use case 3 scenario
4.  Use Case 4 (520x303 px) — CCTV field view matching use case 4 scenario
5.  Use Case 5 (520x303 px) — CCTV field view matching use case 5 scenario
6.  Use Case 6 (520x317 px) — CCTV field view matching use case 6 scenario
7.  viGent Dashboard (422x377 px) — dark-mode AI safety operations dashboard ONLY (NO field/CCTV view)
8.  Reviewer 1 Headshot (56x56 px) — professional corporate headshot
9.  Reviewer 2 Headshot (56x56 px) — professional corporate headshot
10. Reviewer 3 Headshot (56x56 px) — professional corporate headshot
11. Reviewer 4 Headshot (56x56 px) — professional corporate headshot
12. Reviewer 5 Headshot (56x56 px) — professional corporate headshot

IMPORTANT: Do NOT include webpage content sections or SEO metadata.{ctx_block}{custom_block}"""

    return _call_groq(api_key, system, user_msg, max_tokens=3500, temperature=0.7)


def generate_page(industry_name: str, api_key: str) -> str:
    """Legacy full-page generator (kept for backwards compatibility)."""
    sop = (_BASE / "generate_industry_page.md").read_text(encoding="utf-8")
    return _call_groq(api_key, sop, f"Generate page for {industry_name}", max_tokens=8000)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    key = os.getenv("GROQ_API_KEY", "")
    if not key:
        print("Error: GROQ_API_KEY not set in .env")
    else:
        print(generate_sections("Mining", key))

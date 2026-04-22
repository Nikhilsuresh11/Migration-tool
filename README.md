# Document Migration Readiness Tool

A full-stack tool that answers one question for every document you upload:

> **"Is this document ready to migrate to Document360? If not, what needs to change?"**

Upload a `.docx` or `.pdf` file. Get back a readiness grade, a score out of 100, an effort estimate in person-days, a list of blockers that must be fixed, and AI-generated suggestions that reference your actual document — not generic advice.

---

## How It Works

The tool runs three things in sequence when you upload a file:

**1. Parses the document** — extracts every heading, paragraph, table, image, and link from Word and PDF files. 

**2. Extracts metrics** — computes everything a migration specialist would manually audit: word count, page count, heading structure, broken links, image formats and size, table complexity, readability score, duplicate sections.

**3. Runs AI analysis** — sends the extracted text and metrics to LLaMA 3.3 70B (via Groq) which evaluates content clarity, tone consistency, structural quality, and produces document-specific suggestions. The prompt explicitly instructs the model to cite actual section titles and acronyms — not generic advice. Also fallback as google/gemma-4-26b-a4b (via openrouter)

The React frontend visualises all of this in a dashboard styled after Document360's own UI.

---

## Project Structure

```
Migration-tool/
├── backend/
│   ├── app.py                      # Flask entry point
│   ├── config.py                   # API keys, thresholds, limits
│   ├── requirements.txt
│   ├── .env                        # Your Groq API key, Openrouter API key goes here
│   ├── parsers/
│   │   ├── docx_parser.py          # Extracts text, headings, tables, images from .docx
│   │   └── pdf_parser.py           # Same for .pdf
│   ├── metrics/
│   │   └── extractor.py            # Computes all quantitative metrics
│   ├── analysis/
│   │   └── ai_analyzer.py          # Builds the prompt, calls Groq, parses response
│   ├── services/
│   │   ├── metrics_service.py      # Service layer wrapping extractor.py
│   │   └── analysis_service.py     # Service layer wrapping ai_analyzer.py
│   ├── routes/
│   │   ├── parse_routes.py         # POST /api/parse
│   │   ├── metrics_routes.py       # POST /api/metrics
│   │   ├── analysis_routes.py      # POST /api/analyze
│   │   └── report_routes.py        # POST /api/report  ← cummulative endpoint used for UI with skimmed output from all other three routes
│   └── utils/
│       └── helpers.py              # File type detection
│
└── frontend/
    ├── src/
    │   ├── App.jsx                 # Root — manages upload/results state
    │   ├── components/
    │   │   ├── UploadScreen.jsx    # Drag-and-drop zone with loading steps
    │   │   ├── Dashboard.jsx       # Results layout — banner, metrics, tabs
    │   │   ├── tabs/
    │   │   │   ├── Overview.jsx    # Score ring, effort bars, blockers, AI analysis
    │   │   │   ├── ContentDebt.jsx # Acronyms, outdated refs, placeholders
    │   │   │   └── RawJSON.jsx     # Syntax-highlighted full API response
    │   │   └── ActionBar.jsx       # Export JSON button
    │   └── main.jsx
    ├── package.json
    └── vite.config.js              # Proxies /api/* to Flask on port 5000
```

The key design decision: `parsers/` only extracts raw content. `metrics/` only computes numbers. `analysis/` only handles AI. Routes wire them together. This makes each piece independently testable.

---

## Setup

### What you need

- Python 3.9+ (backend)
- Node.js 18+ (frontend)
- A Groq API key - https://console.groq.com
- A Openrouter API key - https://openrouter.ai/workspace (fallback)
---

### Backend

```bash
# 1. Enter the backend folder
cd backend

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your Groq API key
#    Open .env and set:
#    GROQ_API_KEY=your_groq_api_key_here
#    OPENROUTER_API_KEY=your_open_router_key_here

# 5. Start the Flask server
python app.py
```

Backend runs at `http://127.0.0.1:5000`



### Testing documents used (input)

https://drive.google.com/drive/folders/10WGgattvIv08c_a0UN0sojcMlZk3oe0x?usp=sharing

### Input and Output

curl --location 'http://127.0.0.1:5000/api/parse' \
--form 'file=@"d:\\Start\\migrationTool\\docs\\Indus Valley Annual Report 2025.pdf"'

<details>
<summary><strong> View Full API Response</strong></summary>

<br>

```json
{
    "data": {
        "file_type": "pdf",
        "headings": [
            {
                "level": 4,
                "text": "Sajith Pai | sp@blume.vc"
            },
            {
                "level": 4,
                "text": "Anurag Pagaria | anurag@blume.vc"
            },
            {
                "level": 4,
                "text": "Nachammai Savithiri | ns@blume.vc"
            },
            {
                "level": 4,
                "text": "&"
            },
            {
                "level": 4,
                "text": "Dhruv Trehan, Editorial Fellow"
            },
            {
                "level": 1,
                "text": "Indus Valley Annual Report 2025"
            },
            {
                "level": 2,
                "text": "Welcome to the Indus Valley Annual Report 2025"
            },
            {
                "level": 4,
                "text": "India’s vibrant startup ecosystem, concentrated in the eastern suburbs of Bangalore, the satellite cities of"
            },
            {
                "level": 4,
                "text": "Gurgaon and Noida in the Delhi National Capital Region (NCR), the districts of Lower Parel & the Andheri East –"
            },
            {
                "level": 4,
                "text": "Powai belt in Mumbai, the Southern suburbs of Chennai, and in the various scattered pockets across many other"
            },
            {
                "level": 4,
                "text": "cities such as Pune, Hyderabad, Chandigarh etc., has lacked a singular name."
            },
            {
                "level": 4,
                "text": "At Blume, we like to use Indus Valley as a catch all moniker for the Indian startup ecosystem. It is a twist on the"
            },
            {
                "level": 4,
                "text": "typical Silicon Wadi / Glen / Fen naming convention, as well as a reference to the Indus Valley Civilisation, one of"
            },
            {
                "level": 4,
                "text": "the vibrant centres of the ancient world, and the ancestral civilisation of the Indian people."
            },
            {
                "level": 4,
                "text": "Unlike Silicon Valley which has a geographical connotation, the term Indus Valley has no such overtone. It is"
            },
            {
                "level": 4,
                "text": "instead a reference to the entire Indian startup ecosystem, spread throughout the nation. It is also an attitude, a"
            },
            {
                "level": 4,
                "text": "mindset, one of invention, and ‘jugaad’ and chutzpah."
            },
            {
                "level": 4,
                "text": "The Indus Valley Annual Report published by Blume Ventures, celebrates the rise of Indus Valley, and its"
            },
            {
                "level": 4,
                "text": "emergence as one of the centres of innovation and enterprise in the startup world. It gives us a chance to look"
            },
            {
                "level": 4,
                "text": "back, and take stock of its evolution, and look ahead to what is coming. We welcome you to the fourth edition of"
            },
            {
                "level": 4,
                "text": "the Indus Valley Annual Report! Our previous editions (2024, 2023, 2022) can be accessed at the website"
            },
            {
                "level": 4,
                "text": "indusvalleyreport.com"
            },
            {
                "level": 1,
                "text": "India"
            },
            {
                "level": 1,
                "text": "Indus Valley"
            },
            {
                "level": 1,
                "text": "How to read this report"
            },
            {
                "level": 3,
                "text": "Given we have sourced the data across various reports and datasets, consistency in data will always be"
            },
            {
                "level": 3,
                "text": "a challenge. That said, while sometimes an occasional number or two may not match with the other, the"
            },
            {
                "level": 3,
                "text": "broad direction or narrative of these is consistent and comparable."
            },
            {
                "level": 3,
                "text": "We have used millions, billions, trillions (vs lacs, crores) where possible. When we use ₹ billion or ₹"
            },
            {
                "level": 3,
                "text": "trillion, it can sometimes be hard to translate it to $. A shorthand for ₹ billion to $ million is that ₹1 billion ="
            },
            {
                "level": 3,
                "text": "₹100 crores = $12 million roughly. A shorthand for ₹ trillion to $ billion is ₹1 trillion = $12 billion roughly."
            },
            {
                "level": 3,
                "text": "Despite all the charts and datasets we have listed, this is not a data book. We didn’t create it to serve as"
            },
            {
                "level": 3,
                "text": "an exhaustive repository of data or reportage on India. Rather, it is more a narrative, and less a"
            },
            {
                "level": 3,
                "text": "dataguide. Or even better, you should see it as a source of perspective on the Indian startup ecosystem."
            },
            {
                "level": 3,
                "text": "And as with all perspectives, a lot depends on the vantage point of the observer. As the leading seed"
            },
            {
                "level": 3,
                "text": "fund in India, we do think we have a unique perspective and insight into the Indian startup ecosystem, or"
            },
            {
                "level": 3,
                "text": "Indus Valley, as we term it. And with The Indus Valley Report, we hope to get you, dear reader, to view"
            },
            {
                "level": 3,
                "text": "the Indian economy through our lens. Do tell us how you see it. Compliments, criticism, feedback all"
            },
            {
                "level": 3,
                "text": "welcome at sp@blume.vc and / or anurag@blume.vc"
            },
            {
                "level": 1,
                "text": "Section I: India"
            },
            {
                "level": 4,
                "text": "AI meets caste. Cutting-edge tech-advances in AI collide with that most ancient of Indian institutions, the caste system."
            },
            {
                "level": 1,
                "text": "India in one tweet"
            },
            {
                "level": 1,
                "text": "India"
            },
            {
                "level": 1,
                "text": "India - The Last 5 Years"
            },
            {
                "level": 4,
                "text": "How we got here; a look at the events,"
            },
            {
                "level": 4,
                "text": "trends, policies, and initiatives that"
            },
            {
                "level": 4,
                "text": "shaped the Indian economy over the past"
            },
            {
                "level": 4,
                "text": "five years through COVID, and after. We"
            },
            {
                "level": 4,
                "text": "cover the economic downturn,"
            },
            {
                "level": 4,
                "text": "government initiatives to spur recovery,"
            },
            {
                "level": 4,
                "text": "subsequent boom, and inflationary"
            },
            {
                "level": 4,
                "text": "growth, followed by RBI initiatives to"
            },
            {
                "level": 4,
                "text": "control inflation, and finally the growth"
            },
            {
                "level": 4,
                "text": "taper as consumption and government"
            },
            {
                "level": 4,
                "text": "spends reduced."
            },
            {
                "level": 1,
                "text": "India vs the World: Where India stands, today"
            },
            {
                "level": 1,
                "text": "But how did we get here?"
            },
            {
                "level": 3,
                "text": "The next few slides capture the journey the Indian Economy has been on in the last few years."
            },
            {
                "level": 4,
                "text": "The COVID-19 pandemic triggered India's worst economic contraction in its post-independence history"
            },
            {
                "level": 1,
                "text": "COVID pandemic dealt India a severe economic shock"
            }
        ],
        "images_count": 853,
        "metadata": {
            "author": "",
            "created": "",
            "creator": "Google",
            "modified": "",
            "producer": "",
            "subject": "",
            "title": "IVAR25 - vF"
        },
        "pages": [
            {
                "page_number": 1,
                "text": "Sajith Pai | sp@blume.vc\nAnurag Pagaria | anurag@blume.vc \nNachammai Savithiri | ns@blume.vc \n&\nDhruv Trehan, Editorial Fellow\nIndus Valley Annual Report 2025",
                "word_count": 22
            },
            {
                "page_number": 2,
                "text": "2\nWelcome to the Indus Valley Annual Report 2025\nIndia’s vibrant startup ecosystem, concentrated in the eastern suburbs of Bangalore, the satellite cities of \nGurgaon and Noida in the Delhi National Capital Region (NCR), the districts of Lower Parel & the Andheri East – \nPowai belt in Mumbai, the Southern suburbs of Chennai, and in the various scattered pockets across many other \ncities such as Pune, Hyderabad, Chandigarh etc., has lacked a singular name. \nAt Blume, we like to use Indus Valley as a catch all moniker for the Indian startup ecosystem. It is a twist on the \ntypical Silicon Wadi / Glen / Fen naming convention, as well as a reference to the Indus Valley Civilisation, one of \nthe vibrant centres of the ancient world, and the ancestral civilisation of the Indian people.\nUnlike Silicon Valley which has a geographical connotation, the term Indus Valley has no such overtone. It is \ninstead a reference to the entire Indian startup ecosystem, spread throughout the nation. It is also an attitude, a \nmindset, one of invention, and ‘jugaad’ and chutzpah.\nThe Indus Valley Annual Report published by Blume Ventures, celebrates the rise of Indus Valley, and its \nemergence as one of the centres of innovation and enterprise in the startup world. It gives us a chance to look \nback, and take stock of its evolution, and look ahead to what is coming. We welcome you to the fourth edition of \nthe Indus Valley Annual Report! Our previous editions (2024, 2023, 2022) can be accessed at the website \nindusvalleyreport.com",
                "word_count": 257
            },
            {
                "page_number": 3,
                "text": "➔Consumption and services dominate our GDP. (21) \n➔India is formalising, steadily. (29) \n➔India doesn’t save enough. (33) \n➔Why land issues mean India hoards up on gold. (37) \n➔India doesn’t invest in human capital. (41)\n➔India’s manufacturing playbook is good, but not great. (48) \n➔How DPI made India a Digital Welfare State. (54) \n➔How India1’s savings surplus spur an Equity and F&O boom. (58) \nA macro-economic account of the Indian economy over the last five \nyears, from the COVID-pandemic and bust, to the recent growth taper.\nIndia - The Last Five Years Pg 7 \n India\n Indus Valley\nLong-Term Structural Forces Pg 20\n➔India’s consumption numbers look good on an overall basis, but \nnot on a per capita basis.\n➔Why India under consumes.\n➔How India1, India’s top 10%, drives the Indian economic engine.\n➔India1 is not widening as much as deepening.\n➔India1’s high share of consumption shapes the India consumer \nmarket in many distinct ways.\nConsumption Pg 66\nVenture funding trends, and a deep dive, followed by a look at \nIndia’s Unicorns, and the Venture Debt market.\nIndus Valley - Funding Trends Pg 95 \nA deep dive into India's booming IPO market, as well as the SME \nIPO’s rise, including what it implies for founders.\nIPO Boom \n Pg 111\n➔Quick Commerce: Why it works in India, the implications of its \nrise, and is there irrational exuberance re QCom? (120)\n➔AI: Is India getting a foundational model soon? (148)\nSector Deep Dives Pg 120\n➔The various India2 Playbooks. (157)\n➔How Indus Valley influenced Indian advertising. (165)\n➔Returns, and how Indian startups are addressing it. (170)\n➔Marketing framework for the Indian diaspora or India0. (179)\nIndus Valley Playbooks Pg 157 \n3",
                "word_count": 277
            },
            {
                "page_number": 4,
                "text": "4\nHow to read this report\nGiven we have sourced the data across various reports and datasets, consistency in data will always be \na challenge. That said, while sometimes an occasional number or two may not match with the other, the \nbroad direction or narrative of these is consistent and comparable. \nWe have used millions, billions, trillions (vs lacs, crores) where possible. When we use ₹ billion or ₹ \ntrillion, it can sometimes be hard to translate it to $. A shorthand for ₹ billion to $ million is that ₹1 billion = \n₹100 crores = $12 million roughly. A shorthand for ₹ trillion to $ billion is ₹1 trillion = $12 billion roughly.\nDespite all the charts and datasets we have listed, this is not a data book. We didn’t create it to serve as \nan exhaustive repository of data or reportage on India. Rather, it is more a narrative, and less a \ndataguide. Or even better, you should see it as a source of perspective on the Indian startup ecosystem. \nAnd as with all perspectives, a lot depends on the vantage point of the observer. As the leading seed \nfund in India, we do think we have a unique perspective and insight into the Indian startup ecosystem, or \nIndus Valley, as we term it. And with The Indus Valley Report, we hope to get you, dear reader, to view \nthe Indian economy through our lens. Do tell us how you see it. Compliments, criticism, feedback all \nwelcome at sp@blume.vc and / or anurag@blume.vc",
                "word_count": 255
            },
            {
                "page_number": 5,
                "text": "Section I: India",
                "word_count": 3
            },
            {
                "page_number": 6,
                "text": "6\nSource: Twitter / @dhammainvicta; The tweet was subsequently deleted\nAI meets caste. Cutting-edge tech-advances in AI collide with that most ancient of Indian institutions, the caste system.\nIndia in one tweet\nThe associations in this tweet expose a clear bias. \nMany of these would be considered inappropriate in \ncontemporary Indian discourse. \nYet, the AI completion offers a glimpse at how India’s \ndeeply rooted social structures continue to shape \nperspectives, even when filtered through modern \ntechnologies and global pop culture touchpoints.\n[Redacted]",
                "word_count": 82
            },
            {
                "page_number": 7,
                "text": "India\nIndia - The Last 5 Years\nHow we got here; a look at the events, \ntrends, policies, and initiatives that \nshaped the Indian economy over the past \nfive years through COVID, and after. We \ncover the economic downturn, \ngovernment initiatives to spur recovery, \nsubsequent boom, and inflationary \ngrowth, followed by RBI initiatives to \ncontrol inflation, and finally the growth \ntaper as consumption and government \nspends reduced.\nConsumption Pg 66\nLong-term Structural Forces Pg 20\nA macro-economic account of the Indian economy over \nthe last five years, since the COVID-pandemic and bust, \nto the recent growth taper.\nIndia - The Last Five Years \n Pg 7 \n7",
                "word_count": 106
            },
            {
                "page_number": 8,
                "text": "Real GDP Growth (in %)\nMarket Cap (in USD trillion, as on 3 January 2025)\nPer Capita Income (in USD thousands)\nCPI Inflation 2024 (in %)\nIndia - The Last Five Years\nIndia vs the World: Where India stands, today\nAlphabet \nAmazon \nMicrosoft \nNvidia\nApple\nMeta\nTesla\nSource: (Clockwise from top left) IMF, MacroMicro /Visual Capitalist, Jefferies, IMF\nIndia ranks #4 in \nthe market cap \nstandings\n8",
                "word_count": 67
            },
            {
                "page_number": 9,
                "text": "But how did we get here? \nThe next few slides capture the journey the Indian Economy has been on in the last few years.\n9",
                "word_count": 25
            },
            {
                "page_number": 10,
                "text": "10\nThe COVID-19 pandemic triggered India's worst economic contraction in its post-independence history \nCOVID pandemic dealt India a severe economic shock\nSource: MOSPI , Economics Observatory\nIndia's GDP growth rate before and during COVID\nIndia was significantly worse-off vs peers \nIndia - The Last Five Years",
                "word_count": 46
            },
            {
                "page_number": 11,
                "text": "11\nIndia - The Last Five Years\n+76.5%\n+67.5%\nGovernment Capex spends rise\nIncrease in Direct Benefit Transfers\nSubsidy surge\nGovernment’s response\nRBI’s response\nDeclining repo rates\nAggressive government spending was coupled with historically low repo rates from RBI to push the economy forward\nTo combat the economic decline, a dual response\nSource: Left three charts (clockwise from top) PRS India, DBT website, Bank of Baroda, Cleartax",
                "word_count": 67
            },
            {
                "page_number": 12,
                "text": "12\nThe RBI's extended low interest rate regime sparked an unprecedented surge in personal borrowing..\nCheap money sparks a personal credit boom…\nSource: IMA India, UBS\nPersonal loans replace industry loans as biggest \nsegment of non-food borrowings\nIn this period of 4% repo rates, consumer loans \ndrive >18% of PFCE (from <10% in FY12)\nIndia - The Last Five Years",
                "word_count": 60
            },
            {
                "page_number": 13,
                "text": "…leading to a consumption boom, sparking a V-shaped recovery\nSource: Newsclick / Reserve Bank of India, MOSPI\nIndia - The Last Five Years\nIndia engineered a remarkable recovery, with GDP growth rebounding from -5.8% in FY21 to 9.7% in FY22\n13",
                "word_count": 41
            },
            {
                "page_number": 14,
                "text": "14\nThe revival of the Indian economy was achieved through aggressive government spending, which doubled the fiscal \ndeficit between FY20 and FY21, eventually resulting in a rise in money supply. The combination of expanded money \nsupply, along with surging personal credit, and resurgent consumption pushed inflation steadily upward.\nThe cost of recovery: soaring fiscal deficit, and rising inflation\nSource: Jefferies, The Mirrority, World Bank’s Global Database of Inﬂation\nIndia - The Last Five Years\nRising fiscal deficit\nGrowing money supply\nElevated inflation rates",
                "word_count": 83
            },
            {
                "page_number": 15,
                "text": "15\nSeeing inflation rise, RBI began monetary tightening, steadily ramping up the repo rate (what banks borrow from RBI at) from \n4 to 6.5%, thereby increasing cost of money, and impacting the growth in unsecured loans.\nA concerned RBI reins in the easy money policy\nSource: Cleartax, Jefferies\nIndia - The Last Five Years\nRepo Rates back up to 6.5%\nUnsecured loan growth slowdown",
                "word_count": 64
            },
            {
                "page_number": 16,
                "text": "16\nSource: Quess / Macquarie, RBI Urban Households Survey on Inﬂation \nIndia - The Last Five Years\nWage growth below inflation across most industries\nPersistent high inflation expectations among \nhouseholds, post-COVID \nMeanwhile slow wage growth and continuing inflationary \nexpectations dampened urban consumer sentiment…",
                "word_count": 43
            },
            {
                "page_number": 17,
                "text": "17\nSource: CLSA, Axis Bank, Jefferies / CRIF\nIndia - The Last Five Years\n…even as the rural sector benefited from monsoon, higher MSP, \nincreased handouts to women, and microfinance growth\nRural outperforming urban areas in \nFMCG sales in recent quarters\n₹2Tn worth of income transfers contributing \ndirectly to household (HH) expenditure\nMicrofinance loan growth",
                "word_count": 55
            },
            {
                "page_number": 18,
                "text": "18\nSource: PNB, CLSA \nGDP growth was sustained on the back of heavy government capex spends given election year.\nSlowing consumption growth countered by heavy govt spends\nIndia - The Last Five Years\nPFCE or Private Final Consumption Expenditure growth \ndiverged from GDP growth for the first time in FY24\nCentral and state capex growth stayed strong",
                "word_count": 57
            },
            {
                "page_number": 19,
                "text": "19\nSource: CLSA, Macquarie \nIndia - The Last Five Years\nGovernment spend lagging in FY25\nThanks to slowing capex spends, on the back of already \nslowing consumption spends, GDP growth is tapering down\nPost-election spending cuts (to rein in fiscal deficit) meet \nconsumer slowdown, leading to GDP growth tapering",
                "word_count": 49
            },
            {
                "page_number": 20,
                "text": "India\nConsumption and services dominate our GDP.\nIndia is formalising, steadily.\nIndia doesn’t save enough.\nWhy land issues mean India hoards up on gold.\nIndia doesn’t invest in human capital.\nIndia’s manufacturing playbook is good, but not great.\nHow DPI made India a Digital Welfare State.\nHow India1’s savings surplus spur an equity and F&O boom.\nThe Indian economy is shaped by the interaction \nbetween, and acting upon of several powerful long-term \nstructural forces and trends. A closer look at these \nlong-term structural forces!\nLong-Term Structural Forces \nIndia - The Last Five Years Pg 7\nConsumption Pg 66\n20",
                "word_count": 99
            },
            {
                "page_number": 21,
                "text": "India\n➔\nConsumption and services dominate our GDP. \n➔\nIndia is formalising, steadily.\n➔\nIndia doesn’t save enough.\n➔\nWhy land issues mean India hoards up on gold.\n➔\nIndia doesn’t invest in human capital.\n➔\nIndia’s manufacturing playbook is good, but not \ngreat.\n➔\nHow DPI made India a Digital Welfare State.\n➔\nHow India1’s savings surplus spur an Equity and \nF&O boom.\nLong-Term Structural Forces \nConsumption and \nservices dominate \nour GDP\nConsumption and services drive the \nIndian economy, unlike say in China, \nwhere investments and manufacturing \nplay a key role. \nIndia - The Last Five Years Pg 7\nConsumption Pg 66\n21",
                "word_count": 104
            },
            {
                "page_number": 22,
                "text": "22\nIndia’s GDP $3.6 trillion / ₹295.4 trillion (FY24)\nTwo ways to understand GDP\nSource: MOSPI\nIndia - Long-Term Structural Forces / Consumption and Services\nPFCE\n(Consumption)\n56%\nGFCF\n(Investment)\n33%\nGovt. Spends 9%\nServices\n54%\nIndustry\n31%\nAgriculture\n15%\nOthers (Exports less \nImports etc ) 2%\nIndia’s GDP by expenditure components\nIndia’s GDP by sectoral split",
                "word_count": 57
            },
            {
                "page_number": 23,
                "text": "23\nIndia’s GDP is heavily dependent on consumer spending\nSource: Jefferies\nPFCE\n(Consumption)\n56%\nGFCF\n(Investment)\n33%\nGovt 9% \nOthers 2%\nIndia’s GDP by expenditure components\nPFCE has consistently been at 55-60% of Indian GDP through the last decade\nIndia - Long-Term Structural Forces / Consumption and Services",
                "word_count": 48
            },
            {
                "page_number": 24,
                "text": "24\nA key reason is our middling savings rate and low FDI constricting investment in productive assets. India’s FDI inflows for \nFY11-20 were $512 billion while China’s for 2011-20 were over 4x that at $2.4 trillion.\nSource: CLSA / MOSPI, Trading Economics, PIIE, IBEF\nInvestment or Gross Fixed Capital Formation (GFCF) has been a \nmuch smaller contributor to GDP\nChina\n2000-09 | 37.8%\n2010-19 | 43.2%\n2020-23 | 41.9%\nChina\n2000-09 | 44.7%\n2010-19 | 46.7%\n2020-23 | 44.7%\nGFCF as % of GDP\nGross Savings Rate\nIndia - Long-Term Structural Forces / Consumption and Services",
                "word_count": 96
            },
            {
                "page_number": 25,
                "text": "Construction (9%)\nMining & Utilities (5%)\nManufacturing(17%)\n25\nServices sector dominates the Indian economy\nSource: MOSPI, PLFS 23-24\nFinancial & \nProfessional Services, \nReal Estate (23%)\nTrade, Transportation, Hotels, \nCommunication (19%)\nPublic Services (13%)\nManufacturing punches well below the ideal \nweight. China’s equivalent number is 26%. We \ndeep dive into reason’s for manufacturing’s low \nshare and its potential in a subsequent section.\nReal Estate / Construction sector is a key sector \nas it is a large employer of unskilled workers. It \naccounts for 12% of India’s labour force, more \nthan manufacturing (11.4%)!\nServices is a large contributor to India’s \neconomy; unusual for a country with per capita \nincome under $3k. \nServices\n54% of GDP\n31% of Labour Force\nIndustry\n31% of GDP\n23% of Labour Force\nAgriculture\n15% of GDP\n46% of Labour Force\nIndia’s GDP by expenditure components\nServices Labour Force % Split\nIndustry Labour Force % Split\nIndia - Long-Term Structural Forces / Consumption and Services",
                "word_count": 157
            },
            {
                "page_number": 26,
                "text": "26\nServices dominating Industry is not a new trend\nSource: CLSA\nIndustry and manufacturing \nhas consistently been a \nsmaller portion of the \neconomy than services.\n% Share of Gross Value Added (GVA): Agriculture, Industry and Services FY64-FY24\nIndia - Long-Term Structural Forces / Consumption and Services",
                "word_count": 46
            },
            {
                "page_number": 27,
                "text": "27\nServices strength is visible in increasing market share of global \nexports (unlike Goods exports)\nSource: Goldman Sachs\nIndia’s share of global services exports is up from 2% to nearly \n5% of global trade over the past two decades\nIndia’s services exports has grown nearly 2x relative to peers \nlike Brazil and Mexico\nIndia - Long-Term Structural Forces / Consumption and Services",
                "word_count": 62
            },
            {
                "page_number": 28,
                "text": "28\nIT Exports are the crown jewel of our services economy\nSource: Goldman Sachs, CLSA, Jefferies / Nasscom\nGCC headcount has \nmore than doubled in \nunder the last \ndecade, albeit \nbenefitting from a \nlower base.\nFrom a fifth of the \nsize of IT Services, \nGCCs are now a third \nof IT Services \nrevenues; all this in \nunder a decade.\nAnd of late, Professional Consulting Services and GCCs stepping up too!\nProfessional Consulting has been growing faster than IT \nServices, though from a lower base.\nIndia is a global leader with 1,700 Global Capability \nCentres (GCCs). GCC headcount and revenue is growing \nfaster than IT Services.\nIndia - Long-Term Structural Forces / Consumption and Services",
                "word_count": 114
            },
            {
                "page_number": 29,
                "text": "India\n➔\nConsumption and Services dominate our GDP. \n➔\nIndia is formalising, steadily.\n➔\nIndia doesn’t save enough.\n➔\nWhy land issues mean India hoards up on gold.\n➔\nIndia doesn’t invest in human capital.\n➔\nIndia’s manufacturing playbook is good, but not \ngreat.\n➔\nHow DPI made India a Digital Welfare State.\n➔\nHow India1’s savings surplus spur an Equity and \nF&O boom.\nLong-Term Structural Forces\nIndia is formalising \nsteadily\nWe are seeing a steady but firm shift to a \norganised, branded, formal market, from \nwhat was an unorganised, unbranded, \nand informal market.\nIndia - The Last 5 Years Pg 7\nConsumption Pg 66\n29",
                "word_count": 106
            },
            {
                "page_number": 30,
                "text": "30\nThe Indian economy is formalising, shifting from unorganised \nto organised\nSource: Jefferies, GST Council\nIndia - Long-Term Structural Forces / Formalisation\nIncreasing share of income captured in direct tax filings\nGrowth in registered GST payees indicates a formal shift",
                "word_count": 40
            },
            {
                "page_number": 31,
                "text": "31\nSigns of formalisation visible in the consumer economy too \nSource: CLSA\nJewellery market formalisation\nReal estate market formalisation\nIndia - Long-Term Structural Forces / Formalisation",
                "word_count": 26
            },
            {
                "page_number": 32,
                "text": "32\nFrom B2C to B2B we are seeing branded products gain market share\nSource: Jefferies, Vedant Fashions DRHP\nFans market shift\nWedding and celebration-wear shift\nCables and wires shift\nIndia - Long-Term Structural Forces / Formalisation",
                "word_count": 36
            },
            {
                "page_number": 33,
                "text": "India\n➔\nConsumption and services dominate our GDP \n➔\nIndia is formalising, steadily. \n➔\nIndia doesn’t save enough.\n➔\nWhy land issues mean India hoards up on gold.\n➔\nIndia doesn’t invest in human capital\n➔\nIndia’s manufacturing playbook is good, but not \ngreat\n➔\nHow DPI made India a Digital Welfare State\n➔\nHow India1’s savings surplus spur an Equity and \nF&O boom\nLong-Term Structural Forces \nIndia doesn’t save \nenough\nIndia’s savings is good but not \ngreat. A high savings rate is \nnecessary given low FDI rates. A \ndeep dive into savings illustrates \nthat the culprit is financial savings \n(as opposed to physical savings), \nand the reason is rise in financial \nliabilities, chiefly led by rising \n(unsecured) personal loans.\nIndia - The Last Five Years Pg 7\nConsumption Pg 66\n33",
                "word_count": 132
            },
            {
                "page_number": 34,
                "text": "34\nWorryingly, household savings, the biggest contributor, is seeing a declining share\nIndia’s overall savings rate looks ok, but is not\nSource: Jefferies, Economic Survey, MOSPI, RBI\nIndia - Long-Term Structural Forces / Savings\nHousehold financial savings dropped from 10.1% \nto 5.% primarily as a result of financial liabilities \nincreasing from 2 to 5.8% in the same period.\nHousehold savings make up the majority of savings. \nThey have been steadily declining (barring a \npandemic-induced rise in ‘21)\nIndia has a much lower savings rate \nthan its Asian peers, \nespecially China\nA key reason for household savings \nshare dropping is the drop in \nfinancial savings\nHousehold share of savings has \ndropped from 84% in FY00 to just \n61% in FY23! \n30%\n18.4%",
                "word_count": 121
            },
            {
                "page_number": 35,
                "text": "35\nSource: CLSA, BIS, IIF\nSharp rise in indebtedness of the Indian household\nDriven by the increasing share of \nconsumer loans in credit market\n3/4th of household debt is non-housing \ndebt which is high relative to others\nMeanwhile, household debt to GDP \nhits an all-time high\nIndia - Long-Term Structural Forces / Savings",
                "word_count": 53
            },
            {
                "page_number": 36,
                "text": "Increasingly, NBFCs including fintechs and not banks lead the sourcing, typically digitally\nMuch of the indebtedness is due to the rise in Small Ticket \nPersonal Loans (STPL)*\nMuch of it is led by Small Ticket Personal \nLoans (STPL) or loans under ₹100,000\nAverage personal loan size is a fourth \nof what it was\nNBFCs including digital lenders\n dominate sourcing\nLeading to a dramatic 48x rise in STPL loan \nvolumes since 2017\n*Small Ticket Personal Loans or STPL is loans below ₹100,000/-. Source: CRIF Highmark - How India Lends\n6x rise in Personal Loans origination \n(value) over last 7 years\nBut a 22x rise in number of loans originated \n(volume)\n36\nIndia - Long-Term Structural Forces / Savings",
                "word_count": 117
            },
            {
                "page_number": 37,
                "text": "India\n➔\nConsumption and services dominate our GDP. \n➔\nIndia is formalising, steadily.\n➔\nIndia doesn’t save enough.\n➔\nWhy land issues mean India hoards up on gold.\n➔\nIndia doesn’t invest in human capital.\n➔\nIndia’s manufacturing playbook is good, but not \ngreat.\n➔\nHow DPI made India a Digital Welfare State.\n➔\nHow India1’s savings surplus spur an Equity and \nF&O boom.\nLong-Term Structural Forces \nWhy land issues mean \nIndia hoards up on \ngold.\nIndia is the world’s second largest \nconsumer of gold. Behind this are cultural \nfactors, and economic factors, chiefly the \npoor land records, and the challenges in \ncollateralising land. Gold is a far more \nconvenient collateral as we see from \nthese slides.\nIndia - The Last Five Years Pg 7\nConsumption Pg 66\nThis section was authored by \nJoseph Sebastian, from Blume’s \nFintech team \n37",
                "word_count": 140
            },
            {
                "page_number": 38,
                "text": "India is the 2nd largest consumer of gold globally; and as Indians’ preferred savings instrument, gold's impact is seen \nacross our economy\nIndians have a special relationship with gold\nSource: gold.org, JM Financial, Business Standard\nBy contrast, other nations typically keep just \n2–3% of household wealth in gold vs India \nwhich keeps as much as 16%\nIndia is the largest jewellery market in the \nworld; thanks in part to India’s wedding industry\nLarge gold imports significantly impact \nour Current Account Deficit (CAD), in turn \ninfluencing rupee strength and policy \ndecisions \nIndia is the second largest \nconsumer of gold in the world\n1\nSo much so that it has material impact \non our current account deficit\nAfter property, gold accounts for the \nlargest share in household assets\n2\n3\n38\nIndia - Long-Term Structural Forces / Gold",
                "word_count": 136
            },
            {
                "page_number": 39,
                "text": "For borrowers, no credit history is \nrequired as gold is a secure product so \nthey can get loans very easily.\nWhy is gold preferred? Not just because of its cultural significance \nbut also because it is a great collateral\nIn rural communities, gold is the \nprimary way to save\nAccessible credit for borrowers\nTrusted collateral for lenders\nFor farmers and traders, gold acted as a \npractical cash flow tool. They purchase \ngold during periods of surplus and use it \nas collateral for loans during times of \ncash requirements.\nFor lenders, gold-backed loans offer a \nsignificant advantage since the collateral \nis relatively simple to repossess if \nneeded and It can be quickly sold in \ncase of default.\n1\n2\n3\nSource: Fortune India, Indian Express, Financial Express\n39\nIndia - Long-Term Structural Forces / Gold",
                "word_count": 134
            },
            {
                "page_number": 40,
                "text": "What makes gold even more attractive in India, is that land in India is \nnot a good source of collateral\nIndia has one of the smallest \nhousing loan market\nOne of the main reasons for that is \nIndia’s dispute resolution / contract \nenforcement mechanism is broken\nWhich makes India one of the lowest in \nthe world in contract enforcement\nSource: World Bank\nThere are a whopping 47 million pending cases \nin the Indian courts. 66% of these are estimated \nto be linked to land as per Daksh India.\nEconomic growth stories in places like South \nKorea depended on credit creation through the \nmortgage industry. India's housing mortgage \nmarket is far lower than other countries \nbecause property is a more complex form of \ncollateral compared to gold.\nChina\n#5\nUnited \nStates\n#17\nBrazil\n#58\nVietnam\n#68\nKenya\n#89\nIndia \n#136\n#190\nWith one of the world's smallest housing loan market and lengthy contract enforcement (1,445 days), gold emerges as the \npractical collateral choice because land can’t\n1\n2\n3\n40\nIndia - Long-Term Structural Forces / Gold\nWeak contract enforcement reduces the \nconfidence amongst lenders that property can \nbe repossessed easily in the event default, thus \nmaking land an inefficient form of collateral",
                "word_count": 202
            },
            {
                "page_number": 41,
                "text": "India\n➔\nConsumption and Services dominate our GDP. \n➔\nIndia is formalising, steadily.\n➔\nIndia doesn’t save enough.\n➔\nWhy land issues mean India hoards up on gold.\n➔\nIndia underinvests in human capital.\n➔\nIndia’s manufacturing playbook is good, but not \ngreat.\n➔\nHow DPI made India a Digital Welfare State.\n➔\nHow India1’s savings surplus spur an Equity and \nF&O boom.\nLong-Term Structural Forces \nIndia underinvests in \nits human capital\nBehind India’s underinvestment in human \ncapital, is a set of complex interlinked \nfactors but chiefly path dependence from \nits decision post-1947 to invest in the \ntertiary education sphere over the \nprimary and secondary education sphere \n(unlike the Asian Tigers and China which \ninvested in primary and secondary \neducation over tertiary) and developed a \nskilled labour force.\nIndia - The Last Five Years Pg 7\nConsumption Pg 66\n41",
                "word_count": 140
            },
            {
                "page_number": 42,
                "text": "Source: Jefferies, PLFS (2023-24)\nUnemployment Rate is per usual status , i.e. if a person worked 30 days in a year, they are considered as employed for the year\nIndia - Long-Term Structural Forces / Human Capital\nIndia’s Labour Landscape Snapshot\nNuances of India’s Workforce\n326.5 Mn\n110.7 Mn\n70.3 Mn\n51.0 Mn\n20% Casual Workers\n58% Self-Employed \n(33% of self-employed are unpaid helpers in a household enterprise)\n3.2% Unemployed\n13% Regular Salary Employees without job contract\n9% Regular Salary Employees with job contract\n18 Mn\nPeers: % Regular Salary Employees in the Workforce\nRussia\n93%\nBrazil\n68%\nChina\n54%\nBangladesh\n42%\n42",
                "word_count": 103
            },
            {
                "page_number": 43,
                "text": "43\nSource: PLFS 2023-24, Trading Economics, IMF\nIndia has a disguised unemployment problem and a jobless \ngrowth problem\nAgriculture accounts for 46% \nof jobs in India…\nJobless growth in manufacturing\nDisguised unemployment in agriculture\n…but only contributes to 15% \nof GDP\nIndicating a problem of disguised unemployment.\nGiven manufacturing in India is more capital intensive than labour \nintensive, jobless growth is a likely scenario.\nIndia - Long-Term Structural Forces / Human Capital",
                "word_count": 72
            },
            {
                "page_number": 44,
                "text": "India’s youth unemployment rate by level of education (%), 2022\n44\nSource: ILO\nBut what’s worrying is higher the education level, higher the \nunemployment rate\nIndia - Long-Term Structural Forces / Human Capital",
                "word_count": 33
            },
            {
                "page_number": 45,
                "text": "45\nSource: Twitter / Pritesh Lakhani, Twitter / Haidar Naqvi, , ‘Accelerating India’s Development’ by Karthik Muralidharan\nBecause India’s youth want ‘AC’ jobs or government jobs\nEmployment (un)willingness\nWhy aren’t there enough \ngovernment jobs?\nEverybody wants a government job\nWe have fewer government jobs than our peers but \nthese are highly paid relative to the private sector. \nKarthik Muralidharan in his book ‘Accelerating \nIndia’s Development’ describes how government \nschool teachers are paid 5-10 times more than \nprivate school teachers. The high pay and job \nsecurity is a key reason for the high demand for \ngovernment jobs and the many years invested in \nwriting exams to break into these jobs.\nIndia - Long-Term Structural Forces / Human Capital",
                "word_count": 117
            },
            {
                "page_number": 46,
                "text": "46\nSource: CII, Twitter / Paul Novosad featuring the work of Nitin Kumar Bharti and Li Yang\nThe underlying issue? India under invests in its human capital\nEducation spending as a % of GDP\n (India vs Peers)\nFocus on humanities and social \nsciences over technical areas\nFocus on tertiary education while \nneglecting primary education\nIndia - Long-Term Structural Forces / Human Capital",
                "word_count": 62
            },
            {
                "page_number": 47,
                "text": "47\nSource: MacroTrends, Ministry of Skill Development,, Moneycontrol / Shankar Sharma\nIndia’s demographic dividend is underway. To take advantage of it we \nhave to focus on upskilling our workforce, and AI-proofing them!\nDemographic dividend is the phase in which the proportion of working-age population (typically ages 15-64) increases rapidly compared to number of \ndependents (children and elderly). India’s demographic dividend phase began in 2018 and will run till 2055. Japan’s was 1964-2004 and so on.\nIndia v Peers, GDP growth in first 7 \nyears of demographic dividend\nIndia has far fewer population that has \nundergone formal skills training\nUnfair but relevant comparison - India was \ngreatly impacted by COVID led GDP decline.\n“India's reliance on services has made it \na shining star in the emerging world. \nBut AI is a howitzer aimed squarely at \nthat prosperity. The effect AI will have \non India will be profound. Too much has \nbeen written, said and marketed about \nIndia's demographic dividend…All it \ntakes is $29.95 a month to morph it into \nDemographic Debt. Or Demographic \nDust.” \n - Shankar Sharma\nThe above is from a 2019 Ministry of Skill Development report. \nIt is very likely that India’s number has increased today.\nIndia - Long-Term Structural Forces / Human Capital",
                "word_count": 205
            },
            {
                "page_number": 48,
                "text": "India\n➔\nConsumption and services dominate our GDP. \n➔\nIndia is formalising, steadily.\n➔\nIndia doesn’t save enough.\n➔\nWhy land issues mean India hoards up on gold.\n➔\nIndia doesn’t invest in human capital.\n➔\nIndia’s manufacturing playbook is good, but \nnot great.\n➔\nHow DPI made India a Digital Welfare State.\n➔\nHow India1’s savings surplus spur an Equity and \nF&O boom.\nLong-Term Structural Forces \nIndia’s manufacturing \nplaybook is good, but \nnot great.\nIndia has struggled to grow its \nmanufacturing sector historically, though \nit is making a spirited attempt now using \nimportant bans, tariffs, and \nproduction-linked incentives. The journey \nhas been impressive but not as good as \nsay Vietnam’s.\nIndia - The Last Five Years Pg 7\nConsumption Pg 66\n48",
                "word_count": 123
            },
            {
                "page_number": 49,
                "text": "49\nSource: World Bank\nIndia has historically underperformed on the manufacturing front\nIndia also ranks well below its peers when comparing \nmanufacturing’s share of GDP\nIndian manufacturing’s share of GDP is at its lowest ever!\nIndia - Long-Term Structural Forces / Manufacturing",
                "word_count": 42
            },
            {
                "page_number": 50,
                "text": "50\nSource: Ministry of Skill Development, Bloomberg, SBI / YCharts\nBecause of land, labour and capital\nLow skill levels in the Indian labour force mean \nthat despite lower wages, the net impact is neutral \nas a lower-skilled workforce is less productive.\nIndustrial land is expensive in India vs other \nsimilar economies. Path dependence over history \nled by fragmented of land parcels, unclear title \nrights etc., explain the higher cost of land \nacquisition. Below chart from a Bloomberg \narticle by Andy Mukherjee.\nLending rates are much higher in India vs \nother countries - SME loans are at low double \ndigit whereas Chinese companies get at 4%. \nMultiple reasons abound, but essentially India has \nhigher cost of capital.\nGovernment overheads are \nsubstantially higher in India!\nThe above is from a 2019 Ministry of Skill \nDevelopment report. It is very likely that \nIndia’s number has increased today.\nLabour\nCapital\nLand\nLand costs \nare 25% \nhigher!\nIndia - Long-Term Structural Forces / Manufacturing",
                "word_count": 159
            },
            {
                "page_number": 51,
                "text": "51\nSource: Reuters, Hindu BusinessLine, Business Standard, Times of India, Nuvama, Business Today\nIndia is looking to rework its trajectory by the use of bans, tariffs, \nand incentives\nImport bans to promote making in India in \ndefence, electronics. and durables\nProduction-Linked Incentives (PLIs) worth \n$33bn over 5 years across 14 sectors\nHigher tariffs than emerging market peers \nlike Brazil, Vietnam and China\nIndia tariffs at 11% higher than other Emerging \nMarket peers such as Brazil (9%), Vietnam \n(5%), and China at 3%\nIndia - Long-Term Structural Forces / Manufacturing",
                "word_count": 89
            },
            {
                "page_number": 52,
                "text": "52\nSource: Jefferies, The Wire, Business Standard\nAnd the effects are beginning to be seen in various industries\n“Electronic manufacturing sector is an example \nof the change that the scheme is bringing. Seven \nyears ago we used to import mobile phones of \napproximately USD 8 billion. Today, we are \nexporting mobile phones worth USD 3 billion” - \nPM Narendra Modi, 15 August 2021 speech\nFrom FY20 to FY24, India raised tariffs \non imported toys from 20% to 70%, \nleading to India becoming a net exporter\nImport bans have reduced home air \nconditioner imports from 45% to 5%\nTariffs played a huge part to make toys \nexport possible\nElectronics industry supported by PLI \nscheme has seen exports take off\nIndia - Long-Term Structural Forces / Manufacturing",
                "word_count": 125
            },
            {
                "page_number": 53,
                "text": "Source: JP Morgan, US Census website\nWhile India’s Import to US increased by \n60%, Vietnam saw a ~3x jump as \ncompared to India.\nChina has seen a drop of nearly $100 \nbillion in its exports to the U.S\nBut we weren’t the prime beneficiaries of China + 1; Vietnam very likely was!\n53\nIndia - Long-Term Structural Forces / Manufacturing\nThat said we are still in the early days of a manufacturing revival",
                "word_count": 73
            },
            {
                "page_number": 54,
                "text": "India\n➔\nConsumption and services dominate our GDP. \n➔\nIndia is formalising, steadily.\n➔\nIndia doesn’t save enough.\n➔\nWhy land issues mean India hoards up on gold.\n➔\nIndia doesn’t invest in human capital.\n➔\nIndia’s manufacturing playbook is good, but not \ngreat.\n➔\nHow DPI made India a Digital Welfare State.\n➔\nHow India1’s savings surplus spur an Equity and \nF&O boom.\nLong-term Structural Forces \nDPI has helped India \nbecome a ‘Digital \nWelfare State’\nA good way to understand India is as a \nDigital Welfare State, one that leverage \nDPI protocols to deliver cash and in-kind \nbenefits directly to the end users. Not all \nDPI protocols necessarily succeed, and \nwe are beginning to see second-order \neffects of DPI policies emerge!\nIndia - The Last Five Years Pg 7\nConsumption Pg 66\n54",
                "word_count": 134
            },
            {
                "page_number": 55,
                "text": "India - Long-Term Structural Forces / DPI\nThanks to DPI, India is now a digital welfare state\nSource: Motilal Oswal, DBT Website, People by WTF\nGovernment has introduced a slew of DPIs…\n…driving socio-economic impact through DBTs\n“Today, in just 30 seconds, I can \ndirectly transfer money into the \naccounts of 100 million farmers. \nToday, I can send subsidy to 130 \nmillion gas cylinder consumers with \njust one click, in 30 seconds. Billions \nthat were being siphoned out due to \ncorruption are now saved.” \n - PM Narendra Modi\nAadhaar (Unique \nID) + Mobile + \nBank Account \n(Jan Dhan \nAccount) has \nenabled direct \nbenefit transfers \nand reduced \nleakages in the \nsystem.\nPeople by WTF, Nikhil Kamath\nAadhar\n1382 mn\nusers in 2024\nUPI\n330 mn\nusers in 2023\nBHIM\n217 mn\nusers in 2023\nDIGIT\n250 mn\nusers in 2022\ne-Sanjeevani\n148 mn\nusers in 2023\nCo-WIN\n1190 mn\nusers in 2023\nABHA\n440 mn\nusers in 2023\nAA\n25 mn\nusers in 2023\n2000\n2016\n2018\n2019\n2021\n2022\nONDC\n700k sellers\n150 mn \ntransactions\n55",
                "word_count": 176
            },
            {
                "page_number": 56,
                "text": "As DPI protocols flood the market, some find immediate success \nwhile others are yet to find their feet\nSource: NPCI Website, ONDC Website, NASSCOM\n# of Mobility Orders\n# of Retail Orders\nNumber of users on MyGov is on the rise,but the \nactual penetration is quite low at 2% of population\nWhile mobility players on ONDC have seen success, \nretail is still finding its feet\nUPI is the runaway hit product of India Stack\nUPI\nONDC\nMyGov\n56\nIndia - Long-Term Structural Forces / DPI",
                "word_count": 85
            },
            {
                "page_number": 57,
                "text": "June \n2024\nDec \n2024\n57\nSource: India Quotient, RBI Payments Systems Report , Moneycontrol, Techcrunch, \nAs UPI hits maturity, we are seeing its second order effects\nUPI winning market share \nfrom debit and credit cards\n…but 0% MDR taking out profit pools for \nPayment Service Providers\nUPI processed 172 billion transactions \nworth over ₹ 245 tn ($~3tn) in 2024. It \naccounted for 83% of all digital \ntransactions in 2024, compared to just \n34% five years ago.\n…and is beginning to impact demand for \ncash amongst the upper income tier…\nJune \n2024\nDec \n2024\nNPCI, in March 2023, introduced an interchange fee of \n1.1% on P2M transactions >Rs.2000 made via \nprepaid instruments like a mobile wallet or prepaid \ncard. While this is a small portion of the revenue pool, it \ncould signal the introduction of MDRs for other \ntransaction types.\nIndia - Long-Term Structural Forces / DPI",
                "word_count": 146
            },
            {
                "page_number": 58,
                "text": "India\n➔\nConsumption and services dominate our GDP. \n➔\nIndia is formalising, steadily.\n➔\nIndia doesn’t save enough.\n➔\nWhy land issues mean India hoards up on gold.\n➔\nIndia doesn’t invest in human capital.\n➔\nIndia’s manufacturing playbook is good, but not \ngreat.\n➔\nHow DPI made India a Digital Welfare State.\n➔\nHow India1’s savings surplus spur an equity \nand F&O boom.\nLong-term Structural Forces \nHow India1’s savings \nsurplus spur an equity \nand F&O boom. \nIndia - The Last Five Years Pg 7\nConsumption Pg 66\nIndia1’s surplus savings are finding their \nway into the equity market, creating the \n4th largest equity market, and the biggest \nequity derivatives market (by volume). \nSEBI has come down hard on the equity \nderivatives market (effectively ‘financial \ngambling’) and the impact is visible.\n58",
                "word_count": 132
            },
            {
                "page_number": 59,
                "text": "India’s affluent class has seen rising \ndisposable income and growth…\n59\nSource: CLSA, Jefferies, JM Financial\nIndia - Long-Term Structural Forces / Equity\nAs disposable income increases, equity emerges as a new way to \nsave for Indians\n1\nEquity’s share of HH savings \nhas more than doubled over \nthe last 10 years.\n…of which more and more is being \ninvested in public markets.\n…which over time this manifests in a \nsizeable savings pool…\n2\n3",
                "word_count": 75
            },
            {
                "page_number": 60,
                "text": "60\nSource: NSE, AMFI\nDomestic capital is increasingly driving the Indian stock market\nDomestic investor ownership of Indian \nstocks catching up steadily to Foreign \ninvestor ownership\n1\n…with around half of those inflows \ncoming from Mutual Fund SIPs\nDomestic institutional investor (DII) \nflows into Indian stock market at record \nlevels… \n2\n3\nIndia - Long-Term Structural Forces / Equity",
                "word_count": 59
            },
            {
                "page_number": 61,
                "text": "61\nSource: Bloomberg, AMFI\nBut until when can domestic monies drive the market?\nSIP cancellations to registrations have risen to 64% in \nApr-Dec24. In FY24 it was at 52%\nAs equity returns drop and FII continue to sell how long \ncan retail funds keep flowingII\nIndia - Long-Term Structural Forces / Equity",
                "word_count": 52
            },
            {
                "page_number": 62,
                "text": "62\nSource: NSE Pulse, BSE, Jefferies\nDid you know India is the largest derivative market in the world?\nThis is on the back of index options (e.g., Nifty, Bank Nifty \netc.) which has grown 26x over the last 6 years\nIndia is the largest derivatives contracts market globally\nADTO above = Average Daily Turnover. This chart shows the \naverage daily turnover of index options vs regular stock trading; \nwhile in FY19 index options was ~7% of regular stock trading, \ntoday it is over half!\nIndia - Long-Term Structural Forces / Equity",
                "word_count": 91
            },
            {
                "page_number": 63,
                "text": "63\nSource: Jefferies, Twitter / Rajesh Sawhney\nMuch of the volume is driven from short term speculative trades \ndone by retail investors\nAdditionally, 65% of all contracts were weekly rather \nthan monthly in nature, i.e., held for a maximum of \none week versus one month. Effectively derivatives are \ntreated as quasi-gambling products by ‘investors’.\nUnlike U.S. where most option trades \nare held for longer periods (hence \n‘outstanding’), India's trades are \nshort-term and hence settled fast.\nAnd this boom is mainly led by retail \ninvestors\nBecause of low premiums, there has \nbeen a boom in very short-term \ncontracts: 73% of (index option) trades \noccurred on the last day of expiry.\nIndia - Long-Term Structural Forces / Equity",
                "word_count": 116
            },
            {
                "page_number": 64,
                "text": "64\nSource: NSE Pulse, SEBI, Twitter / Alok Jain\nRetail participation in F&O trades shoots up, but more than 90% of \nparticipants lose money!\nAbove via a SEBI study on equity derivatives \nwhich concluded that in FY24, individuals lost ~ \n₹41,000crs / ₹410 Bn and about 91.1% of them \nmade net losses in F&O amounting to an \naverage of ₹1.2 lakh / ₹120k loss per person\nRetail participation in the derivative \nmarket have grown exponentially, going \nfrom <1mn in 2017 to closer to \n12mn in 2024\nPeople are making losses to the tune of \n10-15% of their income, says this tweet\nBut most individual investors lose \nmoney\nIndia - Long-Term Structural Forces / Equity",
                "word_count": 114
            },
            {
                "page_number": 65,
                "text": "65\nSource: Indian Express, Jefferies\nLeading to SEBI’s intervention; and the impact can be seen!\nAverage daily Index option contracts declined 37% in Dec’24 and a \nfurther 52% in Jan’25\nSEBI has increased lot sizes, reduced \nweekly contracts, mandated upfront \npremium collection etc to curb \nspeculative behaviour.\nAnd the effects have starting to be seen with decreased volumes and lower expiry day \ntrades\nIndia - Long-Term Structural Forces / Equity",
                "word_count": 70
            },
            {
                "page_number": 66,
                "text": "A deep dive into India’s consumption patterns, and the \nIndian consumer stack, including India1 and how it \nshapes the Indian consumer market.\n India\nConsumption\nIndia’s consumption numbers look good \non an overall basis, but not on a per \ncapita basis. We take a look at why this \nis so. We look at how India1, India’s top \n10%, drives the Indian economic engine, \nand find that India1 is not widening as \nmuch as deepening. Finally, we show \nhow India1’s high share of consumption \nshapes the India consumer market in \nmany distinct ways.\nConsumption Pg 66\nLong-Term Structural Forces Pg 20\nIndia - The Last Five Years Pg 7\n66",
                "word_count": 108
            },
            {
                "page_number": 67,
                "text": "Source: Twitter / Vivek Raju\n67",
                "word_count": 6
            },
            {
                "page_number": 68,
                "text": "68\nIt has consistently been above 55% since ‘00; Investment / GFCF plays a far lesser role unlike in China\nConsumption is the dominant driver of India’s GDP \nSource: Jefferies, World Bank \nIndia - Consumption\nHow we stack up vis-a-vis China\nGFCF is essentially creation of productive assets such \nas machinery, infrastructure. Unlike India, investment \n(GFCF) plays a larger role in China’s GDP at 41% vs. \nIndia’s 31%. \nNote: PFCE at 60.3% differs from PFCE of 56% on Slide #24; 60.3% is at current prices, while 56% was at constant prices (2011-12).\nIt is hard to get long time-series data for constant prices.",
                "word_count": 103
            },
            {
                "page_number": 69,
                "text": "69\nThis is how Indian Consumption stacks up\nSource: Bernstein, NSSO, Redseer\nGDP split\n(basis current prices)\nHow consumption \nsplits up\nHow retail breaks \ndown into segments\nGFCF\n30%\nGovt. \nExpenses \n& Others\n10%\nRetail\n$1.1 Tn \n55%\nServices\n$1 Tn \n40%\nOther Retail\n$270 Bn (27%)\nRestaurants\n$70 Bn (7%)\nFashion & BPC\n$110 Bn (10%)\n(Consumer Durables, Gems & \nJewellery etc)\nOnline (7%)\nOffline \n(93%)\nUnbranded \n(63%)\nBranded \n(37%)\nNon\nDiscretionary\n(71%)\nDiscretionary \n(29%)\nConsumption \n$2.1 Tn \n60%\nGrocery & FMCG\n$550 Bn (50%)\n We can also split retail in 3 other ways\nIndia - Consumption",
                "word_count": 98
            },
            {
                "page_number": 70,
                "text": "70\nRelative to large economies, India’s consumption growth is amongst the highest\n~60% of $3.7 trillion makes for a sizeable consumption market\nSource: UBS\nIndia is the 5th largest consumption market globally\nIndia’s consumption growth outpaced major global \neconomies\nIndia - Consumption",
                "word_count": 42
            },
            {
                "page_number": 71,
                "text": "71\nOn per capita basis though, India’s consumption metrics look \nless impressive \nSource: World Bank, CLSA \nWe are roughly \nwhere China was \nin 2010\nIndia vs Indonesia vs China: Consumption Expenditure Per Capita (in USD) \nIndia - Consumption",
                "word_count": 38
            },
            {
                "page_number": 72,
                "text": "72\nReflected in under penetration and under consumption across \nseveral categories, such as financial products…\nSource: CLSA\nSource: Jefferies\nSource: FT Partners\nAnon fintech founder: \n“35-40M unique card \nholders. But active will be \nin range of 22-28M”\nSource: BCG / Z47 \nWhile number of MF \ninvestors has risen of \nlate, penetration still \nremains low.\nIndia - Consumption",
                "word_count": 57
            },
            {
                "page_number": 73,
                "text": "73\n…and 2 Wheelers, Air-Conditioners, FMCG, Footwear…\nSource: Jefferies\nSource: CLSA / Technopak\nSource: Ola DRHP\nSource: Jefferies \nRural per-capita FMCG \nspends are even lower, \nat one third of urban.\nIndia accounts for \n~7% of global AC \nunits sold. China \nwas ~55%.\nIndia - Consumption",
                "word_count": 45
            },
            {
                "page_number": 74,
                "text": "74\n…and Cement, Electricity, Hotels, Tourism.\nSource: Jefferies\nSource: Jefferies, KPMG\nSource: Jefferies\nSource: CLSA\nSome of the data on the \ntable will shift post COVID \nas numbers are updated, \nbut in India’s case we don’t \nestimate the numbers to \nshift much basis recent \ntraffic data.\nIndia - Consumption",
                "word_count": 49
            },
            {
                "page_number": 75,
                "text": "75\nIndia - Consumption \nWhy does India consume so little? Why are penetration rates \nso low across so many categories?\nThe answer likely lies in the nature of the consumer economy structure, or the \nIndian consumer stack as we term it.",
                "word_count": 41
            },
            {
                "page_number": 76,
                "text": "India 1\n‘Mexico’\nIndia 2\n‘Indonesia’*\nIndia 3\n‘Sub-Saharan Africa’\nThe Consuming \nClass\n~30m households\n~140m people\n~$15K per person\nIndia1 is the consuming class, and effectively constitutes the \nmarket for most startups. Also most startups start here and \nthen expand to India2.\nThe Aspirant \nClass\n~70m households\n~300m people\n~$3k per person\nIndia2 is the emerging aspirant class. They are heavy \nconsumers and reluctant payers. OTT / media, gaming, \nedtech and lending are relevant markets for them. UPI and \nAutoPay has unlocked small ticket spends and transactions \nfrom this group.\nUnmonetisable\nUsers\n(& Non-Users)\n~205Mn households\n~1Bn people\n~$1k per person\nIndia3 doesn’t have the kind of incomes to be able to spend \nanything on discretionary goods. They are beyond the pale, \nas of now, for startups.\nSome apps straddle different \nIndias e.g., Whatsapp, Youtube, \nFlipkart etc. A good way to \nunderstand the above is that all \napps in India3 can be used by \nIndia2 and India1. Similarly \nIndia2 apps can be used by \nIndia1. The reverse isn’t true. \nIndia1 apps are not used by \nIndia2 or India3.\n* Indonesia’s per capita income is $5k; strictly this is not the right country analogy for India2, but we couldn’t get a country that has a population of ~300m \nwith a per capita income of $3k. So please bear with us for this. \nHow Blume looks at the consumer stack\n76\nIndia - Consumption\nSource: Blume Research",
                "word_count": 236
            },
            {
                "page_number": 77,
                "text": "77\nThis undersized consuming class is reflected in other estimates too…\nSource: Bernstein, UBS, Redseer \n790 mn \n(Income < $3.3K)\n430 mn \n(Income $3.3k - $6k)\n65 million \n(Income $6k -$12k)\n65 million \n(Income > $12k)\n538 million \n(Income < $1.5k)\n222 million \n(Income $1.5k - $2.5k)\n193 million \n(Income $2.5k - $5k )\n79 million (Income $5k - $10k)\n40 million (Income > $10k)\n525 million \n(Income < $3.5k)\n720 million\n(Income $3.5k - $14.2k)\n140 million \n(Income $14.2k - $25k)\n35 million \n(Income > $25k)\nNote: UBS has estimated the above for 15+ population only\nBernstein (2024)\nUBS (2023)\nRedseer (2022)\nIndia - Consumption",
                "word_count": 106
            },
            {
                "page_number": 78,
                "text": "78\nIndia1 is the engine of the Indian consumer economy\nSource: Blume / Bernstein estimates, Goldman Sachs\nIndian consumer stack by share of household \ndiscretionary spend\nIndia1\nIndia 2\nIndia 3\nBlume Consumer Stack\nHow the urban top 10% over index on consumption\n~10% of population\n2/3rd share of discretionary spends\n~23% of population \n1/3rd share of discretionary spends\n2/3rds of the population\nDip into their savings (slight negative \nshare of discretionary spends)\nThis means Urban India top 10% spends 13x of the average per capita \nspend on Durables, and so on.\nIndia - Consumption",
                "word_count": 95
            },
            {
                "page_number": 79,
                "text": "79\nHowever, India1 is not widening… \nSource: UBS, Citi, Zomato Quarterly Reports\nCOVID slowdown\nCOVID slowdown\nDomestic air passenger traffic has not \ngrown much after FY21-22 COVID \nslowdown\n2W sales volumes have remained muted \nfollowing FY21-22 COVID slowdown\nFood ordering MAUs\nIndia - Consumption",
                "word_count": 44
            },
            {
                "page_number": 80,
                "text": "80\n…as much as it is deepening.\nSource: CLSA, Jefferies, UBS \nRising share of premium and executive \nsegment motorcycles FY19 - FY23\nShare of high-end to ultra-luxury housing \nhas doubled in last five years\nLow-end smartphone sales contract as \nmid-premium segment expands\nIndia - Consumption",
                "word_count": 45
            },
            {
                "page_number": 81,
                "text": "81\nNot widening as much as deepening: A look at car sales in India\nSource: Autopunditz, CLSA \n4.5% CAGR\nSlow-growing passenger vehicle market…\n…with a sharp rise in premium segments\nIndia - Consumption",
                "word_count": 33
            },
            {
                "page_number": 82,
                "text": "82\nNot widening as much as deepening: A look at taxpayers in India\nSource: Direct Taxes Data, Government of India\nA small number of taxpayers are \nshouldering the tax burden\nIn FY23, only 2% Indians paid tax \n(and will go down further per the \nexemptions announced Feb’25). In \ncontrast: In China, ~10% paid tax, \nand in USA, ~43% paid tax.\nThe gap between tax filers and tax payers is widening. The recent \nbudget exemptions will further reduce the number of taxpayers.\nIndia - Consumption",
                "word_count": 84
            },
            {
                "page_number": 83,
                "text": "83\nRising share of incomes, and presence atop wealth charts validate \nthe India1 deepening story\nSource: UBS, World Inequality Lab\nIndia’s wealth growth rates were the fifth highest globally\nIndia1’s share of national income has steadily increased\nMiddle 40%\nTop 10% \nBottom 50%\nIndia - Consumption",
                "word_count": 46
            },
            {
                "page_number": 84,
                "text": "84\nIndia1’s high share of consumption shapes the Indian \nconsumer market in many distinct ways.\nIndia - Consumption",
                "word_count": 18
            },
            {
                "page_number": 85,
                "text": "85\nIndia1 is helping spark a fast-growing equity market…\nMarket cap to GDP ratio touching all time highs (in %)\nAnnual SIP contributions are at all time high (in INR trillions)\nNSE investors (Equity + F&O) up 5x from 2019 (in millions)\nEquity share in household savings up 2.5x in a decade (in %)\nSource: CEIC\nSource: AMFI\nSource: NSE Market Pulse\nSource: Jefferies\nIndia - Consumption\n$~25 Bn \nin FY25",
                "word_count": 71
            },
            {
                "page_number": 86,
                "text": "86\n…as well as the rise of the experience economy…\nSource: BookMyShow numbers via Yourstory, MediaBrief, CNBCTV18, Fortune India\nTweets by Chandra Srikanth, Anup Pandey, Akshita Iyer, Spadika Jayaraj\nBookMyShow - Events and attendance\nA frenzy for getting tickets for the recent Coldplay concerts\nGrowth in number of events\nGrowth in event attendance, (in millions)\nIndia - Consumption",
                "word_count": 58
            },
            {
                "page_number": 87,
                "text": "87\nSource: UBS, RBI Bulletins\nIncreased hotel consumption despite rising inflation\nAverage hotel booking transaction \nsize on MakeMyTrip (in USD)\n“When Oberoi Udaivilas opened two decades ago in Udaipur, eight per cent of \nthe occupants were Indians, the rest foreigners. By 2018, the Indian occupancy \nat the luxury hotel was at 52%. “ - Atlas of Affluence\nNumber of hotel booking \nmade on MakeMyTrip (in millions)\n% Share of Travel and Education in Total \nOutward Remittances under LRS\nTotal remittance increased from $1.3 Bn in FY15 to $31.7 Bn in FY24. \nThis means $17 Bn is Travel-related remittances in FY24 (at 53.6% of \ntotal; incidentally this was $~7 Bn in FY20). This includes all credit \ncard spends while abroad as well as travel agents booking holiday \npackages etc., which are classified by banks under LRS. \nIndia1’s travel mania is reflected in the sharp \nrise in travel remittances under LRS!\nIndia - Consumption\n…a key aspect of which is travel…",
                "word_count": 159
            },
            {
                "page_number": 88,
                "text": "88\n…and the creation of homegrown premium / luxury brands in \nseveral categories…\nLeveraging traditional strengths in \ntextiles and ayurveda, reinterpreting \nit for contemporary India.\nLeveraging India1’s desire for world \nclass products with an Indian soul and \naesthetic sensibility.\nLeveraging India1 as the 51st state of \nthe US in tastes and aspirations, \nand using it as a springboard \nto launch globally.\nIndia - Consumption",
                "word_count": 64
            },
            {
                "page_number": 89,
                "text": "89\n…and increasingly how our cities are evolving \nSource: Tweet\nIndia1 prefers gated communities to the ‘Civil Lines’ / Cantonments of their parents \nIndia - Consumption",
                "word_count": 26
            },
            {
                "page_number": 90,
                "text": "90\nGated Communities are concentrations of affluence \nSource: MyGate, Redseer\n40% households in Top 50 cities are gated \ncommunities. The consumption and spend \npower of these households contributes to \n>50% of Consumption Expenditure\nAccording to MyGate, 26% of spending by \nthese households is through online \nchannels.\nAll data in the charts below courtesy \nGated communities punch above their \nweight in Consumption expenditure\nHouseholds in gated communities are savvy \nonline shoppers\nPer capita household spending of gated \ncommunity households is on a steady rise\nIndia - Consumption",
                "word_count": 86
            },
            {
                "page_number": 91,
                "text": "91\nIndia1 is a ‘high income’ country within a country\nIndia1 in population size would be the 10th most \npopulous country\nBasis per capita income, India1 would be 63rd in the \nworld, well ahead of India (ranked 140th)\nSource: World Bank \nIndia1 is spread across urban and rural areas, not concentrated in specific regions (though there is less in East India). Given the dispersion, and the overall size of 10% of population, it \nhas less direct political influence. Its influence is manifested in its consumption behaviour and social media voice, as well as how it helps India project soft power abroad. In the coming \nyears, it will get richer, and the economic gap between it and India will widen. This will bring distinct challenges that we as a society will need to work together to overcome.\nIndia1 will be an advanced economy well before India overall becomes a developed country\nWith ~140mn people India1 \nwould be 10th globally in \npopulation size\nWith US$ 15K per capita \nincome, India1 would pass the \nWorld Bank’s $14K threshold \nfor “high income” status.\nIndia - Consumption",
                "word_count": 182
            },
            {
                "page_number": 92,
                "text": "Source: Twitter / Ritesh Banglani & Anmol Maini\n92",
                "word_count": 9
            },
            {
                "page_number": 93,
                "text": "Section II: Indus Valley",
                "word_count": 4
            },
            {
                "page_number": 94,
                "text": "94\nSource: Twitter / Ashish Sinha\nIndus Valley in one tweet\nUber was forced to make a change to its \ntraditional revenue model (commission on \nthe fare paid) for (3-wheeler) autos in \nIndia. \nNamma Yatri, an Indian startup leveraged \nthe open source Beckn protocol (part of \nIndia Stack / Digital Public Infra ) to build \na mobility solution where the revenue \nmodel was to charge a daily (or monthly) \nfee for drivers for the app, and not take a \nslice of the fare paid. The success of this \nmodel has forced all the other mobility \nplayers (Rapido, Ola, and now Uber to \nfollow suit). \nThe tweet shows how first-world revenue \nmodels have to adapt to the unique \nneeds of the Indian market, the rise of \nDPI, and DPI-native revenue models.",
                "word_count": 130
            },
            {
                "page_number": 95,
                "text": "Venture funding trends, and a deep dive, followed by a \nlook at India’s unicorns, and the venture debt market.\n Indus Valley\nIndus Valley - Funding Trends\nA deep dive into the Indian venture \nmarket, including contrasts with China \nand USA, along with stage-wise funding \nanalysis. We then do an analysis of \nunicorns, and attempt a count of the true \nnumber of unicorns. We wrap this with a \nloop at startups flipping back to India, to \nlist here, and finally, track the rise of \nventure debt.\nIndus Valley - Funding Trends \nIPO Boom Pg 111\nSector Deep Dives Pg 120\nIndus Valley Playbooks Pg 157\n95",
                "word_count": 105
            },
            {
                "page_number": 96,
                "text": "96\nSource: Dealroom\nVenture Capital investments in startups over the last 5 years (in USD billion)\nIndus Valley - Funding Trends\nState of global venture market - US has bounced back strongly, \nIndia seeing signs of revival",
                "word_count": 37
            },
            {
                "page_number": 97,
                "text": "Remember, this was pre-DeepSeek China! \n97\nWhile US saw large rounds thanks to AI, China was in a funk\nSource: Dealroom, Bloomberg, Financial Times\nLarge rounds back in the US, thanks to AI!\nWhile US share of global funding went up, India and \nChina remained muted\nChina’s venture funding trended downward (this was pre-DeepSeek!)\nAI funding alone was a \nrecord $97 Billion of this - \nmaking up to 80% of the \ntotal funds raised in large \nrounds.\n (Bloomberg)\nIndus Valley Funding\nIndus Valley - Funding Trends",
                "word_count": 86
            },
            {
                "page_number": 98,
                "text": "98\nIndia's VC market following 2023 trendlines broadly\nSlight uptick in funding but nowhere near 2021, 2022 levels; in large part due to absence of late stage capital.\nAverage number of rounds : 2,311\n3,435\n3,315\n2,267\nSource: Tracxn\nTracxn updates the database continuously and hence the 2024 number may change in the future; still this snapshot should give you a directional sense of funding trends. Pls do note that each database may \npresent data differently depending on how they categorised certain transactions. You may see numbers differ from chart to chart depending on the database; that said the broad trendline should hold!\n1,721\nIndia Venture Capital Investments (in USD billion)\nIndus Valley Funding\nIndus Valley - Funding Trends",
                "word_count": 119
            },
            {
                "page_number": 99,
                "text": "99\nA stage-wise analysis of India's VC Market \nSource: Tracxn\n2024 mirrors 2023 patterns: Seed saw a small drop, Early and Late stages show modest gains but far below peak levels\nHow Seed, Early, and Late Stage financing stacks up (in USD billion)\nIndus Valley Funding\nIndus Valley - Funding Trends",
                "word_count": 51
            },
            {
                "page_number": 100,
                "text": "100\nSeed funding continues on trendlines - fewer rounds, larger checks\nSource: Tracxn\nSeed funding split by stages per year \nThe average seed round is $1 mn (~3x of what it was in 2017). The number of \ncompanies able to raise a seed round have been decreasing steadily since 2021. In \n2021, about 2,513 raised a seed round while in 2024 only 1,078 raised. The biggest \ndrop was in the <$1 mn segment (37% down). $1-3m saw a 22% drop.\nThe ‘mango seed’ is here to stay \nFrom <10% to 50% of total funding (USD million)\nLarger seed rounds or ‘mango seeds’ (>$3M) now make up 50% of funding, while <$1M rounds drop to one third of 2017 \nlevels. This is led by second time founders, and elite operators, raising larger formation cheques.\n<$1mn seed rounds have decreased by a third from 2017 \nIndus Valley Funding\nIndus Valley - Funding Trends",
                "word_count": 151
            },
            {
                "page_number": 101,
                "text": "Deeptech / Life Sciences\nConsumer\nStudent-focussed\nAll Sector\nSaas / DevTools\nThe Early-Stage funding gap is fueling the rise of MicroVCs\nBetween angels and choosy seed funds, a new stage (pre-seed), and backer (the MicroVC), is emerging\nRise of Specialised MicroVCs\nMicroVCs have created their niche in early Seed stage\n What has led to the rise of MicroVCs?\nAs Seed / Multistage funds get choosy and prefer to focus on elite \nfounders, a gap is opening up in funding for first-time founders, which \nis being filled by MicroVCs.\nHow are MicroVCs different?\n➔\nHave a special focus or highly evolved thesis in a particular \ndomain\n➔\nThere are over 100 MicroVCs (many founded recently) \ntypically investing $100k-$500k at seed / pre-seed stage. \nThese funds invest at valuations of $1M-$8M, taking 3-8% \nstakes in startups, sometimes more.\nSource: Blume analysis;\n101\nIndus Valley Funding\nIndus Valley - Funding Trends",
                "word_count": 148
            },
            {
                "page_number": 102,
                "text": "102\nSeries A/B funding: Stable check sizes, fewer rounds, longer \nintervals\nSource: Tracxn\nStartups raising Series A / B has reset to 2017-18 \nlevels, showing a clear reversal of the 2021-22 surge\nEarly stage funding across A and B has halved from 21’ & 22’, but the average round size has stayed the same. Effectively \nthe number of investments, and the number of companies graduating to A & B stages have halved.\nTime to fundraise has increased, especially for \nSeries B rounds, which now take 9 months \ncompared to 2017, while Series A rounds take 4 \nmonths longer \nSlight uptick in funding but nowhere near \n2021 / ‘22\nTime between rounds is steadily rising\nRound sizes stay flat but the number of \ncompanies raising series A or B reduced \nby 30% (vs 2022)\nIndus Valley Funding\nIndus Valley - Funding Trends",
                "word_count": 141
            },
            {
                "page_number": 103,
                "text": "Startups backed by seed funds taking longer to raise follow-on rounds as compared to ones backed by multistage funds\n103\nTime between rounds: Seed vs multistage fund-backed startups \nSource: Tracxn\nSeed to Series A\nSeries A to Series B\nIndus Valley Funding\nIndus Valley - Funding Trends",
                "word_count": 47
            },
            {
                "page_number": 104,
                "text": "$50m+ rounds remain subdued while overall late stage contribution drops to 59% of total funding\n104\nLate Stage remains lacklustre\nSource: Tracxn\nA thriving venture market like US has about 70/75% late stage funding as more \ncompanies keep growing and require more growth capital.\nMore than half of these \nrounds have been from \ncompanies which raised a \nmuch larger round before.\n$50m+ rounds are still down from their ‘21 highs\nLate Stage rounds as % of total funding is close to where it \nwas in 2016 \nIndus Valley Funding\nIndus Valley - Funding Trends",
                "word_count": 94
            },
            {
                "page_number": 105,
                "text": "India added 6 unicorns is 2024, an improvement from last year’s 2 \n105\nIndia is the 3rd largest unicorn factory…\nSource: Bain, Tracxn\nSlim pickings on the Unicorn-creation front, after the go-go \nyears of 2020-22 \nIndia is the third largest in total unicorn count\nIndus Valley Funding\nIndus Valley - Funding Trends",
                "word_count": 52
            },
            {
                "page_number": 106,
                "text": "Based on our analysis only 91 out of our 117 Unicorns are truly worth >$1bn\n106\nBut do we really have 117 Unicorns?\nSource: Blume Analysis, Tracxn\nGoing Steady\n(54)\nValued Under $1Bn\n(20)\nGoing Public\n(19)\nPublicly Listed\n(14)\nAcquired (7)\nBootstrapped or Founder Owned\nPublicly Listed\nGoing Public\nValued under $1Bn\nGoing Steady\nAcquired\nGreater than\n$1Bn\nLess than\n$1Bn\nLess than\n$1Bn\nFounder Owned (3)\nGreater than\n$1Bn\nIndus Valley Funding\nIndus Valley - Funding Trends",
                "word_count": 79
            },
            {
                "page_number": 107,
                "text": "107\nSource: Indian Express, Outlook Business, Khaitan & Co\nRegulatory changes and strong public markets drive foreign-incorporated startups to return to India\nPhonepe tax bill would make it the 10th \nhighest tax paying company in India in \nFY23\nCompany\nTax Paid\nPhonepe\n$1 Bn\nGroww\n$160 Mn\nRazorpay\n$200 Mn\nZepto\nUndisclosed\nEven more are in the process of reshoring\nIndian companies want to list in the \nfriendlier Indian public market\nSimpler tax norms and policies for them \nto operate.\nIndustry regulations which favour indian \nregistered company (especially fintech \nand ecommerce companies)\nPaying huge tax bills in order to do so\nBut why?\nIndus Valley Funding\nAn emerging trend with late stage startups has been the reverse \nflip back to India \nIndus Valley - Funding Trends",
                "word_count": 126
            },
            {
                "page_number": 108,
                "text": "108\nWhy did they register abroad in the first place?\nSource: Twitter / Anu Hariharan, Linkedin / Rehan Yar Khan \nDifficulty in raising capital domestically\nPlanned to list on the US public market\nIndus Valley Funding\nIndus Valley - Funding Trends",
                "word_count": 41
            },
            {
                "page_number": 109,
                "text": "Longer fundraising cycles and tighter equity markets are making startups tap into venture debt\n109\nVenture Debt becomes more common as equity funding tightens up\nSource: Stride Ventures\nImplication of raising Venture Debt:\n➔\nHigher Liquidation Preference: Venture debt typically comes with priority claims on company assets and cash flows, over equity holders\n➔\nEquity-Dependent Credit Lines: Available venture debt limits are often tied to equity reserves, creating potential downward spirals if equity positions \nweaken\n➔\nRisk of Negative Cycle: As equity funding becomes harder to secure, venture debt capacity may shrink exactly when companies need it most.\nVenture Debt has picked up sharply over the last 7 years\nVenture Debt has grown from <1% of venture funding to 11%\nIndus Valley Funding\nIndus Valley - Funding Trends",
                "word_count": 128
            },
            {
                "page_number": 110,
                "text": "Westbridge investment in WACA (Westbridge Anand Chess Academy) has put Indian chess on the world map. WACA \n‘facilitates mentorship to emerging and established chess players in India’ with the hope of creating more world champions. \n110\nSometimes the best investment is in people, not the company\nSource: linkedin/ Sandeep Singhal, Youtube/ Chessbase India\n Behind Indian Chess champions is Westbridge’s WACA \ninitiative\nWestbridge partnered with Vishy Anand to create initiative \nIndus Valley Funding\nIndus Valley - Funding Trends",
                "word_count": 77
            },
            {
                "page_number": 111,
                "text": "A deep dive into India's booming IPO market, as well as \nthe SME IPO’s rise, including what it implies for \nfounders.\n Indus Valley\nIPO Boom \nIndus Valley - Funding Trends Pg 95\nIPO Boom \nIndus Valley Playbooks Pg 157\nSector Deep Dives Pg 120\nA deep-dive into India’s record-breaking \nIPO market, looking at the performance \nof IPOs, exploring how barriers to list are \ncoming down, as well as the rise of the \nSME IPO Market.\n111",
                "word_count": 76
            },
            {
                "page_number": 112,
                "text": "(India)\n(Japan)\n(Hong Kong)\n(Shanghai)\nBoth the number of IPOs and issue sizes reach record levels\n112\n2024: A record-breaking year for Indian IPOs\nSource: NSE Market Pulse\nHyundai Motor India was the largest-ever IPO in \nIndia, raising ₹27,870 crore (US$~3bn). It was also \nthe second-largest IPO globally in 2024.\n(India)\n(US)\n(US) (Hong Kong)\n(Shanghai)\nOf the 268 IPOs on NSE in India, 90 of them were \nMainboard listing vs 178 SME (NSE Emerge) IPOs\nIndus Valley - IPO Boom\nIndia saw its best year in equity \nfunding raised via IPOs\n1\n…as well as the highest capital \nraised via IPOs across the world\nIndia led in IPO activity globally,\nwith a 23% share of total listings…\n2\n3",
                "word_count": 120
            },
            {
                "page_number": 113,
                "text": "Companies are going public earlier; with 42% lower revenue and 37% lower market cap compared to 2018 levels\n113\nIndian public markets: Becoming more accessible, earlier\nSource: Blume - Insights from a decade of Indian Mainboard IPOs | Part 2\nMedian revenue at listing has decreased 42% since 2018\nMedian market cap at listing has reduced 37% since 2018\nIndus Valley - IPO Boom",
                "word_count": 64
            },
            {
                "page_number": 114,
                "text": "114\nMarket cap data as on 17th January 2025 via NSE. The number of venture funded IPOs here includes post-IPO VC funding. The number includes 3 VC funded companies listed \nabroad - Freshworks, ReNew, and MakeMyTrip. The IPO list was taken from Tracxn. This number includes a total of 14 VC funded SME IPOs.\nPre 2011\n2021\n2025\n50\n37\n80\nVC-funded companies that have gone IPO, pre and post ‘21\nThere has been a history of VC backed IPOs!\nIndia has a long history of venture-funded IPOs\nOver 160 venture-backed companies have gone public thus far, with post-2021 IPOs raising more than double the capital of \nall previous listings\nIndus Valley - IPO Boom",
                "word_count": 115
            },
            {
                "page_number": 115,
                "text": "115\nVenture funded companies that IPO’d 2021 to 2024: A status check\nSource: Nuvama Alt & Quant Research, all data as of 22nd January 2025\nSmaller IPOs (<$1 Bn) dominate with 2/3rd of listings; they have also performed relatively better while larger listings show \nmixed performance; Swiggy signals renewed appetite for big tech offerings\n2/3rds of IPOs in last four years have \nbeen of companies with <$1 Bn Mcap\n1\nVenture-funded co market caps \ndropped ~5% (since IPO day), but \n<$1Bn market cap companies saw a \ngain of 25%\nLarge listings made a comeback in \n2024 thanks to Swiggy\n2\n3\nIndus Valley - IPO Boom",
                "word_count": 106
            },
            {
                "page_number": 116,
                "text": "116\nSource: Live Mint, Money Control\nSME IPO market outperforms Sensex IPO index by 5x, driving record issues, raise and retail participation\nThe number of issues have grown from 68 \nin 2016 to 236 (includes both BSE SME and \nNSE Emerge) in 2024\nSME IPOs saw their biggest year in \nissues and raises \n1\nDriving a lot of retail demand\nSME IPO Index returned 5x over the \nBSE IPO Index\n2\n3\nIndus Valley - IPO Boom\nSME IPO is a potential exit route companies for well-performing \ncompanies that don’t get late stage venture love!",
                "word_count": 95
            },
            {
                "page_number": 117,
                "text": "+₹3 Bn \nMarket Cap\n1 Year\n+₹40 Bn\nMarket Cap\n6 Years\nWith 1 in 3 SME IPO-listed companies graduating to the Mainboard, SME platform demonstrates strong outcomes, putting a \nvery strong case forward for more VC-backed companies to go this route.\n117\nSME IPOs: An untapped opportunity for VC-backed companies\nNote: Market Cap calculations for the 14 Venture Funded SME IPOs in India do not include 3 that have migrated to the mainboard (E2E, AVG, Deccan Healthcare)\nSource: Blume - Learnings from Indian SME IPOs, BSE SME Board website, NSE Emerge website, Tracxn \n14 VC funded companies have IPO’d on the SME board with a total mcap of ~ ₹50 Bn; \nabout 1.5% of total mcap of the SME board\n6 Years\n+₹3 Bn \nMarket Cap\n<1 Year\n+₹6 Bn\n Market Cap\nBlume was a seed \ninvestor and the \nonly institutional \ninvestor at IPO in \nboth E2E and \nInfollion!\nHow has the SME IPO market evolved\n➔\nSince 2012, the median SME IPO market cap has jumped 4.5x to ~₹1 Bn \n(2024) whereas median revenue at IPO grew 3x to ~₹700 Mn (2024)\n➔\nThe median offer size has grown 3x from ~₹80 Mn a decade back to ~\n₹250 Mn now\n➔\nOf the total capital raised, 90% has been through fresh offer / primary \ncapital \nOf 1,053 companies that listed on SME board, 31% have \nmigrated to Mainboard\nVC-funded SME IPOs have impressed post listing!\nIndus Valley - IPO Boom",
                "word_count": 243
            },
            {
                "page_number": 118,
                "text": "118\nFrom SME bourse to AI leader: E2E Networks growth story shows \ntech and VC potential on the SME boards\nSource: Company Documents, Financial Express, Business Standard, Upstox, \nMcap as of 13th Feb 2025\nE2E’s market cap is up 65x from the time of listing.\n➔\nE2E is a hyperscaling cloud provider also enabling access to \nNvidia GPUs, focused on the Indian market.\n➔\nIt was listed on the NSE Emerge (SME) board in May 2018 \nand migrated to the mainboard in April 2022. Blume was the \nonly institutional investor on the cap table.\n➔\nIn the last 2-3 years, it has been able to capitalise on the AI \ntrend by having exclusive access to the latest hardware.\nAbout E2E Network\nIndus Valley - IPO Boom",
                "word_count": 126
            },
            {
                "page_number": 119,
                "text": "119\nGuideline for founders mulling over an SME IPO\nSource: Blume - Learnings from Indian SME IPOs, NSE, Chittorgarh\nWhat is the eligibility criteria?\nWhat needs to be kept in mind for the SME IPO?\nA long-Term lens\nPublic markets are a marathon, not a sprint; you need to have a \ndecade-long time horizon when you think about going public.\nPredictability\nWhat public markets expect is predictability; they don't want any \nsurprises, so your business has to have stability and you should \nhave clear revenue foresight.\nWhy wait for a billion-Dollar IPO?\n You can continue to compound in public markets - if you grow \n20-25%, public markets would value you more than private markets.\nClarity on ‘use of funds’ \nIn private markets, it's fine if the capital you raise isn't used exactly \nas stated, but in public markets, you need to be very precise about \nhow the capital will be used since this will be audited\nCommon criteria for NSE Emerge & BSE SME\n➔\n3+ years existence\n➔\nMax post-issue paid-up capital: ₹25 Mn\n➔\nPositive EBITDA: 2 out of last 3 FYs\nExchange-specific criteria\n➔\nNSE Emerge: Requires positive net worth & FCF to equity \n➔\nBSE SME: Minimum net worth ₹10 Mn & net tangible \nassets ₹30 Mn\nIndus Valley - IPO Boom",
                "word_count": 216
            },
            {
                "page_number": 120,
                "text": "Indus Valley\nQuick Commerce\nIndus Valley - Funding Trends Pg 95\nIPO Boom Pg 111\n➔\nQuick Commerce: Why it works in India, the \nimplications of its rise, and is there irrational \nexuberance re Quick Commerce? \n➔\nAI: Is India getting a foundational model soon?\nSector Deep Dives \nIndus Valley Playbooks Pg 157\nA detailed analysis of the Quick \nCommerce market, its growth, why it \nworks in India, what the vectors of its \ngrowth are, the implications of its rise, \nand whether there is ‘irrational \nexuberance’ about its prospects?\n120",
                "word_count": 90
            },
            {
                "page_number": 121,
                "text": "121\nThe ‘Quick India Movement’\nSource: Twitter / Harsh Punjabi, and Vaibhav Domkundwar\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 22
            },
            {
                "page_number": 122,
                "text": "With 24x growth in order value since FY22 and user base doubling YoY, Quick Commerce is redefining India's retail landscape\n122\nQuick Commerce is India’s fastest growing industry segment ever!\n* MTU numbers stated here are not unique; a user using multiple platforms will be double counted.\nSource: CLSA, JP Morgan, Business Standard | \nOthers (3%)\nBlinkit\n44%\nInstamart\n23%\nZepto\n30%\nFY25 food delivery MTUs for Swiggy and Zomato \n(both of whom who have been operating over a \ndecade) together are expected to be 40.8Mn. Quick \nCommerce MTUs are two-thirds of this in three years.\n24x rise in Gross Order Value in 3 years!\nRapid rise in MTUs or monthly \ntransacting users)*\nBlinkit, Zepto, Instamart dominate this \nspace, but competition is brewing.\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 132
            },
            {
                "page_number": 123,
                "text": "Quick commerce players are aggressively expanding dark store network and geographical presence, with Blinkit leading in \nboth metrics\n123\n“Zomato is India’s Capex Story”* \n* Tongue in cheek remark by Aditya Soman, CLSA, given Blinkit (Zomato’s subsidiary)’s aggressive dark store roll out\nSource: CLSA, JP Morgan, Money Control\nExpansion beyond metros: Recent launches in Tier 2 cities including \nBathinda, Haridwar, Jammu, Kochi, Rajkot, and Bhopal\nDark store growth has been explosive, with nearly 2,000 stores \nadded this financial year…\n…and expanding into more and more cities.\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 95
            },
            {
                "page_number": 124,
                "text": "124\nThanks to scale efficiencies, unit economics has rapidly \nimproved!\nSource: Zepto investor presentation, BofA\nA 2022 store took 23 months to turn EBITDA-positive with 4cr \nspent on capex, while a 2024 store turned EBITDA-positive \nin 8 months with 1.5cr in capex\nZepto is hitting store breakeven faster per the founder\nBlinkit: Contribution Margins turn positive despite rapid \nexpansion and competitive pressures\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 71
            },
            {
                "page_number": 125,
                "text": "Other Variable \nCosts\n₹61\nDelivery Costs\n₹35\nDiscounts ₹5\nKey Blinkit metrics\n125\nContribution margin is built on two key pillars: AOV and take rate\nSource: BofA\nMetrics\nFY25E\nGOV \n₹27,867 Cr\n% yoy\n123.50%\nAverage MTUs\n9.6 Mn\nAOV\n₹674\nOrders\n413 Mn\nImplied Take Rates\n19.50%\nAdjusted Revenue\n₹5,420 Cr\nContribution Margin \n(as % of GOV)\n4.00%\nAdjusted EBITDA\n(₹33 Cr)\n% margin on GOV\n(0.10%)\nIn contrast, Swiggy was AOV of 515 and \n15.5% take rate (Rs.80) which makes it \ndifficult for them to cover delivery & other \nvariable costs and hence lose money. \nUltimately variable costs are also a \nfunction of scale (with increased orders, \nper unit costs drop!) \nBreakup of Blinkit \nAOV ₹674\nCommission & \nAd Revenue\n₹120\nUser Fee ₹11\nSources for \n₹131 revenue\nCost Breakup of \n₹131\nUnit economics of a single Blinkit order\nBlinkit Revenue \n19.5% (₹131)\nContribution \nProfit ₹31\n+\n=\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 159
            },
            {
                "page_number": 126,
                "text": "126\nSource: Twitter / Manish Singh, Motilal Oswal\nIndia has only 6% modern retail share vs China at \n32%, and US/UK ~80% per this tweet\nWhy?\nWith lack of cars and small houses (lesser storage) - people prefer to shop \nlocally as they cannot go long distance and also not stock up on items\nIndia has low car ownership\nHouses are smaller than in other nations\nIndia seems to be leapfrogging Modern Retail and going directly to quick commerce\nQuick Commerce works because India is a poor market for \nModern Retail\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 100
            },
            {
                "page_number": 127,
                "text": "Combination of low labour cost along with high density cities make quick commerce unit economics work for India\n127\nWhy Quick Commerce works in India\nTop Indian Cities counted include Delhi, Mumbai, Kolkata, Bengaluru, Hyderabad. \nGlobal cities counted include Tokyo ,São Paulo, New York City, Los Angeles, Paris\nSource: CLSA, Goldman Sachs | *\n“One reason the quick commerce model has had a greater impact in India is the lower labour cost as a proportion to cart size. Our sample suggests that the minimum \nwage-to-cart size ratio is 10-12% in India compared with 35-40% in China and 40-50% on average in Western countries.” - CLSA\nLow labour cost\n1\nHigh population density*\n India has amongst the lowest rider cost \nto Gross Order Value \n2\n3\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 134
            },
            {
                "page_number": 128,
                "text": "128\nQuick Commerce - Faster, cheaper, and a wider selection\nSource: Twitter / @Sajcasm_, CLSA, Datum \nInstant gratification\n1\nRapidly expanding SKU count\nCheaper, thanks to discounts\n2\n3\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 38
            },
            {
                "page_number": 129,
                "text": "129\nQuick Commerce is moving beyond grocery to become the new \n‘everything store’\nSource: CLSA, The Arc, Twitter / Madhav Chanchani\nMost stores have ~10k SKUs with a select few \nstores with 25k+ SKUs\nBlinkit, in particular, has been \naggressively expanding SKU count \n1\nSwiggy is behind the curve, but is also \nseeing non-food categories grow\nNon-food categories account for \n40% of Blinkit’s GOV\n2\n3\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 75
            },
            {
                "page_number": 130,
                "text": "Returns and refunds, and the post-purchase experience matters too!\n130\nSource: LinkedIn / Aadit Palicha\nAs SKU counts expand and QCommerce (QCom) goes beyond \ngrocery, QCom operators rethink Qcom beyond just delivery\n“It is now time to take the customer \nexperience and growth to the next \nlevel by launching 10-minute returns \nand exchanges.”\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 62
            },
            {
                "page_number": 131,
                "text": "131\nTo drive margin expansion, Zepto and Instamart have introduced \nprivate labels\nSource: CLSA, Twitter / Rahul Mathur\nZepto’s private label meat brand Relish has seen great traction thanks to its \ndistribution muscle \nSwiggy too has started selling its private \nlabel brands on Instamart\nSupreme Harvest\nTruly Good Food\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 58
            },
            {
                "page_number": 132,
                "text": "These 10-min food delivery services mostly leverage their existing store infra\n132\n…and higher margin prepared food products!\nSource: LinkedIn / Aadit Palicha, Zepto investor presentation\nThe top 3 quick commerce players have all forayed into in-house \nfood delivery services \nZepto cafe has gone from 30K to 75K orders/day in just two \nmonths\nOperating via cloud kitchens situated within dark stores allows them to \nincrease their Average Order Value and margins while utilizing their \nexisting infrastructure and avoiding commission payments to \nintermediaries.\nIn Nov’24 Zepto Cafe was present in 15% of its dark stores, whereas \nnow it is available in more than 50% of dark stores.\nAadit Palicha, \nCEO at Zepto, \nsays that Cafe’s \nrun rate is at 10% \nof Domino’s last \nquarter revenue.\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 133
            },
            {
                "page_number": 133,
                "text": "133\nRevenue from ads become a key growth lever for QCom players\nSource: LinkedIn / Aadit Palicha, Goldman Sachs\nFrom BofA : “We estimate ad revenues of QC platforms to be around \n3-3.5% (of GMV). We see this improving to 5-5.5% in coming years for \nselect platforms as they leverage data analytics to extract more from brands \nby adding value. This is a ~90% EBITDA margin business.\"\nQuick commerce ad revenues are growing fast…\n…and are contributing meaningfully to the bottom-line\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 90
            },
            {
                "page_number": 134,
                "text": "134\n‘Quick’ expands to services and verticals too!\nQuick Commerce for Home Services\nQuick Commerce for Fashion\nQuick Commerce for Food Delivery\nSlikk\n60-Min Fashion delivery\nSnabbit\nHouse help in minutes\nSwish \n10-Min Food delivery\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 44
            },
            {
                "page_number": 135,
                "text": "As Quick Commerce’s success inspires larger horizontal and vertical ecommerce players to start their experiments, we are likely to see \na speeding up of delivery times in India across most types of deliveries. We will be a Quickish Commerce country.\n135\nFrom Quick Commerce to Quickish Commerce\nSource: Twitter / Rajesh Sawhney, Twitter / Manish Singh, Economic Times\nFlipkart has entered Quick Commerce\nAmazon has plans to follow\n2\nOther players are taking notice too\n3\n1\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 86
            },
            {
                "page_number": 136,
                "text": "In just three years, Quick commerce has started contributing 30-60% of ecommerce sales for major FMCG players, driving \nnew packaging, distribution strategies.\n136\nFMCG Brands love Quick Commerce\nSource: Datum, Bernstein, Business Standard\nQCom is becoming the fastest growing channel for FMCG \nbrands…\n…influencing them to rethink packaging and pricing for the \nSKUs sold in Quick Commerce channels \n10% of all ice creams sold \nby HUL are sold on quick \ncommerce channels.\nDabur stated that quick \ncommerce makes up \n>30% of its overall \nbeverage sales.\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 94
            },
            {
                "page_number": 137,
                "text": "137\nIn the long run, Quick Commerce may be more frenemy than \nfriend to FMCG players\nSource: Twitter / Arindam Paul\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 30
            },
            {
                "page_number": 138,
                "text": "Quick commerce eliminates traditional distribution moats, creating a level playing field between D2C and FMCG brands\n138\nQuick Commerce levels the playing field for D2C\nSource: Twitter / Ganesh Sonawane, India Today, Salty\nShare of QCom revenue as a % \nof Marketplace revenue rose \nfrom from ~30 to ~90% \nQCom is the fastest growing channel \nfor D2C brands today…\n1\n…and quickly catching up to online \nmarketplaces.\n…getting these brands access to \ncustomers they never had before…\n2\n3\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 88
            },
            {
                "page_number": 139,
                "text": "139\nThe urban consumer is shifting their buying behaviour away from \nKirana stores\nSource: Datum Intell, Mint, Captable\n3/4ths of survey respondents felt that Quick \nCommerce poses a long-term threat to the \nviability of Kirana stores\nFor one Bengaluru-based engineer, his response to \na recent craving for a soft drink made him realise \njust how much quick commerce had reshaped his \nbehaviour. “I randomly order some juice because I \nhave access,” he says. “Earlier, I used to open the \nfridge. Now, I open Instamart, which is like an \nevolved version of checking the fridge.”\nVisible impact on Kirana stores\n1\nKirana owners are clearly worried\nUrban shoppers prefer Quick \nCommerce\n2\n3\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 121
            },
            {
                "page_number": 140,
                "text": "140\nCase Study: Kirana Store owner in Bangalore facing both demand \nand supply side impact\nSource: Blume Research\nDrop in revenue, even with rising prices\nSupply is equally impacted\nDelivery orders have practically vanished\n1\n2\n3\nTrade promotions by FMCG players are \nabsent. \nPreviously, retailers could earn major \nincentives like washing machines for \nmeeting targets - these volume-based \nrewards are now rare.\nMargins on branded products have \ndropped significantly. \nFor instance, biscuit category margins \nhave fallen from 22% to 7-8%, severely \nimpacting retailer profits.\nWeakened demand has forced retailers \nto abandon bulk purchasing in favor of \nsmaller, frequent orders. \nThis shift further reduces margins as they \nlose bulk buying benefits.\nKirana stores don’t have enough options (SKUs) for brand \nconscious customers. And with free delivery as well as the \ndiscounts that QCom offers, online works out cheaper.\nInsights are from an interview with a \nshop owner who has been in \nbusiness for 30 years, currently \noperating in a middle-class \nneighborhood of urban Bangalore.\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 173
            },
            {
                "page_number": 141,
                "text": "141\nQuick Commerce operators have power, and they are not afraid to \nwield it too\nSource: The Ken, Twitter / Prem Pradeep\nBrands find it hard to list on Quick Commerce platforms\nDark patterns have started to emerge on the apps\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 50
            },
            {
                "page_number": 142,
                "text": "A slew of analyst reports have projected heady numbers for Quick Commerce; for instance an equity research report from a \nleading brokerage house projects the Industry to hit $89b in FY31 (FY25E of $7.1bn). How realistic is this? \n142\nIrrational exuberance about Quick Commerce?\nOrders per month per \nuser\nGross annual order \nvalue\nMonthly transacting \nusers (MTUs)\nNumber of dark stores\nTotal annual orders\nLet us examine two of these above estimates: Monthly transacting users (MTUs), as well as Dark Stores, closely.\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 91
            },
            {
                "page_number": 143,
                "text": "Growth projections to 128 million monthly transacting users (MTUs) look ambitious when India1 itself is not widening fast\n143\nHow realistic is the Monthly Transacting User number?\nSource: Leading brokerage house, Twitter / Kunal Shah\nMuch of India’s consumption is led by India1, and within that there is a \nsubset we call India1 Alpha, which is about 8-10 million households \nlarge who are true super consumers. This class is growing slowly, and \nas we saw in the Consumption section, has deepened than widened. \nThe growth in MTUs will thus attract marginal users not power users, \nand thus orders nearly doubling will be challenging.\nHow Quick Commerce is projected to grow\nThis misses out on the true upper bound of the Indian \nconsuming class\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 132
            },
            {
                "page_number": 144,
                "text": "July 2021 estimates by Jefferies projected 32.6M users for Zomato by FY25, but current trajectory points to 20.6M users in \nFY25 - a reminder about user growth forecasts in consumer internet consistently fall short\n144\nWe have been here before\nSource: Jefferies, Motilal Oswal\nJefferies estimate of Zomato’s Monthly Transacting Users \n(MTUs) in Jul’21\nIn reality, Zomato has not come anywhere near those \nprojections. It is at 2/3rd of those numbers.\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 80
            },
            {
                "page_number": 145,
                "text": "145\nHow realistic is the Dark Stores number?\nSource: Leading brokerage house, Bernstein, HDFC Securities\nThe dark store number is projected to \ngrow from 3400 to 11500 over 6 years\n19300\nTotal \nPincodes\n965\nBut does India have so much depth?\nA proxy for affluence is presence of 5+ organised \nretail stores, which per a Bernstein study is seen in \nonly 5% of India’s pincodes. These pincodes \nserves 11% of population.\nThe challenge is that there are not many of these in \na country with per capita income below $3k.\nPresuming each of Blinkit, Instamart, Zepto has 2 \nDark Stores per pincode, and rounding off to 10 \nDark Stores per pincode, we are still looking at \n9,650 Dark Stores (not 11,500). \nPer a HDFC Securities study, \nthere are only 63 districts in \nIndia (<10% of 780 or so \ndistricts) with per capita income \nof ₹150k+ and density > 500 \npeople per sq km. \nThese have ~90m households \nin all (across all income levels) \nand per HDFC Securities, \nthese can support at max \n~7,800 dark stores, not 11,500!\nWhen existing dark stores have begun stagnating\nAdded to that is that Orders per Dark Store have \nstabilised. Given this, and the diminishing returns \nof expanding Dark Stores beyond certain areas, \nthe aggressive projections of total orders seem \na tad unrealistic. (80% of Blinkit’s sales come \nfrom the top 8 cities per Albinder (3QFY25 \nanalyst call transcript).\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 243
            },
            {
                "page_number": 146,
                "text": "146\nTL;DR\nSource: Blume Analysis\n●\nQuick Commerce is not immune to the gravitational pull of low TAM (given India’s low \nper capita income) and the power law of a tiny percentage of superconsumers\n●\nLike rideshare, food delivery, and even ecommerce, we will see MTU growth tapering \n- it is unlikely that Quick Commerce is immune to this.\n●\nECommerce players have already started reacting, and while it is not guaranteed they \nwill be able to counter Quick Commerce players, the increased competition will have \nsome impact on the Quick Commerce industry profit pool.\n●\nIt is the case that we are moving to almost every ecommerce platform speeding up \ntheir delivery. India will become a Quickish Commerce country, especially because of \nthe superconsumers are in high density areas amenable to rapid delivery.\n●\nAs Quick Commerce expands, and the toll on Kiranas becomes more visible, we may \nsee more visible debates and measures to check Quick Commerce’s growth.\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 169
            },
            {
                "page_number": 147,
                "text": "Source: Twitter / Soumya Gupta\n147\nIndus Valley - Sector Deep Dives / Quick Commerce",
                "word_count": 15
            },
            {
                "page_number": 148,
                "text": "➔\nQuick Commerce: Why it works in India, the \nimplications of its rise, and is there irrational \nexuberance re QCom? \n➔\nAI: Is India getting a foundational model \nsoon?\n Indus Valley\nWhy China, not India had a DeepSeek \nmoment, and whether the recent \nenthusiasm and initiatives could spur the \ncreation of a foundational model? \nAI: Is India getting a \nfoundational model \nsoon?\nIndus Valley - Funding Trends Pg 95\nIPO Boom Pg 111\nSector Deep Dives \nIndus Valley Playbooks Pg 157\n148",
                "word_count": 82
            },
            {
                "page_number": 149,
                "text": "149\nAn Indian company was present at the birth of OpenAI\nSource: Introducing OpenAI 2015\nInfosys was one of the founding donors of \nOpenAI, then structured as a non-profit.\nSubsequently due to Vishal Sikka’s exit, there was \nno link with OpenAI, and it missed the opportunity to \nbe an investor when OpenAI restructured itself and \nspun off a for-profit entity in 2019.\nThis was the entity that Microsoft, Khosla Ventures \ninvested.\n…\nIndus Valley - Sector Deep Dives / AI",
                "word_count": 80
            },
            {
                "page_number": 150,
                "text": "150\nBroad vibe till late 2024\nSource: Twitter / Chandra R Srikanth\nPre-DeepSeek default mode\nIndian-founded startups building in AI\nServices\nApplications\nMiddleware\nFoundation Models\nCloud Platforms\nComputer Hardware\nIndus Valley - Sector Deep Dives / AI",
                "word_count": 37
            },
            {
                "page_number": 151,
                "text": "151\nVibeshift!\nSource: Twitter via tweets from Financial Times, Aravind Srinivas, Paras Chopra and Sridhar Vembu\nIndus Valley - Sector Deep Dives / AI",
                "word_count": 24
            },
            {
                "page_number": 152,
                "text": "152\nWhy didn’t India do DeepSeek?\nSource: Twitter / Sadanand Dhume, Twitter / Anmol Maini\nThe forcing functions that created DeepSeek\n1\n2\n3\n…\nChina being the base for 1/8th of World’s top \nAI researchers (India has none)\nChina has been continuously investing in \nand improving in AI. The Australian Strategic \nPolicy Institute identified that China led in \njust three of 64 critical technologies in the \nyears from 2003 to 2007, but is the leading \ncountry in 57 of 64 technologies over the \npast five years from 2019 to 2023. \nConstraints breed creativity - the challenges \nin accessing GPUs led them to approaches \nand tech minimising GPU use\nCrackdown on the finance industry leading \nto the hedge fund High-Flyer deciding to \nredirect its attention towards AI tech, away \nfrom Finance. They also managed to access \ncapital (Govt support?) to undertake the \n$1.6b+ investment to develop the same \n($1.6b via Semi Analysis)\n4\nIndus Valley - Sector Deep Dives / AI",
                "word_count": 161
            },
            {
                "page_number": 153,
                "text": "153\nCan India build its own foundational model? We will find out soon!\nSource: Twitter / Vinod Khosla, Twitter / India IT Minister Ashwini Vaishnav, IndiaAI Website\nBlume Perspective: We do think we will have home grown foundational models emerging in the coming 12-18 months given the Government support, as well \nas the emergence of teams keen to build India’s first foundational model. There is too much momentum behind this, and enough confidence that it can be built \n(post DeepSeek) for it to not happen.\nDPI and ISRO, both examples of frugal innovation, and also examples of public-private partnerships, show a potential path forward for AI foundational models. \n‘AI Sovereignty’\n₹20bn ($240m) allocation in the Indian budget; access to 18k GPUs at 40% below \nmarket rates to spur India’s homegrown LLMs.\nIndus Valley - Sector Deep Dives / AI",
                "word_count": 139
            },
            {
                "page_number": 154,
                "text": "154\nThe success of Digital Public Infra and ISRO / Space Missions are two \ngreat examples of frugal innovation. Could AI models be the third? \nSource: UIDAI Accounts, UIDAI Annual Report ‘23, Hindu Business Line , Blume Indus Valley Report 2024\nThe UPI Story\nThe ISRO Story\nISRO is consistently cited as having pioneered the frugal approach to \nspace exploration, cheaper than Hollywood space movies even!\nWith just over $1b spend, India had onboarded a billion people to the \nAadhar identity initiative; resulting in annual savings of over a billion!\nYear\nAmount\n2009-10\n₹26.2 Cr\n2010-11\n₹268.4 Cr\n2011-12\n₹1,187.5 Cr\n2012-13\n₹1,338.7 Cr\n2013-14\n₹1,544.4 Cr\n2014-15\n₹1,615.3 Cr\n2015-16\n₹1680.4 Cr\n2016-17\n₹1132.8 Cr\nExpenditure on Aadhaar (in INR crore)\nIndus Valley - Sector Deep Dives / AI",
                "word_count": 130
            },
            {
                "page_number": 155,
                "text": "155\nIndia has the talent (even if our best talent is in the US) and now \nwe are getting the GPUs!\nSource: Twitter / GitHub CEO Thomas Dohmke, Savills India Research, Visual Capitalist, Cushman & Wakeﬁeld, Moneycontrol \nWe have the talent\nWe are getting the data centres\nWe can build cheaper than our peers\nIndus Valley - Sector Deep Dives / AI",
                "word_count": 62
            },
            {
                "page_number": 156,
                "text": "156\nMeanwhile there are impressive Consumer AI stories emerging \nfrom India as well!\nSource: Twitter / Sanket Shah, Twitter / Sumanth Raghavendra, Presentations AI blog\nVideo generation via prompts leveraging OpenAI\n“4 million MAUs creating 7 million videos a month” - OpenAI\nCreate presentations leveraging AI.\nHit 1 million users in <3 months and then hit $1 million \nrevenue in 12 months (by Jun’24), and founder writes has \ngrown ‘leaps and bounds’ since then to hit “5 million users, \n112 countries, millions in profits”\nIndus Valley - Sector Deep Dives / AI",
                "word_count": 92
            },
            {
                "page_number": 157,
                "text": "➔\nThe various India2 Playbooks.\n➔\nHow Indus Valley influenced Indian advertising.\n➔\nReturns, and how Indian startups are addressing \nit.\n➔\nMarketing framework for the Indian diaspora or \nIndia0.\n Indus Valley\nThe various India2 \nPlaybooks.\nHistoric playbooks contrasted with the \nEvolved and Emerging playbooks, \nfollowed by case studies of STAGE, \nKaleidofin, and Voice Club. Why voice, \nand microtransactions are two killer \nfeatures of the Emerging playbook.\nIndus Valley - Funding Trends Pg 95\nIPO Boom Pg 111\nSector Deep Dives Pg 120\nIndus Valley Playbooks \n157",
                "word_count": 87
            },
            {
                "page_number": 158,
                "text": "158\nIndus Valley - Playbooks / India2\nThe India2 playbook is evolving\nEmerging Playbook\nRethink the product around the fundamental \nneed to be solved (or job-to-be-done / JTBD)\nEvolved Playbook\nRe-engineer the product for Indian context \nand user behaviour, and margins(!) benefitting \nfrom Jio & UPI boost.\n2015 - 2020\n2020 Onwards\nHistoric OG Playbook\nLaunch a proven western product to suit Indian tastes and language preferences.\nConversations with \nthe opposite sex, \nnot dates.\nAstrological \ncounselling as \ntherapy sessions.\nDriver subs, and not \nuser charges as the \nrevenue model",
                "word_count": 89
            },
            {
                "page_number": 159,
                "text": "159\nEvolved Playbook: Re-engineer the product, and price it \naffordably, for India2\n₹20\n₹105\n₹75\n₹10\n₹1,788 \nannual\n₹399\nannual\n➔\nHere the product is re-engineered to suit India2’s language, taste, and price preferences. \n“Our users are happier to pay ₹10 every day for a month than pay ₹300 upfront” \n - Harsh Jain of Dream11 (during a conversation with Blume portfolio founders)\n➔\nThese products have superior unit economics thanks to being rethought from the grounds up for India2; as opposed to being \nworked downward from an India1 product.\nIndus Valley - Playbooks / India2",
                "word_count": 95
            },
            {
                "page_number": 160,
                "text": "160\nHow STAGE engineers ultra low-cost content\n➔\nStandardized set of story tropes and templates re-scripted for different languages, designed for low-cost shooting \n(e.g., mostly small sets scripted into storyline).\n➔\nWork with local content creators who don’t have access to other mainstream outlets willing to work for low costs.\n➔\nSignificant amount of pre-planning prior to shoot enabling quick turnarounds. \n=\n+\n+\nLower\nBudgets\nPer Film\nFaster \nShoots\nPer Film\nHighly\nRated\nSource: STAGE\nIndus Valley - Playbooks / India2",
                "word_count": 82
            },
            {
                "page_number": 161,
                "text": "161\nSource: Kaleidoﬁn\n ki score is an inclusive supervised AI/ML score developed by Kaleidofin, and used for Credit Decisioning and Risk \nManagement through all stages of the loan lifecycle. It is designed to reduce risk while significantly increasing access to traditionally underserved \ncustomers. It is built on datasets with dimensions including credit history, demographics, customer behaviour and alternate data. It is a powerful tool \nfor increasing access to appropriate credit beyond a credit bureau score.”\nCategory\nPAR 90 %\nki score accept + cb accept\n1.53%\nki score accept + cb reject\n2.51%\nki score reject + cb accept\n4.44%\nki score reject + cb reject \n7.68%\nPAR 90% measures borrowers defaulting on \nprincipal for over 90 days. Customers \napproved by ki score but rejected by credit \nbureaus have lower default rates compared to \nthose rejected by ki score but approved by \ncredit bureaus (cb hereafter).\nki score enabled 42.3% \nadditional loans beyond \ntraditional credit bureau \nratings\nki score has increased loans disbursed \nby 73%\nMonthly household income growth for \nnano-entrepreneurs shows \nki score’s impact\nPAR 90% data validates ki score's \naccuracy and inclusiveness \nFindings from a pool of ki scored nano-entrepreneurs \nshows the impact that access to timely credit may have \non customer resilience and well-being and the ki score \nacts as a key enabler here. “We see an average \nincrease of 26% in monthly HH income, 47% in \nannual business turnover, and 52% in monthly \nbusiness profits.”\nIndus Valley - Playbooks / India2\nHow Kaleidofin reengineered the credit rating product for India2 / India3",
                "word_count": 256
            },
            {
                "page_number": 162,
                "text": "162\nEmerging Playbook: Rethink the product for the specific job to be \ndone (JTBD) to fit India2’s context\nJTBD\nHelp me start dating\nJTBD \nI need easy, reliable \naccess to high quality \nmental healthcare.\nJTBD\nI don’t think there is anything wrong with \nme that I need ‘therapy’ (it is not socially \nacceptable in my context). Astrology counselling \nis a safe socially acceptable space for me to \nunburden myself and get some emotional relief.\nHere, founders understand the core Job-To-Be-Done (JTBD) in the context of the India2 user, including how prevalent cultural \npractices will support adoption, and use this to rethink the product itself. \nIndia 1\nIndia 2\nJTBD\nBefore I can think of dating, I need to \nspeak to members of the opposite sex. \nSo the product is to enable better \nconversations, via gamified formats.\nIndus Valley - Playbooks / India2",
                "word_count": 142
            },
            {
                "page_number": 163,
                "text": "163\nTwo other core features of the Emerging India2 Playbook:\nVoice and microtransactions\nMicrotransactions-led revenue model (prefilled wallet used for \ngifting) leading to whale + tail model\nFRND, AstroTalk, InstaAstro, Clarity all have 1:1 voice as a key revenue model. India2 (and many India1) users are willing to pay to talk to a stranger \n(expert or member of the opposite sex). The success of this model is attracting apps with a tangential interest in the space (e.g., Lokal) to explore \nthis revenue opportunity.\nHeavy on voice, with 1:1 conversations as a key revenue \ndriver\nwhich enables 1:1 counselling conversations, is an example of a company that exemplifies these features. \nSource: Voice Club\nIndus Valley - Playbooks / India2",
                "word_count": 118
            },
            {
                "page_number": 164,
                "text": "164\nSometimes it flips, and you have a India1 offering for what was a \nIndia2 product!\nSource: The Print\nIndus Valley - Playbooks / India2",
                "word_count": 25
            },
            {
                "page_number": 165,
                "text": "➔\nThe various India2 Playbooks.\n➔\nHow Indus Valley influenced Indian \nadvertising.\n➔\nReturns, and how Indian startups are addressing \nit.\n➔\nMarketing framework for the Indian diaspora or \nIndia0.\n Indus Valley\nHow Indus Valley \ninfluenced Indian \nadvertising.\nHow Indus Valley rethought the celebrity \nad to generate shock value, and how it \nhas shaped the Indian advertising \nmarket. We also look at the currency of \ntrust-building is diverging between India1 \nand India2 resulting in distinct \ncommunication templates.\nIndus Valley - Funding Trends Pg 95\nIPO Boom Pg 111\nSector Deep Dives Pg 120\nIndus Valley Playbooks \n165",
                "word_count": 97
            },
            {
                "page_number": 166,
                "text": "Humanising celebrities, making fun of them, was a new addition to the Indian ad oeuvre. Legacy brands historically kept the \ncelebrity on a near pedestal (with some exceptions).\n166\nIndus Valley - Playbooks / Indus Valley Marketing\nHow Indus Valley pioneered a new ad trope\n➔\nWhat is common to these ads is that their makers are ex-members of AIB (All India Bakchod) a comedy collective that melted down in the \n2018 #metoo wave. Key members include Tanmay Bhatt, Devaiah Bopanna, Vishal Dayama etc. [Tanmay + Devaiah also work together as \nMoonshot.]\n➔\nThey pitched legacy brands who hesitated to sign them given their lack of big agency experience; Startups however found a perfect match in \nthem especially given the comedians’ ability to create attention and shock value by depicting celebrities in a never before light, cutting \nthrough clutter.\nThis and the following slides in this section benefited significantly from inputs gathered during a conversation with Karthik Srinivasan, a leading ad / marketing guru (x.com/beastoftraal).\nI also enjoyed speaking with Arun Iyer (x.com/aruniyer), a seasoned adman who co-founded and is Partner at Spring Marketing Capital.",
                "word_count": 185
            },
            {
                "page_number": 167,
                "text": "167\nAs the ‘ComAdians’ went up market, Big Ad stepped down to \npartner with startups\nMoonshot now works with the likes of \nVadilal, Rungta Steel etc. \nDaftar, a smaller creative shop \ndoes work for Pepsi… \nMeanwhile a couple of glimpses of how \nmainstream ad agencies are working with \nscaling startups.\nIndus Valley - Playbooks / Indus Valley Marketing",
                "word_count": 58
            },
            {
                "page_number": 168,
                "text": "168\nMeanwhile, Indus Valley likes full stack brand-building\nFounders are building personal brands to canvass for \ntheir startups, or sometimes just to build \npersonal brands.\nZomato inspired the trend of startups setting up \nagencies. That trend has continued to gather strength.\nIndus Valley - Playbooks / Indus Valley Marketing",
                "word_count": 49
            },
            {
                "page_number": 169,
                "text": "169\nHighlighting ingredients, clever copy, and use of \ncontent are ways to build trust for India1 products. \nIn the case of India2, trust is mediated through the credibility associated with a \ncelebrity. While celebs are also used for India1 advertising, they are used more to cut \nthrough clutter (e.g., Bold Care, Cred) and less to reinforce or borrow credibility from. \nIndus Valley - Playbooks / Indus Valley Marketing\nHow trust is mediated through communication is diverging between India1 and India2. \nThe currency of trust-building is also diverging between India1 \nand India2",
                "word_count": 91
            },
            {
                "page_number": 170,
                "text": "Indus Valley\n➔\n➔\nThe various India2 Playbooks.\n➔\nHow Indus Valley influenced Indian advertising.\n➔\nReturns, and how Indian startups are \naddressing it.\n➔\nMarketing framework for the Indian diaspora or \nIndia0.\nReturns, and how \nIndian startups are \naddressing it.\nIndian startups in the consumer space, \nespecially apparel and footwear brands, \nhave a returns issue. We analyse trends \nand suggest playbooks that Brands are \nadopting / can adopt to overcome these \nchallenges. \nIndus Valley - Funding Trends Pg 95\nIPO Boom Pg 111\nSector Deep Dives Pg 120\nIndus Valley Playbooks \n170",
                "word_count": 93
            },
            {
                "page_number": 171,
                "text": "171\nHigh Return rates are a key concern area for Indian online sellers\nSource: Redseer x Ecom Express Report, Unicommerce India Ecommerce Index 2023 Report, Return Prime Report\nReturns can be even higher on \nmarketplaces\nReturns % on marketplaces is 26.3% \nvs for 6.2% on brand’s own website, \nper Unicommerce. \nReturns are higher for Cash-on-Delivery \norders \nvs prepaid orders. COD or Cash on Delivery \norder returns are 20.9% (vs 5.8% for prepaid \norders), per Unicommerce.\nReturns are highest for fashion & \nfootwear \nApparel return rates as high as 30-35% per \nReturn Prime.\nFor COD orders of fashion brands on \nmarketplaces, returns are thus in the \n45-55% range!\nAround a sixth of ecommerce shipment volumes get returned\n16%\nIndus Valley - Playbooks / Returns",
                "word_count": 123
            },
            {
                "page_number": 172,
                "text": "172\nUnderstanding Returns\nNote: * The fashion brand wants to remain unnamed\nReturn to Origin (RTO)\nCustomer not at home or \norder not delivered\nA high return rate increases logistics cost, leads to more spoilage due to the \nback-and-forth thereby increasing cost of goods sold. In the process of \ncollection, repair, and clean up it also reduces the inventory available for \nsale. Returns thereby have a corrosive impact on unit economics.\nTwo types of \nReturns\nReturn to Vendor (RTV)\nCustomer collects and \nreturns due to wrong \nitem, damages, or fit \nissues\nHow returns stack up for a fashion brand*\nOwn \nWebsite\nMarketplaces\nRTO\n10%\n9%\nRTV\n14%\n39%\nTotal Returns\n24%\n48%\nMarketplaces encourage returns (to reduce purchase \nfriction), and customer is frequently encouraged to \nbracket, i.e., buying multiple sizes and then returning \nseveral back.\nIndus Valley - Playbooks / Returns",
                "word_count": 141
            },
            {
                "page_number": 173,
                "text": "173\nReducing RTO or Return to Origin\nSource: Redseer x Unicommerce Report, Delhivery\nAjith Pai, COO, Delhivery: “There are two factors that determine the extent of RTO \n1/ Speed of fulfillment : faster the delivery, the lower the likelihood of doorstep rejections \n2/ COD vs Prepaid: the higher the Prepaid share of orders, the lower the RTO.”\nThis has been trickier. Regular customers do graduate from COD to Prepaid, but as ecommerce \nexpands to Tier 3 towns / India2, there is a rise in customers who prefer COD. So overall COD has only \nslightly moved down to 65%.\nSuccessfully increased speed of delivery \nSpeed of Fulfillment\nCOD vs Prepaid\n35% of this COD is UPI at \ndoorstep. This is higher than \nDelhivery’s peers (at 5-10%), \nand is largely a function of \ntheir focus in bringing down \ncash handling.\n2024’s avg shipment value of \nCOD is ₹660 and prepaid is \n₹1,850. Clearly richer \ncustomers pay in advance. \nPrepaid shipment value has \nincreased over the years, but \nCOD shipment value is stable.\nRTOs drop sharply with \nprepaid orders! COD order \nRTOs are 6x more likely than \nPrepaid order RTOs!\nIndus Valley - Playbooks / Returns",
                "word_count": 193
            },
            {
                "page_number": 174,
                "text": "174\nConsumer Brands (and marketplaces) are nudging buyers to prepay\nSource: Reddit, Dharmesh Ba / The India Notes\nIntroducing friction, creating commitments for COD are ways to nudge customers slowly into prepaid orders \nLevying a ‘handling fee’\n1\nNudging customers to pay in advance \nby charging more for COD\nMaking customers pay a \nsmall advance\n2\n3\nIndus Valley - Playbooks / Returns",
                "word_count": 63
            },
            {
                "page_number": 175,
                "text": "175\nD2C / Consumer Brands beginning to see the impact of these nudges\nSource: GoKwik\n an eCommerce enabler brand providing smart checkout and COD-enabler solutions shared data on how COD \nis trending downwards for the brands they support. \nAs we see here, the higher the city \ntier, the lower the COD share of \norders! \nAn interesting data point shared by \nGoKwik team was on the rise of \nCredit as a payment option at \ncheckout. From <1% in ‘22 it is at \n~5.5% in ‘24.\nTier 1 Cities COD Orders %\nTier 2 Cities COD Orders %\nTier 3 Cities COD Orders %\nRemember this was 65% for Delhivery!\nCOD orders trending down\nIndus Valley - Playbooks / Returns",
                "word_count": 118
            },
            {
                "page_number": 176,
                "text": "176\nPlaybooks to reduce RTOs: better address management\nA tale of 2 cities. Why are Indian \naddresses so long?\nAnd so hard to locate?\nAnd they cost us money!\nGC & Accel’s Bay Area office addresses \nvs Bangalore, clipped from their websites.\n“Poor addresses cost \nIndia $10 - 14 billion \nannually, ~0.5% of the \nGDP.”\n-\nDr Santanu Bhattacharya, \nMIT Media Lab\nIndus Valley - Playbooks / Returns",
                "word_count": 68
            },
            {
                "page_number": 177,
                "text": "177\nHow startups are ‘addressing’ RTOs :)\nThese are 2 interesting demand-side solutions that tackle the \nproblem on the customer’s end (as compiled by Dharmesh Ba) \n●\n Add a video guide (Bharat Agri) \n●\nAdd a pic of your front door (Swiggy)\nThere are 2 supply-side innovations to drive down RTOs\n●\nRTO predictor by Delhivery (below, left image) \n●\nGoKwik’s offering to reduce RTO (below right) \nCustomer-end solution\nSupply-side solution\nSource: Dharmesh Ba / The India Notes, Delhivery, and GoKwik\nIndus Valley - Playbooks / Returns",
                "word_count": 87
            },
            {
                "page_number": 178,
                "text": "178\nHow brands are attacking RTV (Return to Vendor)\nSource: Return Prime website, Slikk website\nEncourage exchanges \ninstead of refunds\nOffer store credit / gift \ncards instead of cash \nback, enhancing friction \nto avoid lazy \n‘bracketing’.\nAbove via\nSlikk, a qCom \napparel player offers \na “Try & Buy” option, \nto reduce the \nchances of a misfit. \n~20% of orders are \nvia “Try & Buy” - says \nSlikk cofounder \nAkshay Gulati.\nAbove via\nPromote exchanges over refunds\nTry & Buy\nIndus Valley - Playbooks / Returns\nUltimately the only way to address this is through better fits (the biggest reason for RTB. However, two interesting playbooks \nare shown below",
                "word_count": 108
            },
            {
                "page_number": 179,
                "text": "➔\n➔\nThe various India2 Playbooks.\n➔\nHow Indus Valley influenced Indian advertising.\n➔\nReturns, and how Indian startups are addressing \nit.\n➔\nMarketing framework for the Indian diaspora \nor India0.\n Indus Valley\nMarketing framework \nfor the Indian diaspora \nor India0.\nNo report is complete without a 2x2. Here \nis our framework for how brands can \nposition themselves for the Indian \ndiaspora (or India0) basis affluence and \naffiliation (or affinity). We give example of \nstrategies / playbooks for three of the \nfour quadrants.\nIndus Valley - Funding Trends Pg 95\nIPO Boom Pg 111\nSector Deep Dives Pg 120\nIndus Valley Playbooks \n179",
                "word_count": 103
            },
            {
                "page_number": 180,
                "text": "180\nIndus Valley - Playbooks / Diaspora Marketing\nIndian Diaspora, and India0\nSource: Indian Express, Ministry of Foreign Affairs, MEA, PHDCCI, IBEF\nThe Indian Diaspora is affluent and influential. Their economic power is reflected in high \nremittance flows into India - the highest in the world ($107 Bn in 2023-24) and interestingly \ngreater than FDI flows into India ($70.9 Bn in 2023-24) . At Blume, we like to use the term India0 \nas a moniker for this economically ascendant community. \nAs of May 2024, the total number \nof overseas Indians worldwide is \napproximately 35.42 million.\nPIOs\nNRIs\nUSA\n5.4 Mn\nMalaysia\n2.9 Mn\nCanada\n2.8 Mn\nMyanmar\n2 Mn\nUK\n1.9 Mn\nSouth Africa\n1.7 Mn\nHow large is the Indian Diaspora?\nThe Indian Diaspora is well spread out across different continents and geographies\n��\nSaudi Arabia\n2.5 Mn\nUAE\n3.6 Mn",
                "word_count": 142
            },
            {
                "page_number": 181,
                "text": "181\nIndia0 punches above its population weight class\nSource: Indus Valley Report 2024, Times of India\nIn the US, the Indian community ranks highest in \nmedian household income.\n Indian Diaspora makes up 1.5% of the US \npopulation, and this group accounts for 5-6% of all \nUS taxes.\nIndia0 are the highest earners in \nmost host countries\nIndian culture is breaking out into the \nglobal mainstream\nGlobal players are waking up to the \nspending power of this diaspora\nIndus Valley - Playbooks / Diaspora Marketing",
                "word_count": 84
            },
            {
                "page_number": 182,
                "text": "182\nBlume’s Diaspora Marketing Framework\nThe following framework maps out different brands and the diaspora personas they are catering to. We have categorised the diaspora personas \nbased on their income levels (high or low earners) and their level of affiliation to their country of origin (high or low affiliation).\nIndus Valley - Playbooks / Diaspora Marketing",
                "word_count": 56
            },
            {
                "page_number": 183,
                "text": "183\nDiaspora marketing: case studies\nSource: Moneycontrol, Fortune India\nIndus Valley - Playbooks / Diaspora Marketing",
                "word_count": 16
            },
            {
                "page_number": 184,
                "text": "How Inde Wild broke into the global mainstream\n184\nBrand started out as an influencer \nbrand on the back of founder Diipa \nBüller-Khosla’s following\n1\nFrom here they made their foray into \nthe mainstream\nFrom here, brand expanded to \nmulticultural audiences across four \nkey geos - US, UK, Canada and India\n2\n3\nThe founder, is a \nglobal-Indian influencer. \nShe leveraged her \ncommunity of 2m+ \nindividuals to curate test \ngroups across 4 \ngeographies and identify \nunaddressed gaps in \nthe skincare market.\nSource: Inde wild\n54% from \nIndia\nRest from \nUS + UK\nIndus Valley - Playbooks / Diaspora Marketing",
                "word_count": 99
            },
            {
                "page_number": 185,
                "text": "185\nDiaspora marketing channels \nIndus Valley - Playbooks / Diaspora Marketing",
                "word_count": 11
            },
            {
                "page_number": 186,
                "text": "186\nAcknowledgements\nAs with all reports, this too rests on the labour of several analysts, researchers and writers whose work we used to \nbuild on. We stand on the shoulders of giants. We have acknowledged the sources and their contributions on each \nof the pages; in particular, a shout out to Jefferies, Bernstein, Goldman, Redseer, UBS, CRIF, Barclays, Nuvama, \nCLSA, Tracxn, for their regular reports enabling greater access to data, and enhancing our understanding of the \nIndian startup ecosystem. We also acknowledge the inputs and insights of Rahul Mathur, Dharmesh Ba, Arindam \nPaul and other astute observers of the Indian startup ecosystem - thank you for your openness in explaining the \nworld from your perspective, and sharing insights that inform this report. This time we also had the participation of \nseveral startups such as Delhivery, GoKwik, MyGate, Stage, Kaleidofin, Salty, Inde Wild, VoiceClub etc., who \nhelped us with their proprietary data sets that we were able to analyse and draw insights from. We thank them \nprofusely for this support!\nFinally, we would also like to thank the wider Blume team, especially Joseph Sebastian, for their inputs.\nAm sure I have possibly left out a lot more names! Apologies in advance for the same!\n-\nSajith, Anurag, Nachammai & Dhruv",
                "word_count": 209
            },
            {
                "page_number": 187,
                "text": "187\nAbout Blume Ventures\nBlume Ventures is an early stage venture firm based across Mumbai, Bangalore, Delhi and San Francisco, that \nprovides ‘conviction capital’ to founders across India consumer internet as well as software & enterprise technology.\nWe add value through a platform approach – over 85 specialists across shared CFO services, legal advisory, talent \nacquisition, capital raising, GTM enablement, operations support – who focus entirely on supporting portfolio \ncompanies and helping founders learn, thereby greatly improving their chances of success. Our value-added \napproach has helped us retain board representation in the vast majority of our top companies; with an overall Asset \nunder Management (AUM) upwards of $650M.\nYou can read more about us at blume.vc",
                "word_count": 116
            },
            {
                "page_number": 188,
                "text": "The End",
                "word_count": 2
            }
        ],
        "paragraphs": [
            "Sajith Pai | sp@blume.vc\nAnurag Pagaria | anurag@blume.vc \nNachammai Savithiri | ns@blume.vc \n&\nDhruv Trehan, Editorial Fellow\nIndus Valley Annual Report 2025",
            "2\nWelcome to the Indus Valley Annual Report 2025\nIndia’s vibrant startup ecosystem, concentrated in the eastern suburbs of Bangalore, the satellite cities of \nGurgaon and Noida in the Delhi National Capital Region (NCR), the districts of Lower Parel & the Andheri East – \nPowai belt in Mumbai, the Southern suburbs of Chennai, and in the various scattered pockets across many other \ncities such as Pune, Hyderabad, Chandigarh etc., has lacked a singular name. \nAt Blume, we like to use Indus Valley as a catch all moniker for the Indian startup ecosystem. It is a twist on the \ntypical Silicon Wadi / Glen / Fen naming convention, as well as a reference to the Indus Valley Civilisation, one of \nthe vibrant centres of the ancient world, and the ancestral civilisation of the Indian people.\nUnlike Silicon Valley which has a geographical connotation, the term Indus Valley has no such overtone. It is \ninstead a reference to the entire Indian startup ecosystem, spread throughout the nation. It is also an attitude, a \nmindset, one of invention, and ‘jugaad’ and chutzpah.\nThe Indus Valley Annual Report published by Blume Ventures, celebrates the rise of Indus Valley, and its \nemergence as one of the centres of innovation and enterprise in the startup world. It gives us a chance to look \nback, and take stock of its evolution, and look ahead to what is coming. We welcome you to the fourth edition of \nthe Indus Valley Annual Report! Our previous editions (2024, 2023, 2022) can be accessed at the website \nindusvalleyreport.com",
            "➔Consumption and services dominate our GDP. (21) \n➔India is formalising, steadily. (29) \n➔India doesn’t save enough. (33) \n➔Why land issues mean India hoards up on gold. (37) \n➔India doesn’t invest in human capital. (41)\n➔India’s manufacturing playbook is good, but not great. (48) \n➔How DPI made India a Digital Welfare State. (54) \n➔How India1’s savings surplus spur an Equity and F&O boom. (58) \nA macro-economic account of the Indian economy over the last five \nyears, from the COVID-pandemic and bust, to the recent growth taper.\nIndia - The Last Five Years Pg 7 \n India\n Indus Valley\nLong-Term Structural Forces Pg 20\n➔India’s consumption numbers look good on an overall basis, but \nnot on a per capita basis.\n➔Why India under consumes.\n➔How India1, India’s top 10%, drives the Indian economic engine.\n➔India1 is not widening as much as deepening.\n➔India1’s high share of consumption shapes the India consumer \nmarket in many distinct ways.\nConsumption Pg 66\nVenture funding trends, and a deep dive, followed by a look at \nIndia’s Unicorns, and the Venture Debt market.\nIndus Valley - Funding Trends Pg 95 \nA deep dive into India's booming IPO market, as well as the SME \nIPO’s rise, including what it implies for founders.\nIPO Boom \n Pg 111\n➔Quick Commerce: Why it works in India, the implications of its \nrise, and is there irrational exuberance re QCom? (120)\n➔AI: Is India getting a foundational model soon? (148)\nSector Deep Dives Pg 120\n➔The various India2 Playbooks. (157)\n➔How Indus Valley influenced Indian advertising. (165)\n➔Returns, and how Indian startups are addressing it. (170)\n➔Marketing framework for the Indian diaspora or India0. (179)\nIndus Valley Playbooks Pg 157 \n3",
            "4\nHow to read this report\nGiven we have sourced the data across various reports and datasets, consistency in data will always be \na challenge. That said, while sometimes an occasional number or two may not match with the other, the \nbroad direction or narrative of these is consistent and comparable. \nWe have used millions, billions, trillions (vs lacs, crores) where possible. When we use ₹ billion or ₹ \ntrillion, it can sometimes be hard to translate it to $. A shorthand for ₹ billion to $ million is that ₹1 billion = \n₹100 crores = $12 million roughly. A shorthand for ₹ trillion to $ billion is ₹1 trillion = $12 billion roughly.\nDespite all the charts and datasets we have listed, this is not a data book. We didn’t create it to serve as \nan exhaustive repository of data or reportage on India. Rather, it is more a narrative, and less a \ndataguide. Or even better, you should see it as a source of perspective on the Indian startup ecosystem. \nAnd as with all perspectives, a lot depends on the vantage point of the observer. As the leading seed \nfund in India, we do think we have a unique perspective and insight into the Indian startup ecosystem, or \nIndus Valley, as we term it. And with The Indus Valley Report, we hope to get you, dear reader, to view \nthe Indian economy through our lens. Do tell us how you see it. Compliments, criticism, feedback all \nwelcome at sp@blume.vc and / or anurag@blume.vc",
            "Section I: India",
            "6\nSource: Twitter / @dhammainvicta; The tweet was subsequently deleted\nAI meets caste. Cutting-edge tech-advances in AI collide with that most ancient of Indian institutions, the caste system.\nIndia in one tweet\nThe associations in this tweet expose a clear bias. \nMany of these would be considered inappropriate in \ncontemporary Indian discourse. \nYet, the AI completion offers a glimpse at how India’s \ndeeply rooted social structures continue to shape \nperspectives, even when filtered through modern \ntechnologies and global pop culture touchpoints.\n[Redacted]",
            "India\nIndia - The Last 5 Years\nHow we got here; a look at the events, \ntrends, policies, and initiatives that \nshaped the Indian economy over the past \nfive years through COVID, and after. We \ncover the economic downturn, \ngovernment initiatives to spur recovery, \nsubsequent boom, and inflationary \ngrowth, followed by RBI initiatives to \ncontrol inflation, and finally the growth \ntaper as consumption and government \nspends reduced.\nConsumption Pg 66\nLong-term Structural Forces Pg 20\nA macro-economic account of the Indian economy over \nthe last five years, since the COVID-pandemic and bust, \nto the recent growth taper.\nIndia - The Last Five Years \n Pg 7 \n7",
            "Real GDP Growth (in %)\nMarket Cap (in USD trillion, as on 3 January 2025)\nPer Capita Income (in USD thousands)\nCPI Inflation 2024 (in %)\nIndia - The Last Five Years\nIndia vs the World: Where India stands, today\nAlphabet \nAmazon \nMicrosoft \nNvidia\nApple\nMeta\nTesla\nSource: (Clockwise from top left) IMF, MacroMicro /Visual Capitalist, Jefferies, IMF\nIndia ranks #4 in \nthe market cap \nstandings\n8",
            "But how did we get here? \nThe next few slides capture the journey the Indian Economy has been on in the last few years.\n9",
            "10\nThe COVID-19 pandemic triggered India's worst economic contraction in its post-independence history \nCOVID pandemic dealt India a severe economic shock\nSource: MOSPI , Economics Observatory\nIndia's GDP growth rate before and during COVID\nIndia was significantly worse-off vs peers \nIndia - The Last Five Years",
            "11\nIndia - The Last Five Years\n+76.5%\n+67.5%\nGovernment Capex spends rise\nIncrease in Direct Benefit Transfers\nSubsidy surge\nGovernment’s response\nRBI’s response\nDeclining repo rates\nAggressive government spending was coupled with historically low repo rates from RBI to push the economy forward\nTo combat the economic decline, a dual response\nSource: Left three charts (clockwise from top) PRS India, DBT website, Bank of Baroda, Cleartax",
            "12\nThe RBI's extended low interest rate regime sparked an unprecedented surge in personal borrowing..\nCheap money sparks a personal credit boom…\nSource: IMA India, UBS\nPersonal loans replace industry loans as biggest \nsegment of non-food borrowings\nIn this period of 4% repo rates, consumer loans \ndrive >18% of PFCE (from <10% in FY12)\nIndia - The Last Five Years",
            "…leading to a consumption boom, sparking a V-shaped recovery\nSource: Newsclick / Reserve Bank of India, MOSPI\nIndia - The Last Five Years\nIndia engineered a remarkable recovery, with GDP growth rebounding from -5.8% in FY21 to 9.7% in FY22\n13",
            "14\nThe revival of the Indian economy was achieved through aggressive government spending, which doubled the fiscal \ndeficit between FY20 and FY21, eventually resulting in a rise in money supply. The combination of expanded money \nsupply, along with surging personal credit, and resurgent consumption pushed inflation steadily upward.\nThe cost of recovery: soaring fiscal deficit, and rising inflation\nSource: Jefferies, The Mirrority, World Bank’s Global Database of Inﬂation\nIndia - The Last Five Years\nRising fiscal deficit\nGrowing money supply\nElevated inflation rates",
            "15\nSeeing inflation rise, RBI began monetary tightening, steadily ramping up the repo rate (what banks borrow from RBI at) from \n4 to 6.5%, thereby increasing cost of money, and impacting the growth in unsecured loans.\nA concerned RBI reins in the easy money policy\nSource: Cleartax, Jefferies\nIndia - The Last Five Years\nRepo Rates back up to 6.5%\nUnsecured loan growth slowdown",
            "16\nSource: Quess / Macquarie, RBI Urban Households Survey on Inﬂation \nIndia - The Last Five Years\nWage growth below inflation across most industries\nPersistent high inflation expectations among \nhouseholds, post-COVID \nMeanwhile slow wage growth and continuing inflationary \nexpectations dampened urban consumer sentiment…",
            "17\nSource: CLSA, Axis Bank, Jefferies / CRIF\nIndia - The Last Five Years\n…even as the rural sector benefited from monsoon, higher MSP, \nincreased handouts to women, and microfinance growth\nRural outperforming urban areas in \nFMCG sales in recent quarters\n₹2Tn worth of income transfers contributing \ndirectly to household (HH) expenditure\nMicrofinance loan growth",
            "18\nSource: PNB, CLSA \nGDP growth was sustained on the back of heavy government capex spends given election year.\nSlowing consumption growth countered by heavy govt spends\nIndia - The Last Five Years\nPFCE or Private Final Consumption Expenditure growth \ndiverged from GDP growth for the first time in FY24\nCentral and state capex growth stayed strong",
            "19\nSource: CLSA, Macquarie \nIndia - The Last Five Years\nGovernment spend lagging in FY25\nThanks to slowing capex spends, on the back of already \nslowing consumption spends, GDP growth is tapering down\nPost-election spending cuts (to rein in fiscal deficit) meet \nconsumer slowdown, leading to GDP growth tapering",
            "India\nConsumption and services dominate our GDP.\nIndia is formalising, steadily.\nIndia doesn’t save enough.\nWhy land issues mean India hoards up on gold.\nIndia doesn’t invest in human capital.\nIndia’s manufacturing playbook is good, but not great.\nHow DPI made India a Digital Welfare State.\nHow India1’s savings surplus spur an equity and F&O boom.\nThe Indian economy is shaped by the interaction \nbetween, and acting upon of several powerful long-term \nstructural forces and trends. A closer look at these \nlong-term structural forces!\nLong-Term Structural Forces \nIndia - The Last Five Years Pg 7\nConsumption Pg 66\n20",
            "India\n➔\nConsumption and services dominate our GDP. \n➔\nIndia is formalising, steadily.\n➔\nIndia doesn’t save enough.\n➔\nWhy land issues mean India hoards up on gold.\n➔\nIndia doesn’t invest in human capital.\n➔\nIndia’s manufacturing playbook is good, but not \ngreat.\n➔\nHow DPI made India a Digital Welfare State.\n➔\nHow India1’s savings surplus spur an Equity and \nF&O boom.\nLong-Term Structural Forces \nConsumption and \nservices dominate \nour GDP\nConsumption and services drive the \nIndian economy, unlike say in China, \nwhere investments and manufacturing \nplay a key role. \nIndia - The Last Five Years Pg 7\nConsumption Pg 66\n21",
            "22\nIndia’s GDP $3.6 trillion / ₹295.4 trillion (FY24)\nTwo ways to understand GDP\nSource: MOSPI\nIndia - Long-Term Structural Forces / Consumption and Services\nPFCE\n(Consumption)\n56%\nGFCF\n(Investment)\n33%\nGovt. Spends 9%\nServices\n54%\nIndustry\n31%\nAgriculture\n15%\nOthers (Exports less \nImports etc ) 2%\nIndia’s GDP by expenditure components\nIndia’s GDP by sectoral split",
            "23\nIndia’s GDP is heavily dependent on consumer spending\nSource: Jefferies\nPFCE\n(Consumption)\n56%\nGFCF\n(Investment)\n33%\nGovt 9% \nOthers 2%\nIndia’s GDP by expenditure components\nPFCE has consistently been at 55-60% of Indian GDP through the last decade\nIndia - Long-Term Structural Forces / Consumption and Services",
            "24\nA key reason is our middling savings rate and low FDI constricting investment in productive assets. India’s FDI inflows for \nFY11-20 were $512 billion while China’s for 2011-20 were over 4x that at $2.4 trillion.\nSource: CLSA / MOSPI, Trading Economics, PIIE, IBEF\nInvestment or Gross Fixed Capital Formation (GFCF) has been a \nmuch smaller contributor to GDP\nChina\n2000-09 | 37.8%\n2010-19 | 43.2%\n2020-23 | 41.9%\nChina\n2000-09 | 44.7%\n2010-19 | 46.7%\n2020-23 | 44.7%\nGFCF as % of GDP\nGross Savings Rate\nIndia - Long-Term Structural Forces / Consumption and Services",
            "Construction (9%)\nMining & Utilities (5%)\nManufacturing(17%)\n25\nServices sector dominates the Indian economy\nSource: MOSPI, PLFS 23-24\nFinancial & \nProfessional Services, \nReal Estate (23%)\nTrade, Transportation, Hotels, \nCommunication (19%)\nPublic Services (13%)\nManufacturing punches well below the ideal \nweight. China’s equivalent number is 26%. We \ndeep dive into reason’s for manufacturing’s low \nshare and its potential in a subsequent section.\nReal Estate / Construction sector is a key sector \nas it is a large employer of unskilled workers. It \naccounts for 12% of India’s labour force, more \nthan manufacturing (11.4%)!\nServices is a large contributor to India’s \neconomy; unusual for a country with per capita \nincome under $3k. \nServices\n54% of GDP\n31% of Labour Force\nIndustry\n31% of GDP\n23% of Labour Force\nAgriculture\n15% of GDP\n46% of Labour Force\nIndia’s GDP by expenditure components\nServices Labour Force % Split\nIndustry Labour Force % Split\nIndia - Long-Term Structural Forces / Consumption and Services",
            "26\nServices dominating Industry is not a new trend\nSource: CLSA\nIndustry and manufacturing \nhas consistently been a \nsmaller portion of the \neconomy than services.\n% Share of Gross Value Added (GVA): Agriculture, Industry and Services FY64-FY24\nIndia - Long-Term Structural Forces / Consumption and Services",
            "27\nServices strength is visible in increasing market share of global \nexports (unlike Goods exports)\nSource: Goldman Sachs\nIndia’s share of global services exports is up from 2% to nearly \n5% of global trade over the past two decades\nIndia’s services exports has grown nearly 2x relative to peers \nlike Brazil and Mexico\nIndia - Long-Term Structural Forces / Consumption and Services",
            "28\nIT Exports are the crown jewel of our services economy\nSource: Goldman Sachs, CLSA, Jefferies / Nasscom\nGCC headcount has \nmore than doubled in \nunder the last \ndecade, albeit \nbenefitting from a \nlower base.\nFrom a fifth of the \nsize of IT Services, \nGCCs are now a third \nof IT Services \nrevenues; all this in \nunder a decade.\nAnd of late, Professional Consulting Services and GCCs stepping up too!\nProfessional Consulting has been growing faster than IT \nServices, though from a lower base.\nIndia is a global leader with 1,700 Global Capability \nCentres (GCCs). GCC headcount and revenue is growing \nfaster than IT Services.\nIndia - Long-Term Structural Forces / Consumption and Services",
            "India\n➔\nConsumption and Services dominate our GDP. \n➔\nIndia is formalising, steadily.\n➔\nIndia doesn’t save enough.\n➔\nWhy land issues mean India hoards up on gold.\n➔\nIndia doesn’t invest in human capital.\n➔\nIndia’s manufacturing playbook is good, but not \ngreat.\n➔\nHow DPI made India a Digital Welfare State.\n➔\nHow India1’s savings surplus spur an Equity and \nF&O boom.\nLong-Term Structural Forces\nIndia is formalising \nsteadily\nWe are seeing a steady but firm shift to a \norganised, branded, formal market, from \nwhat was an unorganised, unbranded, \nand informal market.\nIndia - The Last 5 Years Pg 7\nConsumption Pg 66\n29",
            "30\nThe Indian economy is formalising, shifting from unorganised \nto organised\nSource: Jefferies, GST Council\nIndia - Long-Term Structural Forces / Formalisation\nIncreasing share of income captured in direct tax filings\nGrowth in registered GST payees indicates a formal shift",
            "31\nSigns of formalisation visible in the consumer economy too \nSource: CLSA\nJewellery market formalisation\nReal estate market formalisation\nIndia - Long-Term Structural Forces / Formalisation",
            "32\nFrom B2C to B2B we are seeing branded products gain market share\nSource: Jefferies, Vedant Fashions DRHP\nFans market shift\nWedding and celebration-wear shift\nCables and wires shift\nIndia - Long-Term Structural Forces / Formalisation",
            "India\n➔\nConsumption and services dominate our GDP \n➔\nIndia is formalising, steadily. \n➔\nIndia doesn’t save enough.\n➔\nWhy land issues mean India hoards up on gold.\n➔\nIndia doesn’t invest in human capital\n➔\nIndia’s manufacturing playbook is good, but not \ngreat\n➔\nHow DPI made India a Digital Welfare State\n➔\nHow India1’s savings surplus spur an Equity and \nF&O boom\nLong-Term Structural Forces \nIndia doesn’t save \nenough\nIndia’s savings is good but not \ngreat. A high savings rate is \nnecessary given low FDI rates. A \ndeep dive into savings illustrates \nthat the culprit is financial savings \n(as opposed to physical savings), \nand the reason is rise in financial \nliabilities, chiefly led by rising \n(unsecured) personal loans.\nIndia - The Last Five Years Pg 7\nConsumption Pg 66\n33",
            "34\nWorryingly, household savings, the biggest contributor, is seeing a declining share\nIndia’s overall savings rate looks ok, but is not\nSource: Jefferies, Economic Survey, MOSPI, RBI\nIndia - Long-Term Structural Forces / Savings\nHousehold financial savings dropped from 10.1% \nto 5.% primarily as a result of financial liabilities \nincreasing from 2 to 5.8% in the same period.\nHousehold savings make up the majority of savings. \nThey have been steadily declining (barring a \npandemic-induced rise in ‘21)\nIndia has a much lower savings rate \nthan its Asian peers, \nespecially China\nA key reason for household savings \nshare dropping is the drop in \nfinancial savings\nHousehold share of savings has \ndropped from 84% in FY00 to just \n61% in FY23! \n30%\n18.4%",
            "35\nSource: CLSA, BIS, IIF\nSharp rise in indebtedness of the Indian household\nDriven by the increasing share of \nconsumer loans in credit market\n3/4th of household debt is non-housing \ndebt which is high relative to others\nMeanwhile, household debt to GDP \nhits an all-time high\nIndia - Long-Term Structural Forces / Savings",
            "Increasingly, NBFCs including fintechs and not banks lead the sourcing, typically digitally\nMuch of the indebtedness is due to the rise in Small Ticket \nPersonal Loans (STPL)*\nMuch of it is led by Small Ticket Personal \nLoans (STPL) or loans under ₹100,000\nAverage personal loan size is a fourth \nof what it was\nNBFCs including digital lenders\n dominate sourcing\nLeading to a dramatic 48x rise in STPL loan \nvolumes since 2017\n*Small Ticket Personal Loans or STPL is loans below ₹100,000/-. Source: CRIF Highmark - How India Lends\n6x rise in Personal Loans origination \n(value) over last 7 years\nBut a 22x rise in number of loans originated \n(volume)\n36\nIndia - Long-Term Structural Forces / Savings",
            "India\n➔\nConsumption and services dominate our GDP. \n➔\nIndia is formalising, steadily.\n➔\nIndia doesn’t save enough.\n➔\nWhy land issues mean India hoards up on gold.\n➔\nIndia doesn’t invest in human capital.\n➔\nIndia’s manufacturing playbook is good, but not \ngreat.\n➔\nHow DPI made India a Digital Welfare State.\n➔\nHow India1’s savings surplus spur an Equity and \nF&O boom.\nLong-Term Structural Forces \nWhy land issues mean \nIndia hoards up on \ngold.\nIndia is the world’s second largest \nconsumer of gold. Behind this are cultural \nfactors, and economic factors, chiefly the \npoor land records, and the challenges in \ncollateralising land. Gold is a far more \nconvenient collateral as we see from \nthese slides.\nIndia - The Last Five Years Pg 7\nConsumption Pg 66\nThis section was authored by \nJoseph Sebastian, from Blume’s \nFintech team \n37",
            "India is the 2nd largest consumer of gold globally; and as Indians’ preferred savings instrument, gold's impact is seen \nacross our economy\nIndians have a special relationship with gold\nSource: gold.org, JM Financial, Business Standard\nBy contrast, other nations typically keep just \n2–3% of household wealth in gold vs India \nwhich keeps as much as 16%\nIndia is the largest jewellery market in the \nworld; thanks in part to India’s wedding industry\nLarge gold imports significantly impact \nour Current Account Deficit (CAD), in turn \ninfluencing rupee strength and policy \ndecisions \nIndia is the second largest \nconsumer of gold in the world\n1\nSo much so that it has material impact \non our current account deficit\nAfter property, gold accounts for the \nlargest share in household assets\n2\n3\n38\nIndia - Long-Term Structural Forces / Gold",
            "For borrowers, no credit history is \nrequired as gold is a secure product so \nthey can get loans very easily.\nWhy is gold preferred? Not just because of its cultural significance \nbut also because it is a great collateral\nIn rural communities, gold is the \nprimary way to save\nAccessible credit for borrowers\nTrusted collateral for lenders\nFor farmers and traders, gold acted as a \npractical cash flow tool. They purchase \ngold during periods of surplus and use it \nas collateral for loans during times of \ncash requirements.\nFor lenders, gold-backed loans offer a \nsignificant advantage since the collateral \nis relatively simple to repossess if \nneeded and It can be quickly sold in \ncase of default.\n1\n2\n3\nSource: Fortune India, Indian Express, Financial Express\n39\nIndia - Long-Term Structural Forces / Gold",
            "What makes gold even more attractive in India, is that land in India is \nnot a good source of collateral\nIndia has one of the smallest \nhousing loan market\nOne of the main reasons for that is \nIndia’s dispute resolution / contract \nenforcement mechanism is broken\nWhich makes India one of the lowest in \nthe world in contract enforcement\nSource: World Bank\nThere are a whopping 47 million pending cases \nin the Indian courts. 66% of these are estimated \nto be linked to land as per Daksh India.\nEconomic growth stories in places like South \nKorea depended on credit creation through the \nmortgage industry. India's housing mortgage \nmarket is far lower than other countries \nbecause property is a more complex form of \ncollateral compared to gold.\nChina\n#5\nUnited \nStates\n#17\nBrazil\n#58\nVietnam\n#68\nKenya\n#89\nIndia \n#136\n#190\nWith one of the world's smallest housing loan market and lengthy contract enforcement (1,445 days), gold emerges as the \npractical collateral choice because land can’t\n1\n2\n3\n40\nIndia - Long-Term Structural Forces / Gold\nWeak contract enforcement reduces the \nconfidence amongst lenders that property can \nbe repossessed easily in the event default, thus \nmaking land an inefficient form of collateral",
            "India\n➔\nConsumption and Services dominate our GDP. \n➔\nIndia is formalising, steadily.\n➔\nIndia doesn’t save enough.\n➔\nWhy land issues mean India hoards up on gold.\n➔\nIndia underinvests in human capital.\n➔\nIndia’s manufacturing playbook is good, but not \ngreat.\n➔\nHow DPI made India a Digital Welfare State.\n➔\nHow India1’s savings surplus spur an Equity and \nF&O boom.\nLong-Term Structural Forces \nIndia underinvests in \nits human capital\nBehind India’s underinvestment in human \ncapital, is a set of complex interlinked \nfactors but chiefly path dependence from \nits decision post-1947 to invest in the \ntertiary education sphere over the \nprimary and secondary education sphere \n(unlike the Asian Tigers and China which \ninvested in primary and secondary \neducation over tertiary) and developed a \nskilled labour force.\nIndia - The Last Five Years Pg 7\nConsumption Pg 66\n41",
            "Source: Jefferies, PLFS (2023-24)\nUnemployment Rate is per usual status , i.e. if a person worked 30 days in a year, they are considered as employed for the year\nIndia - Long-Term Structural Forces / Human Capital\nIndia’s Labour Landscape Snapshot\nNuances of India’s Workforce\n326.5 Mn\n110.7 Mn\n70.3 Mn\n51.0 Mn\n20% Casual Workers\n58% Self-Employed \n(33% of self-employed are unpaid helpers in a household enterprise)\n3.2% Unemployed\n13% Regular Salary Employees without job contract\n9% Regular Salary Employees with job contract\n18 Mn\nPeers: % Regular Salary Employees in the Workforce\nRussia\n93%\nBrazil\n68%\nChina\n54%\nBangladesh\n42%\n42",
            "43\nSource: PLFS 2023-24, Trading Economics, IMF\nIndia has a disguised unemployment problem and a jobless \ngrowth problem\nAgriculture accounts for 46% \nof jobs in India…\nJobless growth in manufacturing\nDisguised unemployment in agriculture\n…but only contributes to 15% \nof GDP\nIndicating a problem of disguised unemployment.\nGiven manufacturing in India is more capital intensive than labour \nintensive, jobless growth is a likely scenario.\nIndia - Long-Term Structural Forces / Human Capital",
            "India’s youth unemployment rate by level of education (%), 2022\n44\nSource: ILO\nBut what’s worrying is higher the education level, higher the \nunemployment rate\nIndia - Long-Term Structural Forces / Human Capital",
            "45\nSource: Twitter / Pritesh Lakhani, Twitter / Haidar Naqvi, , ‘Accelerating India’s Development’ by Karthik Muralidharan\nBecause India’s youth want ‘AC’ jobs or government jobs\nEmployment (un)willingness\nWhy aren’t there enough \ngovernment jobs?\nEverybody wants a government job\nWe have fewer government jobs than our peers but \nthese are highly paid relative to the private sector. \nKarthik Muralidharan in his book ‘Accelerating \nIndia’s Development’ describes how government \nschool teachers are paid 5-10 times more than \nprivate school teachers. The high pay and job \nsecurity is a key reason for the high demand for \ngovernment jobs and the many years invested in \nwriting exams to break into these jobs.\nIndia - Long-Term Structural Forces / Human Capital",
            "46\nSource: CII, Twitter / Paul Novosad featuring the work of Nitin Kumar Bharti and Li Yang\nThe underlying issue? India under invests in its human capital\nEducation spending as a % of GDP\n (India vs Peers)\nFocus on humanities and social \nsciences over technical areas\nFocus on tertiary education while \nneglecting primary education\nIndia - Long-Term Structural Forces / Human Capital",
            "47\nSource: MacroTrends, Ministry of Skill Development,, Moneycontrol / Shankar Sharma\nIndia’s demographic dividend is underway. To take advantage of it we \nhave to focus on upskilling our workforce, and AI-proofing them!\nDemographic dividend is the phase in which the proportion of working-age population (typically ages 15-64) increases rapidly compared to number of \ndependents (children and elderly). India’s demographic dividend phase began in 2018 and will run till 2055. Japan’s was 1964-2004 and so on.\nIndia v Peers, GDP growth in first 7 \nyears of demographic dividend\nIndia has far fewer population that has \nundergone formal skills training\nUnfair but relevant comparison - India was \ngreatly impacted by COVID led GDP decline.\n“India's reliance on services has made it \na shining star in the emerging world. \nBut AI is a howitzer aimed squarely at \nthat prosperity. The effect AI will have \non India will be profound. Too much has \nbeen written, said and marketed about \nIndia's demographic dividend…All it \ntakes is $29.95 a month to morph it into \nDemographic Debt. Or Demographic \nDust.” \n - Shankar Sharma\nThe above is from a 2019 Ministry of Skill Development report. \nIt is very likely that India’s number has increased today.\nIndia - Long-Term Structural Forces / Human Capital",
            "India\n➔\nConsumption and services dominate our GDP. \n➔\nIndia is formalising, steadily.\n➔\nIndia doesn’t save enough.\n➔\nWhy land issues mean India hoards up on gold.\n➔\nIndia doesn’t invest in human capital.\n➔\nIndia’s manufacturing playbook is good, but \nnot great.\n➔\nHow DPI made India a Digital Welfare State.\n➔\nHow India1’s savings surplus spur an Equity and \nF&O boom.\nLong-Term Structural Forces \nIndia’s manufacturing \nplaybook is good, but \nnot great.\nIndia has struggled to grow its \nmanufacturing sector historically, though \nit is making a spirited attempt now using \nimportant bans, tariffs, and \nproduction-linked incentives. The journey \nhas been impressive but not as good as \nsay Vietnam’s.\nIndia - The Last Five Years Pg 7\nConsumption Pg 66\n48",
            "49\nSource: World Bank\nIndia has historically underperformed on the manufacturing front\nIndia also ranks well below its peers when comparing \nmanufacturing’s share of GDP\nIndian manufacturing’s share of GDP is at its lowest ever!\nIndia - Long-Term Structural Forces / Manufacturing",
            "50\nSource: Ministry of Skill Development, Bloomberg, SBI / YCharts\nBecause of land, labour and capital\nLow skill levels in the Indian labour force mean \nthat despite lower wages, the net impact is neutral \nas a lower-skilled workforce is less productive.\nIndustrial land is expensive in India vs other \nsimilar economies. Path dependence over history \nled by fragmented of land parcels, unclear title \nrights etc., explain the higher cost of land \nacquisition. Below chart from a Bloomberg \narticle by Andy Mukherjee.\nLending rates are much higher in India vs \nother countries - SME loans are at low double \ndigit whereas Chinese companies get at 4%. \nMultiple reasons abound, but essentially India has \nhigher cost of capital.\nGovernment overheads are \nsubstantially higher in India!\nThe above is from a 2019 Ministry of Skill \nDevelopment report. It is very likely that \nIndia’s number has increased today.\nLabour\nCapital\nLand\nLand costs \nare 25% \nhigher!\nIndia - Long-Term Structural Forces / Manufacturing",
            "51\nSource: Reuters, Hindu BusinessLine, Business Standard, Times of India, Nuvama, Business Today\nIndia is looking to rework its trajectory by the use of bans, tariffs, \nand incentives\nImport bans to promote making in India in \ndefence, electronics. and durables\nProduction-Linked Incentives (PLIs) worth \n$33bn over 5 years across 14 sectors\nHigher tariffs than emerging market peers \nlike Brazil, Vietnam and China\nIndia tariffs at 11% higher than other Emerging \nMarket peers such as Brazil (9%), Vietnam \n(5%), and China at 3%\nIndia - Long-Term Structural Forces / Manufacturing",
            "52\nSource: Jefferies, The Wire, Business Standard\nAnd the effects are beginning to be seen in various industries\n“Electronic manufacturing sector is an example \nof the change that the scheme is bringing. Seven \nyears ago we used to import mobile phones of \napproximately USD 8 billion. Today, we are \nexporting mobile phones worth USD 3 billion” - \nPM Narendra Modi, 15 August 2021 speech\nFrom FY20 to FY24, India raised tariffs \non imported toys from 20% to 70%, \nleading to India becoming a net exporter\nImport bans have reduced home air \nconditioner imports from 45% to 5%\nTariffs played a huge part to make toys \nexport possible\nElectronics industry supported by PLI \nscheme has seen exports take off\nIndia - Long-Term Structural Forces / Manufacturing",
            "Source: JP Morgan, US Census website\nWhile India’s Import to US increased by \n60%, Vietnam saw a ~3x jump as \ncompared to India.\nChina has seen a drop of nearly $100 \nbillion in its exports to the U.S\nBut we weren’t the prime beneficiaries of China + 1; Vietnam very likely was!\n53\nIndia - Long-Term Structural Forces / Manufacturing\nThat said we are still in the early days of a manufacturing revival",
            "India\n➔\nConsumption and services dominate our GDP. \n➔\nIndia is formalising, steadily.\n➔\nIndia doesn’t save enough.\n➔\nWhy land issues mean India hoards up on gold.\n➔\nIndia doesn’t invest in human capital.\n➔\nIndia’s manufacturing playbook is good, but not \ngreat.\n➔\nHow DPI made India a Digital Welfare State.\n➔\nHow India1’s savings surplus spur an Equity and \nF&O boom.\nLong-term Structural Forces \nDPI has helped India \nbecome a ‘Digital \nWelfare State’\nA good way to understand India is as a \nDigital Welfare State, one that leverage \nDPI protocols to deliver cash and in-kind \nbenefits directly to the end users. Not all \nDPI protocols necessarily succeed, and \nwe are beginning to see second-order \neffects of DPI policies emerge!\nIndia - The Last Five Years Pg 7\nConsumption Pg 66\n54",
            "India - Long-Term Structural Forces / DPI\nThanks to DPI, India is now a digital welfare state\nSource: Motilal Oswal, DBT Website, People by WTF\nGovernment has introduced a slew of DPIs…\n…driving socio-economic impact through DBTs\n“Today, in just 30 seconds, I can \ndirectly transfer money into the \naccounts of 100 million farmers. \nToday, I can send subsidy to 130 \nmillion gas cylinder consumers with \njust one click, in 30 seconds. Billions \nthat were being siphoned out due to \ncorruption are now saved.” \n - PM Narendra Modi\nAadhaar (Unique \nID) + Mobile + \nBank Account \n(Jan Dhan \nAccount) has \nenabled direct \nbenefit transfers \nand reduced \nleakages in the \nsystem.\nPeople by WTF, Nikhil Kamath\nAadhar\n1382 mn\nusers in 2024\nUPI\n330 mn\nusers in 2023\nBHIM\n217 mn\nusers in 2023\nDIGIT\n250 mn\nusers in 2022\ne-Sanjeevani\n148 mn\nusers in 2023\nCo-WIN\n1190 mn\nusers in 2023\nABHA\n440 mn\nusers in 2023\nAA\n25 mn\nusers in 2023\n2000\n2016\n2018\n2019\n2021\n2022\nONDC\n700k sellers\n150 mn \ntransactions\n55",
            "As DPI protocols flood the market, some find immediate success \nwhile others are yet to find their feet\nSource: NPCI Website, ONDC Website, NASSCOM\n# of Mobility Orders\n# of Retail Orders\nNumber of users on MyGov is on the rise,but the \nactual penetration is quite low at 2% of population\nWhile mobility players on ONDC have seen success, \nretail is still finding its feet\nUPI is the runaway hit product of India Stack\nUPI\nONDC\nMyGov\n56\nIndia - Long-Term Structural Forces / DPI",
            "June \n2024\nDec \n2024\n57\nSource: India Quotient, RBI Payments Systems Report , Moneycontrol, Techcrunch, \nAs UPI hits maturity, we are seeing its second order effects\nUPI winning market share \nfrom debit and credit cards\n…but 0% MDR taking out profit pools for \nPayment Service Providers\nUPI processed 172 billion transactions \nworth over ₹ 245 tn ($~3tn) in 2024. It \naccounted for 83% of all digital \ntransactions in 2024, compared to just \n34% five years ago.\n…and is beginning to impact demand for \ncash amongst the upper income tier…\nJune \n2024\nDec \n2024\nNPCI, in March 2023, introduced an interchange fee of \n1.1% on P2M transactions >Rs.2000 made via \nprepaid instruments like a mobile wallet or prepaid \ncard. While this is a small portion of the revenue pool, it \ncould signal the introduction of MDRs for other \ntransaction types.\nIndia - Long-Term Structural Forces / DPI",
            "India\n➔\nConsumption and services dominate our GDP. \n➔\nIndia is formalising, steadily.\n➔\nIndia doesn’t save enough.\n➔\nWhy land issues mean India hoards up on gold.\n➔\nIndia doesn’t invest in human capital.\n➔\nIndia’s manufacturing playbook is good, but not \ngreat.\n➔\nHow DPI made India a Digital Welfare State.\n➔\nHow India1’s savings surplus spur an equity \nand F&O boom.\nLong-term Structural Forces \nHow India1’s savings \nsurplus spur an equity \nand F&O boom. \nIndia - The Last Five Years Pg 7\nConsumption Pg 66\nIndia1’s surplus savings are finding their \nway into the equity market, creating the \n4th largest equity market, and the biggest \nequity derivatives market (by volume). \nSEBI has come down hard on the equity \nderivatives market (effectively ‘financial \ngambling’) and the impact is visible.\n58",
            "India’s affluent class has seen rising \ndisposable income and growth…\n59\nSource: CLSA, Jefferies, JM Financial\nIndia - Long-Term Structural Forces / Equity\nAs disposable income increases, equity emerges as a new way to \nsave for Indians\n1\nEquity’s share of HH savings \nhas more than doubled over \nthe last 10 years.\n…of which more and more is being \ninvested in public markets.\n…which over time this manifests in a \nsizeable savings pool…\n2\n3",
            "60\nSource: NSE, AMFI\nDomestic capital is increasingly driving the Indian stock market\nDomestic investor ownership of Indian \nstocks catching up steadily to Foreign \ninvestor ownership\n1\n…with around half of those inflows \ncoming from Mutual Fund SIPs\nDomestic institutional investor (DII) \nflows into Indian stock market at record \nlevels… \n2\n3\nIndia - Long-Term Structural Forces / Equity",
            "61\nSource: Bloomberg, AMFI\nBut until when can domestic monies drive the market?\nSIP cancellations to registrations have risen to 64% in \nApr-Dec24. In FY24 it was at 52%\nAs equity returns drop and FII continue to sell how long \ncan retail funds keep flowingII\nIndia - Long-Term Structural Forces / Equity",
            "62\nSource: NSE Pulse, BSE, Jefferies\nDid you know India is the largest derivative market in the world?\nThis is on the back of index options (e.g., Nifty, Bank Nifty \netc.) which has grown 26x over the last 6 years\nIndia is the largest derivatives contracts market globally\nADTO above = Average Daily Turnover. This chart shows the \naverage daily turnover of index options vs regular stock trading; \nwhile in FY19 index options was ~7% of regular stock trading, \ntoday it is over half!\nIndia - Long-Term Structural Forces / Equity",
            "63\nSource: Jefferies, Twitter / Rajesh Sawhney\nMuch of the volume is driven from short term speculative trades \ndone by retail investors\nAdditionally, 65% of all contracts were weekly rather \nthan monthly in nature, i.e., held for a maximum of \none week versus one month. Effectively derivatives are \ntreated as quasi-gambling products by ‘investors’.\nUnlike U.S. where most option trades \nare held for longer periods (hence \n‘outstanding’), India's trades are \nshort-term and hence settled fast.\nAnd this boom is mainly led by retail \ninvestors\nBecause of low premiums, there has \nbeen a boom in very short-term \ncontracts: 73% of (index option) trades \noccurred on the last day of expiry.\nIndia - Long-Term Structural Forces / Equity",
            "64\nSource: NSE Pulse, SEBI, Twitter / Alok Jain\nRetail participation in F&O trades shoots up, but more than 90% of \nparticipants lose money!\nAbove via a SEBI study on equity derivatives \nwhich concluded that in FY24, individuals lost ~ \n₹41,000crs / ₹410 Bn and about 91.1% of them \nmade net losses in F&O amounting to an \naverage of ₹1.2 lakh / ₹120k loss per person\nRetail participation in the derivative \nmarket have grown exponentially, going \nfrom <1mn in 2017 to closer to \n12mn in 2024\nPeople are making losses to the tune of \n10-15% of their income, says this tweet\nBut most individual investors lose \nmoney\nIndia - Long-Term Structural Forces / Equity",
            "65\nSource: Indian Express, Jefferies\nLeading to SEBI’s intervention; and the impact can be seen!\nAverage daily Index option contracts declined 37% in Dec’24 and a \nfurther 52% in Jan’25\nSEBI has increased lot sizes, reduced \nweekly contracts, mandated upfront \npremium collection etc to curb \nspeculative behaviour.\nAnd the effects have starting to be seen with decreased volumes and lower expiry day \ntrades\nIndia - Long-Term Structural Forces / Equity",
            "A deep dive into India’s consumption patterns, and the \nIndian consumer stack, including India1 and how it \nshapes the Indian consumer market.\n India\nConsumption\nIndia’s consumption numbers look good \non an overall basis, but not on a per \ncapita basis. We take a look at why this \nis so. We look at how India1, India’s top \n10%, drives the Indian economic engine, \nand find that India1 is not widening as \nmuch as deepening. Finally, we show \nhow India1’s high share of consumption \nshapes the India consumer market in \nmany distinct ways.\nConsumption Pg 66\nLong-Term Structural Forces Pg 20\nIndia - The Last Five Years Pg 7\n66",
            "Source: Twitter / Vivek Raju\n67",
            "68\nIt has consistently been above 55% since ‘00; Investment / GFCF plays a far lesser role unlike in China\nConsumption is the dominant driver of India’s GDP \nSource: Jefferies, World Bank \nIndia - Consumption\nHow we stack up vis-a-vis China\nGFCF is essentially creation of productive assets such \nas machinery, infrastructure. Unlike India, investment \n(GFCF) plays a larger role in China’s GDP at 41% vs. \nIndia’s 31%. \nNote: PFCE at 60.3% differs from PFCE of 56% on Slide #24; 60.3% is at current prices, while 56% was at constant prices (2011-12).\nIt is hard to get long time-series data for constant prices.",
            "69\nThis is how Indian Consumption stacks up\nSource: Bernstein, NSSO, Redseer\nGDP split\n(basis current prices)\nHow consumption \nsplits up\nHow retail breaks \ndown into segments\nGFCF\n30%\nGovt. \nExpenses \n& Others\n10%\nRetail\n$1.1 Tn \n55%\nServices\n$1 Tn \n40%\nOther Retail\n$270 Bn (27%)\nRestaurants\n$70 Bn (7%)\nFashion & BPC\n$110 Bn (10%)\n(Consumer Durables, Gems & \nJewellery etc)\nOnline (7%)\nOffline \n(93%)\nUnbranded \n(63%)\nBranded \n(37%)\nNon\nDiscretionary\n(71%)\nDiscretionary \n(29%)\nConsumption \n$2.1 Tn \n60%\nGrocery & FMCG\n$550 Bn (50%)\n We can also split retail in 3 other ways\nIndia - Consumption",
            "70\nRelative to large economies, India’s consumption growth is amongst the highest\n~60% of $3.7 trillion makes for a sizeable consumption market\nSource: UBS\nIndia is the 5th largest consumption market globally\nIndia’s consumption growth outpaced major global \neconomies\nIndia - Consumption",
            "71\nOn per capita basis though, India’s consumption metrics look \nless impressive \nSource: World Bank, CLSA \nWe are roughly \nwhere China was \nin 2010\nIndia vs Indonesia vs China: Consumption Expenditure Per Capita (in USD) \nIndia - Consumption",
            "72\nReflected in under penetration and under consumption across \nseveral categories, such as financial products…\nSource: CLSA\nSource: Jefferies\nSource: FT Partners\nAnon fintech founder: \n“35-40M unique card \nholders. But active will be \nin range of 22-28M”\nSource: BCG / Z47 \nWhile number of MF \ninvestors has risen of \nlate, penetration still \nremains low.\nIndia - Consumption",
            "73\n…and 2 Wheelers, Air-Conditioners, FMCG, Footwear…\nSource: Jefferies\nSource: CLSA / Technopak\nSource: Ola DRHP\nSource: Jefferies \nRural per-capita FMCG \nspends are even lower, \nat one third of urban.\nIndia accounts for \n~7% of global AC \nunits sold. China \nwas ~55%.\nIndia - Consumption",
            "74\n…and Cement, Electricity, Hotels, Tourism.\nSource: Jefferies\nSource: Jefferies, KPMG\nSource: Jefferies\nSource: CLSA\nSome of the data on the \ntable will shift post COVID \nas numbers are updated, \nbut in India’s case we don’t \nestimate the numbers to \nshift much basis recent \ntraffic data.\nIndia - Consumption",
            "75\nIndia - Consumption \nWhy does India consume so little? Why are penetration rates \nso low across so many categories?\nThe answer likely lies in the nature of the consumer economy structure, or the \nIndian consumer stack as we term it.",
            "India 1\n‘Mexico’\nIndia 2\n‘Indonesia’*\nIndia 3\n‘Sub-Saharan Africa’\nThe Consuming \nClass\n~30m households\n~140m people\n~$15K per person\nIndia1 is the consuming class, and effectively constitutes the \nmarket for most startups. Also most startups start here and \nthen expand to India2.\nThe Aspirant \nClass\n~70m households\n~300m people\n~$3k per person\nIndia2 is the emerging aspirant class. They are heavy \nconsumers and reluctant payers. OTT / media, gaming, \nedtech and lending are relevant markets for them. UPI and \nAutoPay has unlocked small ticket spends and transactions \nfrom this group.\nUnmonetisable\nUsers\n(& Non-Users)\n~205Mn households\n~1Bn people\n~$1k per person\nIndia3 doesn’t have the kind of incomes to be able to spend \nanything on discretionary goods. They are beyond the pale, \nas of now, for startups.\nSome apps straddle different \nIndias e.g., Whatsapp, Youtube, \nFlipkart etc. A good way to \nunderstand the above is that all \napps in India3 can be used by \nIndia2 and India1. Similarly \nIndia2 apps can be used by \nIndia1. The reverse isn’t true. \nIndia1 apps are not used by \nIndia2 or India3.\n* Indonesia’s per capita income is $5k; strictly this is not the right country analogy for India2, but we couldn’t get a country that has a population of ~300m \nwith a per capita income of $3k. So please bear with us for this. \nHow Blume looks at the consumer stack\n76\nIndia - Consumption\nSource: Blume Research",
            "77\nThis undersized consuming class is reflected in other estimates too…\nSource: Bernstein, UBS, Redseer \n790 mn \n(Income < $3.3K)\n430 mn \n(Income $3.3k - $6k)\n65 million \n(Income $6k -$12k)\n65 million \n(Income > $12k)\n538 million \n(Income < $1.5k)\n222 million \n(Income $1.5k - $2.5k)\n193 million \n(Income $2.5k - $5k )\n79 million (Income $5k - $10k)\n40 million (Income > $10k)\n525 million \n(Income < $3.5k)\n720 million\n(Income $3.5k - $14.2k)\n140 million \n(Income $14.2k - $25k)\n35 million \n(Income > $25k)\nNote: UBS has estimated the above for 15+ population only\nBernstein (2024)\nUBS (2023)\nRedseer (2022)\nIndia - Consumption",
            "78\nIndia1 is the engine of the Indian consumer economy\nSource: Blume / Bernstein estimates, Goldman Sachs\nIndian consumer stack by share of household \ndiscretionary spend\nIndia1\nIndia 2\nIndia 3\nBlume Consumer Stack\nHow the urban top 10% over index on consumption\n~10% of population\n2/3rd share of discretionary spends\n~23% of population \n1/3rd share of discretionary spends\n2/3rds of the population\nDip into their savings (slight negative \nshare of discretionary spends)\nThis means Urban India top 10% spends 13x of the average per capita \nspend on Durables, and so on.\nIndia - Consumption",
            "79\nHowever, India1 is not widening… \nSource: UBS, Citi, Zomato Quarterly Reports\nCOVID slowdown\nCOVID slowdown\nDomestic air passenger traffic has not \ngrown much after FY21-22 COVID \nslowdown\n2W sales volumes have remained muted \nfollowing FY21-22 COVID slowdown\nFood ordering MAUs\nIndia - Consumption",
            "80\n…as much as it is deepening.\nSource: CLSA, Jefferies, UBS \nRising share of premium and executive \nsegment motorcycles FY19 - FY23\nShare of high-end to ultra-luxury housing \nhas doubled in last five years\nLow-end smartphone sales contract as \nmid-premium segment expands\nIndia - Consumption",
            "81\nNot widening as much as deepening: A look at car sales in India\nSource: Autopunditz, CLSA \n4.5% CAGR\nSlow-growing passenger vehicle market…\n…with a sharp rise in premium segments\nIndia - Consumption",
            "82\nNot widening as much as deepening: A look at taxpayers in India\nSource: Direct Taxes Data, Government of India\nA small number of taxpayers are \nshouldering the tax burden\nIn FY23, only 2% Indians paid tax \n(and will go down further per the \nexemptions announced Feb’25). In \ncontrast: In China, ~10% paid tax, \nand in USA, ~43% paid tax.\nThe gap between tax filers and tax payers is widening. The recent \nbudget exemptions will further reduce the number of taxpayers.\nIndia - Consumption",
            "83\nRising share of incomes, and presence atop wealth charts validate \nthe India1 deepening story\nSource: UBS, World Inequality Lab\nIndia’s wealth growth rates were the fifth highest globally\nIndia1’s share of national income has steadily increased\nMiddle 40%\nTop 10% \nBottom 50%\nIndia - Consumption",
            "84\nIndia1’s high share of consumption shapes the Indian \nconsumer market in many distinct ways.\nIndia - Consumption",
            "85\nIndia1 is helping spark a fast-growing equity market…\nMarket cap to GDP ratio touching all time highs (in %)\nAnnual SIP contributions are at all time high (in INR trillions)\nNSE investors (Equity + F&O) up 5x from 2019 (in millions)\nEquity share in household savings up 2.5x in a decade (in %)\nSource: CEIC\nSource: AMFI\nSource: NSE Market Pulse\nSource: Jefferies\nIndia - Consumption\n$~25 Bn \nin FY25",
            "86\n…as well as the rise of the experience economy…\nSource: BookMyShow numbers via Yourstory, MediaBrief, CNBCTV18, Fortune India\nTweets by Chandra Srikanth, Anup Pandey, Akshita Iyer, Spadika Jayaraj\nBookMyShow - Events and attendance\nA frenzy for getting tickets for the recent Coldplay concerts\nGrowth in number of events\nGrowth in event attendance, (in millions)\nIndia - Consumption",
            "87\nSource: UBS, RBI Bulletins\nIncreased hotel consumption despite rising inflation\nAverage hotel booking transaction \nsize on MakeMyTrip (in USD)\n“When Oberoi Udaivilas opened two decades ago in Udaipur, eight per cent of \nthe occupants were Indians, the rest foreigners. By 2018, the Indian occupancy \nat the luxury hotel was at 52%. “ - Atlas of Affluence\nNumber of hotel booking \nmade on MakeMyTrip (in millions)\n% Share of Travel and Education in Total \nOutward Remittances under LRS\nTotal remittance increased from $1.3 Bn in FY15 to $31.7 Bn in FY24. \nThis means $17 Bn is Travel-related remittances in FY24 (at 53.6% of \ntotal; incidentally this was $~7 Bn in FY20). This includes all credit \ncard spends while abroad as well as travel agents booking holiday \npackages etc., which are classified by banks under LRS. \nIndia1’s travel mania is reflected in the sharp \nrise in travel remittances under LRS!\nIndia - Consumption\n…a key aspect of which is travel…",
            "88\n…and the creation of homegrown premium / luxury brands in \nseveral categories…\nLeveraging traditional strengths in \ntextiles and ayurveda, reinterpreting \nit for contemporary India.\nLeveraging India1’s desire for world \nclass products with an Indian soul and \naesthetic sensibility.\nLeveraging India1 as the 51st state of \nthe US in tastes and aspirations, \nand using it as a springboard \nto launch globally.\nIndia - Consumption",
            "89\n…and increasingly how our cities are evolving \nSource: Tweet\nIndia1 prefers gated communities to the ‘Civil Lines’ / Cantonments of their parents \nIndia - Consumption",
            "90\nGated Communities are concentrations of affluence \nSource: MyGate, Redseer\n40% households in Top 50 cities are gated \ncommunities. The consumption and spend \npower of these households contributes to \n>50% of Consumption Expenditure\nAccording to MyGate, 26% of spending by \nthese households is through online \nchannels.\nAll data in the charts below courtesy \nGated communities punch above their \nweight in Consumption expenditure\nHouseholds in gated communities are savvy \nonline shoppers\nPer capita household spending of gated \ncommunity households is on a steady rise\nIndia - Consumption",
            "91\nIndia1 is a ‘high income’ country within a country\nIndia1 in population size would be the 10th most \npopulous country\nBasis per capita income, India1 would be 63rd in the \nworld, well ahead of India (ranked 140th)\nSource: World Bank \nIndia1 is spread across urban and rural areas, not concentrated in specific regions (though there is less in East India). Given the dispersion, and the overall size of 10% of population, it \nhas less direct political influence. Its influence is manifested in its consumption behaviour and social media voice, as well as how it helps India project soft power abroad. In the coming \nyears, it will get richer, and the economic gap between it and India will widen. This will bring distinct challenges that we as a society will need to work together to overcome.\nIndia1 will be an advanced economy well before India overall becomes a developed country\nWith ~140mn people India1 \nwould be 10th globally in \npopulation size\nWith US$ 15K per capita \nincome, India1 would pass the \nWorld Bank’s $14K threshold \nfor “high income” status.\nIndia - Consumption",
            "Source: Twitter / Ritesh Banglani & Anmol Maini\n92",
            "Section II: Indus Valley",
            "94\nSource: Twitter / Ashish Sinha\nIndus Valley in one tweet\nUber was forced to make a change to its \ntraditional revenue model (commission on \nthe fare paid) for (3-wheeler) autos in \nIndia. \nNamma Yatri, an Indian startup leveraged \nthe open source Beckn protocol (part of \nIndia Stack / Digital Public Infra ) to build \na mobility solution where the revenue \nmodel was to charge a daily (or monthly) \nfee for drivers for the app, and not take a \nslice of the fare paid. The success of this \nmodel has forced all the other mobility \nplayers (Rapido, Ola, and now Uber to \nfollow suit). \nThe tweet shows how first-world revenue \nmodels have to adapt to the unique \nneeds of the Indian market, the rise of \nDPI, and DPI-native revenue models.",
            "Venture funding trends, and a deep dive, followed by a \nlook at India’s unicorns, and the venture debt market.\n Indus Valley\nIndus Valley - Funding Trends\nA deep dive into the Indian venture \nmarket, including contrasts with China \nand USA, along with stage-wise funding \nanalysis. We then do an analysis of \nunicorns, and attempt a count of the true \nnumber of unicorns. We wrap this with a \nloop at startups flipping back to India, to \nlist here, and finally, track the rise of \nventure debt.\nIndus Valley - Funding Trends \nIPO Boom Pg 111\nSector Deep Dives Pg 120\nIndus Valley Playbooks Pg 157\n95",
            "96\nSource: Dealroom\nVenture Capital investments in startups over the last 5 years (in USD billion)\nIndus Valley - Funding Trends\nState of global venture market - US has bounced back strongly, \nIndia seeing signs of revival",
            "Remember, this was pre-DeepSeek China! \n97\nWhile US saw large rounds thanks to AI, China was in a funk\nSource: Dealroom, Bloomberg, Financial Times\nLarge rounds back in the US, thanks to AI!\nWhile US share of global funding went up, India and \nChina remained muted\nChina’s venture funding trended downward (this was pre-DeepSeek!)\nAI funding alone was a \nrecord $97 Billion of this - \nmaking up to 80% of the \ntotal funds raised in large \nrounds.\n (Bloomberg)\nIndus Valley Funding\nIndus Valley - Funding Trends",
            "98\nIndia's VC market following 2023 trendlines broadly\nSlight uptick in funding but nowhere near 2021, 2022 levels; in large part due to absence of late stage capital.\nAverage number of rounds : 2,311\n3,435\n3,315\n2,267\nSource: Tracxn\nTracxn updates the database continuously and hence the 2024 number may change in the future; still this snapshot should give you a directional sense of funding trends. Pls do note that each database may \npresent data differently depending on how they categorised certain transactions. You may see numbers differ from chart to chart depending on the database; that said the broad trendline should hold!\n1,721\nIndia Venture Capital Investments (in USD billion)\nIndus Valley Funding\nIndus Valley - Funding Trends",
            "99\nA stage-wise analysis of India's VC Market \nSource: Tracxn\n2024 mirrors 2023 patterns: Seed saw a small drop, Early and Late stages show modest gains but far below peak levels\nHow Seed, Early, and Late Stage financing stacks up (in USD billion)\nIndus Valley Funding\nIndus Valley - Funding Trends",
            "100\nSeed funding continues on trendlines - fewer rounds, larger checks\nSource: Tracxn\nSeed funding split by stages per year \nThe average seed round is $1 mn (~3x of what it was in 2017). The number of \ncompanies able to raise a seed round have been decreasing steadily since 2021. In \n2021, about 2,513 raised a seed round while in 2024 only 1,078 raised. The biggest \ndrop was in the <$1 mn segment (37% down). $1-3m saw a 22% drop.\nThe ‘mango seed’ is here to stay \nFrom <10% to 50% of total funding (USD million)\nLarger seed rounds or ‘mango seeds’ (>$3M) now make up 50% of funding, while <$1M rounds drop to one third of 2017 \nlevels. This is led by second time founders, and elite operators, raising larger formation cheques.\n<$1mn seed rounds have decreased by a third from 2017 \nIndus Valley Funding\nIndus Valley - Funding Trends",
            "Deeptech / Life Sciences\nConsumer\nStudent-focussed\nAll Sector\nSaas / DevTools\nThe Early-Stage funding gap is fueling the rise of MicroVCs\nBetween angels and choosy seed funds, a new stage (pre-seed), and backer (the MicroVC), is emerging\nRise of Specialised MicroVCs\nMicroVCs have created their niche in early Seed stage\n What has led to the rise of MicroVCs?\nAs Seed / Multistage funds get choosy and prefer to focus on elite \nfounders, a gap is opening up in funding for first-time founders, which \nis being filled by MicroVCs.\nHow are MicroVCs different?\n➔\nHave a special focus or highly evolved thesis in a particular \ndomain\n➔\nThere are over 100 MicroVCs (many founded recently) \ntypically investing $100k-$500k at seed / pre-seed stage. \nThese funds invest at valuations of $1M-$8M, taking 3-8% \nstakes in startups, sometimes more.\nSource: Blume analysis;\n101\nIndus Valley Funding\nIndus Valley - Funding Trends",
            "102\nSeries A/B funding: Stable check sizes, fewer rounds, longer \nintervals\nSource: Tracxn\nStartups raising Series A / B has reset to 2017-18 \nlevels, showing a clear reversal of the 2021-22 surge\nEarly stage funding across A and B has halved from 21’ & 22’, but the average round size has stayed the same. Effectively \nthe number of investments, and the number of companies graduating to A & B stages have halved.\nTime to fundraise has increased, especially for \nSeries B rounds, which now take 9 months \ncompared to 2017, while Series A rounds take 4 \nmonths longer \nSlight uptick in funding but nowhere near \n2021 / ‘22\nTime between rounds is steadily rising\nRound sizes stay flat but the number of \ncompanies raising series A or B reduced \nby 30% (vs 2022)\nIndus Valley Funding\nIndus Valley - Funding Trends",
            "Startups backed by seed funds taking longer to raise follow-on rounds as compared to ones backed by multistage funds\n103\nTime between rounds: Seed vs multistage fund-backed startups \nSource: Tracxn\nSeed to Series A\nSeries A to Series B\nIndus Valley Funding\nIndus Valley - Funding Trends",
            "$50m+ rounds remain subdued while overall late stage contribution drops to 59% of total funding\n104\nLate Stage remains lacklustre\nSource: Tracxn\nA thriving venture market like US has about 70/75% late stage funding as more \ncompanies keep growing and require more growth capital.\nMore than half of these \nrounds have been from \ncompanies which raised a \nmuch larger round before.\n$50m+ rounds are still down from their ‘21 highs\nLate Stage rounds as % of total funding is close to where it \nwas in 2016 \nIndus Valley Funding\nIndus Valley - Funding Trends",
            "India added 6 unicorns is 2024, an improvement from last year’s 2 \n105\nIndia is the 3rd largest unicorn factory…\nSource: Bain, Tracxn\nSlim pickings on the Unicorn-creation front, after the go-go \nyears of 2020-22 \nIndia is the third largest in total unicorn count\nIndus Valley Funding\nIndus Valley - Funding Trends",
            "Based on our analysis only 91 out of our 117 Unicorns are truly worth >$1bn\n106\nBut do we really have 117 Unicorns?\nSource: Blume Analysis, Tracxn\nGoing Steady\n(54)\nValued Under $1Bn\n(20)\nGoing Public\n(19)\nPublicly Listed\n(14)\nAcquired (7)\nBootstrapped or Founder Owned\nPublicly Listed\nGoing Public\nValued under $1Bn\nGoing Steady\nAcquired\nGreater than\n$1Bn\nLess than\n$1Bn\nLess than\n$1Bn\nFounder Owned (3)\nGreater than\n$1Bn\nIndus Valley Funding\nIndus Valley - Funding Trends",
            "107\nSource: Indian Express, Outlook Business, Khaitan & Co\nRegulatory changes and strong public markets drive foreign-incorporated startups to return to India\nPhonepe tax bill would make it the 10th \nhighest tax paying company in India in \nFY23\nCompany\nTax Paid\nPhonepe\n$1 Bn\nGroww\n$160 Mn\nRazorpay\n$200 Mn\nZepto\nUndisclosed\nEven more are in the process of reshoring\nIndian companies want to list in the \nfriendlier Indian public market\nSimpler tax norms and policies for them \nto operate.\nIndustry regulations which favour indian \nregistered company (especially fintech \nand ecommerce companies)\nPaying huge tax bills in order to do so\nBut why?\nIndus Valley Funding\nAn emerging trend with late stage startups has been the reverse \nflip back to India \nIndus Valley - Funding Trends",
            "108\nWhy did they register abroad in the first place?\nSource: Twitter / Anu Hariharan, Linkedin / Rehan Yar Khan \nDifficulty in raising capital domestically\nPlanned to list on the US public market\nIndus Valley Funding\nIndus Valley - Funding Trends",
            "Longer fundraising cycles and tighter equity markets are making startups tap into venture debt\n109\nVenture Debt becomes more common as equity funding tightens up\nSource: Stride Ventures\nImplication of raising Venture Debt:\n➔\nHigher Liquidation Preference: Venture debt typically comes with priority claims on company assets and cash flows, over equity holders\n➔\nEquity-Dependent Credit Lines: Available venture debt limits are often tied to equity reserves, creating potential downward spirals if equity positions \nweaken\n➔\nRisk of Negative Cycle: As equity funding becomes harder to secure, venture debt capacity may shrink exactly when companies need it most.\nVenture Debt has picked up sharply over the last 7 years\nVenture Debt has grown from <1% of venture funding to 11%\nIndus Valley Funding\nIndus Valley - Funding Trends",
            "Westbridge investment in WACA (Westbridge Anand Chess Academy) has put Indian chess on the world map. WACA \n‘facilitates mentorship to emerging and established chess players in India’ with the hope of creating more world champions. \n110\nSometimes the best investment is in people, not the company\nSource: linkedin/ Sandeep Singhal, Youtube/ Chessbase India\n Behind Indian Chess champions is Westbridge’s WACA \ninitiative\nWestbridge partnered with Vishy Anand to create initiative \nIndus Valley Funding\nIndus Valley - Funding Trends",
            "A deep dive into India's booming IPO market, as well as \nthe SME IPO’s rise, including what it implies for \nfounders.\n Indus Valley\nIPO Boom \nIndus Valley - Funding Trends Pg 95\nIPO Boom \nIndus Valley Playbooks Pg 157\nSector Deep Dives Pg 120\nA deep-dive into India’s record-breaking \nIPO market, looking at the performance \nof IPOs, exploring how barriers to list are \ncoming down, as well as the rise of the \nSME IPO Market.\n111",
            "(India)\n(Japan)\n(Hong Kong)\n(Shanghai)\nBoth the number of IPOs and issue sizes reach record levels\n112\n2024: A record-breaking year for Indian IPOs\nSource: NSE Market Pulse\nHyundai Motor India was the largest-ever IPO in \nIndia, raising ₹27,870 crore (US$~3bn). It was also \nthe second-largest IPO globally in 2024.\n(India)\n(US)\n(US) (Hong Kong)\n(Shanghai)\nOf the 268 IPOs on NSE in India, 90 of them were \nMainboard listing vs 178 SME (NSE Emerge) IPOs\nIndus Valley - IPO Boom\nIndia saw its best year in equity \nfunding raised via IPOs\n1\n…as well as the highest capital \nraised via IPOs across the world\nIndia led in IPO activity globally,\nwith a 23% share of total listings…\n2\n3",
            "Companies are going public earlier; with 42% lower revenue and 37% lower market cap compared to 2018 levels\n113\nIndian public markets: Becoming more accessible, earlier\nSource: Blume - Insights from a decade of Indian Mainboard IPOs | Part 2\nMedian revenue at listing has decreased 42% since 2018\nMedian market cap at listing has reduced 37% since 2018\nIndus Valley - IPO Boom",
            "114\nMarket cap data as on 17th January 2025 via NSE. The number of venture funded IPOs here includes post-IPO VC funding. The number includes 3 VC funded companies listed \nabroad - Freshworks, ReNew, and MakeMyTrip. The IPO list was taken from Tracxn. This number includes a total of 14 VC funded SME IPOs.\nPre 2011\n2021\n2025\n50\n37\n80\nVC-funded companies that have gone IPO, pre and post ‘21\nThere has been a history of VC backed IPOs!\nIndia has a long history of venture-funded IPOs\nOver 160 venture-backed companies have gone public thus far, with post-2021 IPOs raising more than double the capital of \nall previous listings\nIndus Valley - IPO Boom",
            "115\nVenture funded companies that IPO’d 2021 to 2024: A status check\nSource: Nuvama Alt & Quant Research, all data as of 22nd January 2025\nSmaller IPOs (<$1 Bn) dominate with 2/3rd of listings; they have also performed relatively better while larger listings show \nmixed performance; Swiggy signals renewed appetite for big tech offerings\n2/3rds of IPOs in last four years have \nbeen of companies with <$1 Bn Mcap\n1\nVenture-funded co market caps \ndropped ~5% (since IPO day), but \n<$1Bn market cap companies saw a \ngain of 25%\nLarge listings made a comeback in \n2024 thanks to Swiggy\n2\n3\nIndus Valley - IPO Boom",
            "116\nSource: Live Mint, Money Control\nSME IPO market outperforms Sensex IPO index by 5x, driving record issues, raise and retail participation\nThe number of issues have grown from 68 \nin 2016 to 236 (includes both BSE SME and \nNSE Emerge) in 2024\nSME IPOs saw their biggest year in \nissues and raises \n1\nDriving a lot of retail demand\nSME IPO Index returned 5x over the \nBSE IPO Index\n2\n3\nIndus Valley - IPO Boom\nSME IPO is a potential exit route companies for well-performing \ncompanies that don’t get late stage venture love!",
            "+₹3 Bn \nMarket Cap\n1 Year\n+₹40 Bn\nMarket Cap\n6 Years\nWith 1 in 3 SME IPO-listed companies graduating to the Mainboard, SME platform demonstrates strong outcomes, putting a \nvery strong case forward for more VC-backed companies to go this route.\n117\nSME IPOs: An untapped opportunity for VC-backed companies\nNote: Market Cap calculations for the 14 Venture Funded SME IPOs in India do not include 3 that have migrated to the mainboard (E2E, AVG, Deccan Healthcare)\nSource: Blume - Learnings from Indian SME IPOs, BSE SME Board website, NSE Emerge website, Tracxn \n14 VC funded companies have IPO’d on the SME board with a total mcap of ~ ₹50 Bn; \nabout 1.5% of total mcap of the SME board\n6 Years\n+₹3 Bn \nMarket Cap\n<1 Year\n+₹6 Bn\n Market Cap\nBlume was a seed \ninvestor and the \nonly institutional \ninvestor at IPO in \nboth E2E and \nInfollion!\nHow has the SME IPO market evolved\n➔\nSince 2012, the median SME IPO market cap has jumped 4.5x to ~₹1 Bn \n(2024) whereas median revenue at IPO grew 3x to ~₹700 Mn (2024)\n➔\nThe median offer size has grown 3x from ~₹80 Mn a decade back to ~\n₹250 Mn now\n➔\nOf the total capital raised, 90% has been through fresh offer / primary \ncapital \nOf 1,053 companies that listed on SME board, 31% have \nmigrated to Mainboard\nVC-funded SME IPOs have impressed post listing!\nIndus Valley - IPO Boom",
            "118\nFrom SME bourse to AI leader: E2E Networks growth story shows \ntech and VC potential on the SME boards\nSource: Company Documents, Financial Express, Business Standard, Upstox, \nMcap as of 13th Feb 2025\nE2E’s market cap is up 65x from the time of listing.\n➔\nE2E is a hyperscaling cloud provider also enabling access to \nNvidia GPUs, focused on the Indian market.\n➔\nIt was listed on the NSE Emerge (SME) board in May 2018 \nand migrated to the mainboard in April 2022. Blume was the \nonly institutional investor on the cap table.\n➔\nIn the last 2-3 years, it has been able to capitalise on the AI \ntrend by having exclusive access to the latest hardware.\nAbout E2E Network\nIndus Valley - IPO Boom",
            "119\nGuideline for founders mulling over an SME IPO\nSource: Blume - Learnings from Indian SME IPOs, NSE, Chittorgarh\nWhat is the eligibility criteria?\nWhat needs to be kept in mind for the SME IPO?\nA long-Term lens\nPublic markets are a marathon, not a sprint; you need to have a \ndecade-long time horizon when you think about going public.\nPredictability\nWhat public markets expect is predictability; they don't want any \nsurprises, so your business has to have stability and you should \nhave clear revenue foresight.\nWhy wait for a billion-Dollar IPO?\n You can continue to compound in public markets - if you grow \n20-25%, public markets would value you more than private markets.\nClarity on ‘use of funds’ \nIn private markets, it's fine if the capital you raise isn't used exactly \nas stated, but in public markets, you need to be very precise about \nhow the capital will be used since this will be audited\nCommon criteria for NSE Emerge & BSE SME\n➔\n3+ years existence\n➔\nMax post-issue paid-up capital: ₹25 Mn\n➔\nPositive EBITDA: 2 out of last 3 FYs\nExchange-specific criteria\n➔\nNSE Emerge: Requires positive net worth & FCF to equity \n➔\nBSE SME: Minimum net worth ₹10 Mn & net tangible \nassets ₹30 Mn\nIndus Valley - IPO Boom",
            "Indus Valley\nQuick Commerce\nIndus Valley - Funding Trends Pg 95\nIPO Boom Pg 111\n➔\nQuick Commerce: Why it works in India, the \nimplications of its rise, and is there irrational \nexuberance re Quick Commerce? \n➔\nAI: Is India getting a foundational model soon?\nSector Deep Dives \nIndus Valley Playbooks Pg 157\nA detailed analysis of the Quick \nCommerce market, its growth, why it \nworks in India, what the vectors of its \ngrowth are, the implications of its rise, \nand whether there is ‘irrational \nexuberance’ about its prospects?\n120",
            "121\nThe ‘Quick India Movement’\nSource: Twitter / Harsh Punjabi, and Vaibhav Domkundwar\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "With 24x growth in order value since FY22 and user base doubling YoY, Quick Commerce is redefining India's retail landscape\n122\nQuick Commerce is India’s fastest growing industry segment ever!\n* MTU numbers stated here are not unique; a user using multiple platforms will be double counted.\nSource: CLSA, JP Morgan, Business Standard | \nOthers (3%)\nBlinkit\n44%\nInstamart\n23%\nZepto\n30%\nFY25 food delivery MTUs for Swiggy and Zomato \n(both of whom who have been operating over a \ndecade) together are expected to be 40.8Mn. Quick \nCommerce MTUs are two-thirds of this in three years.\n24x rise in Gross Order Value in 3 years!\nRapid rise in MTUs or monthly \ntransacting users)*\nBlinkit, Zepto, Instamart dominate this \nspace, but competition is brewing.\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "Quick commerce players are aggressively expanding dark store network and geographical presence, with Blinkit leading in \nboth metrics\n123\n“Zomato is India’s Capex Story”* \n* Tongue in cheek remark by Aditya Soman, CLSA, given Blinkit (Zomato’s subsidiary)’s aggressive dark store roll out\nSource: CLSA, JP Morgan, Money Control\nExpansion beyond metros: Recent launches in Tier 2 cities including \nBathinda, Haridwar, Jammu, Kochi, Rajkot, and Bhopal\nDark store growth has been explosive, with nearly 2,000 stores \nadded this financial year…\n…and expanding into more and more cities.\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "124\nThanks to scale efficiencies, unit economics has rapidly \nimproved!\nSource: Zepto investor presentation, BofA\nA 2022 store took 23 months to turn EBITDA-positive with 4cr \nspent on capex, while a 2024 store turned EBITDA-positive \nin 8 months with 1.5cr in capex\nZepto is hitting store breakeven faster per the founder\nBlinkit: Contribution Margins turn positive despite rapid \nexpansion and competitive pressures\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "Other Variable \nCosts\n₹61\nDelivery Costs\n₹35\nDiscounts ₹5\nKey Blinkit metrics\n125\nContribution margin is built on two key pillars: AOV and take rate\nSource: BofA\nMetrics\nFY25E\nGOV \n₹27,867 Cr\n% yoy\n123.50%\nAverage MTUs\n9.6 Mn\nAOV\n₹674\nOrders\n413 Mn\nImplied Take Rates\n19.50%\nAdjusted Revenue\n₹5,420 Cr\nContribution Margin \n(as % of GOV)\n4.00%\nAdjusted EBITDA\n(₹33 Cr)\n% margin on GOV\n(0.10%)\nIn contrast, Swiggy was AOV of 515 and \n15.5% take rate (Rs.80) which makes it \ndifficult for them to cover delivery & other \nvariable costs and hence lose money. \nUltimately variable costs are also a \nfunction of scale (with increased orders, \nper unit costs drop!) \nBreakup of Blinkit \nAOV ₹674\nCommission & \nAd Revenue\n₹120\nUser Fee ₹11\nSources for \n₹131 revenue\nCost Breakup of \n₹131\nUnit economics of a single Blinkit order\nBlinkit Revenue \n19.5% (₹131)\nContribution \nProfit ₹31\n+\n=\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "126\nSource: Twitter / Manish Singh, Motilal Oswal\nIndia has only 6% modern retail share vs China at \n32%, and US/UK ~80% per this tweet\nWhy?\nWith lack of cars and small houses (lesser storage) - people prefer to shop \nlocally as they cannot go long distance and also not stock up on items\nIndia has low car ownership\nHouses are smaller than in other nations\nIndia seems to be leapfrogging Modern Retail and going directly to quick commerce\nQuick Commerce works because India is a poor market for \nModern Retail\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "Combination of low labour cost along with high density cities make quick commerce unit economics work for India\n127\nWhy Quick Commerce works in India\nTop Indian Cities counted include Delhi, Mumbai, Kolkata, Bengaluru, Hyderabad. \nGlobal cities counted include Tokyo ,São Paulo, New York City, Los Angeles, Paris\nSource: CLSA, Goldman Sachs | *\n“One reason the quick commerce model has had a greater impact in India is the lower labour cost as a proportion to cart size. Our sample suggests that the minimum \nwage-to-cart size ratio is 10-12% in India compared with 35-40% in China and 40-50% on average in Western countries.” - CLSA\nLow labour cost\n1\nHigh population density*\n India has amongst the lowest rider cost \nto Gross Order Value \n2\n3\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "128\nQuick Commerce - Faster, cheaper, and a wider selection\nSource: Twitter / @Sajcasm_, CLSA, Datum \nInstant gratification\n1\nRapidly expanding SKU count\nCheaper, thanks to discounts\n2\n3\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "129\nQuick Commerce is moving beyond grocery to become the new \n‘everything store’\nSource: CLSA, The Arc, Twitter / Madhav Chanchani\nMost stores have ~10k SKUs with a select few \nstores with 25k+ SKUs\nBlinkit, in particular, has been \naggressively expanding SKU count \n1\nSwiggy is behind the curve, but is also \nseeing non-food categories grow\nNon-food categories account for \n40% of Blinkit’s GOV\n2\n3\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "Returns and refunds, and the post-purchase experience matters too!\n130\nSource: LinkedIn / Aadit Palicha\nAs SKU counts expand and QCommerce (QCom) goes beyond \ngrocery, QCom operators rethink Qcom beyond just delivery\n“It is now time to take the customer \nexperience and growth to the next \nlevel by launching 10-minute returns \nand exchanges.”\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "131\nTo drive margin expansion, Zepto and Instamart have introduced \nprivate labels\nSource: CLSA, Twitter / Rahul Mathur\nZepto’s private label meat brand Relish has seen great traction thanks to its \ndistribution muscle \nSwiggy too has started selling its private \nlabel brands on Instamart\nSupreme Harvest\nTruly Good Food\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "These 10-min food delivery services mostly leverage their existing store infra\n132\n…and higher margin prepared food products!\nSource: LinkedIn / Aadit Palicha, Zepto investor presentation\nThe top 3 quick commerce players have all forayed into in-house \nfood delivery services \nZepto cafe has gone from 30K to 75K orders/day in just two \nmonths\nOperating via cloud kitchens situated within dark stores allows them to \nincrease their Average Order Value and margins while utilizing their \nexisting infrastructure and avoiding commission payments to \nintermediaries.\nIn Nov’24 Zepto Cafe was present in 15% of its dark stores, whereas \nnow it is available in more than 50% of dark stores.\nAadit Palicha, \nCEO at Zepto, \nsays that Cafe’s \nrun rate is at 10% \nof Domino’s last \nquarter revenue.\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "133\nRevenue from ads become a key growth lever for QCom players\nSource: LinkedIn / Aadit Palicha, Goldman Sachs\nFrom BofA : “We estimate ad revenues of QC platforms to be around \n3-3.5% (of GMV). We see this improving to 5-5.5% in coming years for \nselect platforms as they leverage data analytics to extract more from brands \nby adding value. This is a ~90% EBITDA margin business.\"\nQuick commerce ad revenues are growing fast…\n…and are contributing meaningfully to the bottom-line\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "134\n‘Quick’ expands to services and verticals too!\nQuick Commerce for Home Services\nQuick Commerce for Fashion\nQuick Commerce for Food Delivery\nSlikk\n60-Min Fashion delivery\nSnabbit\nHouse help in minutes\nSwish \n10-Min Food delivery\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "As Quick Commerce’s success inspires larger horizontal and vertical ecommerce players to start their experiments, we are likely to see \na speeding up of delivery times in India across most types of deliveries. We will be a Quickish Commerce country.\n135\nFrom Quick Commerce to Quickish Commerce\nSource: Twitter / Rajesh Sawhney, Twitter / Manish Singh, Economic Times\nFlipkart has entered Quick Commerce\nAmazon has plans to follow\n2\nOther players are taking notice too\n3\n1\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "In just three years, Quick commerce has started contributing 30-60% of ecommerce sales for major FMCG players, driving \nnew packaging, distribution strategies.\n136\nFMCG Brands love Quick Commerce\nSource: Datum, Bernstein, Business Standard\nQCom is becoming the fastest growing channel for FMCG \nbrands…\n…influencing them to rethink packaging and pricing for the \nSKUs sold in Quick Commerce channels \n10% of all ice creams sold \nby HUL are sold on quick \ncommerce channels.\nDabur stated that quick \ncommerce makes up \n>30% of its overall \nbeverage sales.\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "137\nIn the long run, Quick Commerce may be more frenemy than \nfriend to FMCG players\nSource: Twitter / Arindam Paul\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "Quick commerce eliminates traditional distribution moats, creating a level playing field between D2C and FMCG brands\n138\nQuick Commerce levels the playing field for D2C\nSource: Twitter / Ganesh Sonawane, India Today, Salty\nShare of QCom revenue as a % \nof Marketplace revenue rose \nfrom from ~30 to ~90% \nQCom is the fastest growing channel \nfor D2C brands today…\n1\n…and quickly catching up to online \nmarketplaces.\n…getting these brands access to \ncustomers they never had before…\n2\n3\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "139\nThe urban consumer is shifting their buying behaviour away from \nKirana stores\nSource: Datum Intell, Mint, Captable\n3/4ths of survey respondents felt that Quick \nCommerce poses a long-term threat to the \nviability of Kirana stores\nFor one Bengaluru-based engineer, his response to \na recent craving for a soft drink made him realise \njust how much quick commerce had reshaped his \nbehaviour. “I randomly order some juice because I \nhave access,” he says. “Earlier, I used to open the \nfridge. Now, I open Instamart, which is like an \nevolved version of checking the fridge.”\nVisible impact on Kirana stores\n1\nKirana owners are clearly worried\nUrban shoppers prefer Quick \nCommerce\n2\n3\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "140\nCase Study: Kirana Store owner in Bangalore facing both demand \nand supply side impact\nSource: Blume Research\nDrop in revenue, even with rising prices\nSupply is equally impacted\nDelivery orders have practically vanished\n1\n2\n3\nTrade promotions by FMCG players are \nabsent. \nPreviously, retailers could earn major \nincentives like washing machines for \nmeeting targets - these volume-based \nrewards are now rare.\nMargins on branded products have \ndropped significantly. \nFor instance, biscuit category margins \nhave fallen from 22% to 7-8%, severely \nimpacting retailer profits.\nWeakened demand has forced retailers \nto abandon bulk purchasing in favor of \nsmaller, frequent orders. \nThis shift further reduces margins as they \nlose bulk buying benefits.\nKirana stores don’t have enough options (SKUs) for brand \nconscious customers. And with free delivery as well as the \ndiscounts that QCom offers, online works out cheaper.\nInsights are from an interview with a \nshop owner who has been in \nbusiness for 30 years, currently \noperating in a middle-class \nneighborhood of urban Bangalore.\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "141\nQuick Commerce operators have power, and they are not afraid to \nwield it too\nSource: The Ken, Twitter / Prem Pradeep\nBrands find it hard to list on Quick Commerce platforms\nDark patterns have started to emerge on the apps\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "A slew of analyst reports have projected heady numbers for Quick Commerce; for instance an equity research report from a \nleading brokerage house projects the Industry to hit $89b in FY31 (FY25E of $7.1bn). How realistic is this? \n142\nIrrational exuberance about Quick Commerce?\nOrders per month per \nuser\nGross annual order \nvalue\nMonthly transacting \nusers (MTUs)\nNumber of dark stores\nTotal annual orders\nLet us examine two of these above estimates: Monthly transacting users (MTUs), as well as Dark Stores, closely.\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "Growth projections to 128 million monthly transacting users (MTUs) look ambitious when India1 itself is not widening fast\n143\nHow realistic is the Monthly Transacting User number?\nSource: Leading brokerage house, Twitter / Kunal Shah\nMuch of India’s consumption is led by India1, and within that there is a \nsubset we call India1 Alpha, which is about 8-10 million households \nlarge who are true super consumers. This class is growing slowly, and \nas we saw in the Consumption section, has deepened than widened. \nThe growth in MTUs will thus attract marginal users not power users, \nand thus orders nearly doubling will be challenging.\nHow Quick Commerce is projected to grow\nThis misses out on the true upper bound of the Indian \nconsuming class\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "July 2021 estimates by Jefferies projected 32.6M users for Zomato by FY25, but current trajectory points to 20.6M users in \nFY25 - a reminder about user growth forecasts in consumer internet consistently fall short\n144\nWe have been here before\nSource: Jefferies, Motilal Oswal\nJefferies estimate of Zomato’s Monthly Transacting Users \n(MTUs) in Jul’21\nIn reality, Zomato has not come anywhere near those \nprojections. It is at 2/3rd of those numbers.\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "145\nHow realistic is the Dark Stores number?\nSource: Leading brokerage house, Bernstein, HDFC Securities\nThe dark store number is projected to \ngrow from 3400 to 11500 over 6 years\n19300\nTotal \nPincodes\n965\nBut does India have so much depth?\nA proxy for affluence is presence of 5+ organised \nretail stores, which per a Bernstein study is seen in \nonly 5% of India’s pincodes. These pincodes \nserves 11% of population.\nThe challenge is that there are not many of these in \na country with per capita income below $3k.\nPresuming each of Blinkit, Instamart, Zepto has 2 \nDark Stores per pincode, and rounding off to 10 \nDark Stores per pincode, we are still looking at \n9,650 Dark Stores (not 11,500). \nPer a HDFC Securities study, \nthere are only 63 districts in \nIndia (<10% of 780 or so \ndistricts) with per capita income \nof ₹150k+ and density > 500 \npeople per sq km. \nThese have ~90m households \nin all (across all income levels) \nand per HDFC Securities, \nthese can support at max \n~7,800 dark stores, not 11,500!\nWhen existing dark stores have begun stagnating\nAdded to that is that Orders per Dark Store have \nstabilised. Given this, and the diminishing returns \nof expanding Dark Stores beyond certain areas, \nthe aggressive projections of total orders seem \na tad unrealistic. (80% of Blinkit’s sales come \nfrom the top 8 cities per Albinder (3QFY25 \nanalyst call transcript).\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "146\nTL;DR\nSource: Blume Analysis\n●\nQuick Commerce is not immune to the gravitational pull of low TAM (given India’s low \nper capita income) and the power law of a tiny percentage of superconsumers\n●\nLike rideshare, food delivery, and even ecommerce, we will see MTU growth tapering \n- it is unlikely that Quick Commerce is immune to this.\n●\nECommerce players have already started reacting, and while it is not guaranteed they \nwill be able to counter Quick Commerce players, the increased competition will have \nsome impact on the Quick Commerce industry profit pool.\n●\nIt is the case that we are moving to almost every ecommerce platform speeding up \ntheir delivery. India will become a Quickish Commerce country, especially because of \nthe superconsumers are in high density areas amenable to rapid delivery.\n●\nAs Quick Commerce expands, and the toll on Kiranas becomes more visible, we may \nsee more visible debates and measures to check Quick Commerce’s growth.\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "Source: Twitter / Soumya Gupta\n147\nIndus Valley - Sector Deep Dives / Quick Commerce",
            "➔\nQuick Commerce: Why it works in India, the \nimplications of its rise, and is there irrational \nexuberance re QCom? \n➔\nAI: Is India getting a foundational model \nsoon?\n Indus Valley\nWhy China, not India had a DeepSeek \nmoment, and whether the recent \nenthusiasm and initiatives could spur the \ncreation of a foundational model? \nAI: Is India getting a \nfoundational model \nsoon?\nIndus Valley - Funding Trends Pg 95\nIPO Boom Pg 111\nSector Deep Dives \nIndus Valley Playbooks Pg 157\n148",
            "149\nAn Indian company was present at the birth of OpenAI\nSource: Introducing OpenAI 2015\nInfosys was one of the founding donors of \nOpenAI, then structured as a non-profit.\nSubsequently due to Vishal Sikka’s exit, there was \nno link with OpenAI, and it missed the opportunity to \nbe an investor when OpenAI restructured itself and \nspun off a for-profit entity in 2019.\nThis was the entity that Microsoft, Khosla Ventures \ninvested.\n…\nIndus Valley - Sector Deep Dives / AI",
            "150\nBroad vibe till late 2024\nSource: Twitter / Chandra R Srikanth\nPre-DeepSeek default mode\nIndian-founded startups building in AI\nServices\nApplications\nMiddleware\nFoundation Models\nCloud Platforms\nComputer Hardware\nIndus Valley - Sector Deep Dives / AI",
            "151\nVibeshift!\nSource: Twitter via tweets from Financial Times, Aravind Srinivas, Paras Chopra and Sridhar Vembu\nIndus Valley - Sector Deep Dives / AI",
            "152\nWhy didn’t India do DeepSeek?\nSource: Twitter / Sadanand Dhume, Twitter / Anmol Maini\nThe forcing functions that created DeepSeek\n1\n2\n3\n…\nChina being the base for 1/8th of World’s top \nAI researchers (India has none)\nChina has been continuously investing in \nand improving in AI. The Australian Strategic \nPolicy Institute identified that China led in \njust three of 64 critical technologies in the \nyears from 2003 to 2007, but is the leading \ncountry in 57 of 64 technologies over the \npast five years from 2019 to 2023. \nConstraints breed creativity - the challenges \nin accessing GPUs led them to approaches \nand tech minimising GPU use\nCrackdown on the finance industry leading \nto the hedge fund High-Flyer deciding to \nredirect its attention towards AI tech, away \nfrom Finance. They also managed to access \ncapital (Govt support?) to undertake the \n$1.6b+ investment to develop the same \n($1.6b via Semi Analysis)\n4\nIndus Valley - Sector Deep Dives / AI",
            "153\nCan India build its own foundational model? We will find out soon!\nSource: Twitter / Vinod Khosla, Twitter / India IT Minister Ashwini Vaishnav, IndiaAI Website\nBlume Perspective: We do think we will have home grown foundational models emerging in the coming 12-18 months given the Government support, as well \nas the emergence of teams keen to build India’s first foundational model. There is too much momentum behind this, and enough confidence that it can be built \n(post DeepSeek) for it to not happen.\nDPI and ISRO, both examples of frugal innovation, and also examples of public-private partnerships, show a potential path forward for AI foundational models. \n‘AI Sovereignty’\n₹20bn ($240m) allocation in the Indian budget; access to 18k GPUs at 40% below \nmarket rates to spur India’s homegrown LLMs.\nIndus Valley - Sector Deep Dives / AI",
            "154\nThe success of Digital Public Infra and ISRO / Space Missions are two \ngreat examples of frugal innovation. Could AI models be the third? \nSource: UIDAI Accounts, UIDAI Annual Report ‘23, Hindu Business Line , Blume Indus Valley Report 2024\nThe UPI Story\nThe ISRO Story\nISRO is consistently cited as having pioneered the frugal approach to \nspace exploration, cheaper than Hollywood space movies even!\nWith just over $1b spend, India had onboarded a billion people to the \nAadhar identity initiative; resulting in annual savings of over a billion!\nYear\nAmount\n2009-10\n₹26.2 Cr\n2010-11\n₹268.4 Cr\n2011-12\n₹1,187.5 Cr\n2012-13\n₹1,338.7 Cr\n2013-14\n₹1,544.4 Cr\n2014-15\n₹1,615.3 Cr\n2015-16\n₹1680.4 Cr\n2016-17\n₹1132.8 Cr\nExpenditure on Aadhaar (in INR crore)\nIndus Valley - Sector Deep Dives / AI",
            "155\nIndia has the talent (even if our best talent is in the US) and now \nwe are getting the GPUs!\nSource: Twitter / GitHub CEO Thomas Dohmke, Savills India Research, Visual Capitalist, Cushman & Wakeﬁeld, Moneycontrol \nWe have the talent\nWe are getting the data centres\nWe can build cheaper than our peers\nIndus Valley - Sector Deep Dives / AI",
            "156\nMeanwhile there are impressive Consumer AI stories emerging \nfrom India as well!\nSource: Twitter / Sanket Shah, Twitter / Sumanth Raghavendra, Presentations AI blog\nVideo generation via prompts leveraging OpenAI\n“4 million MAUs creating 7 million videos a month” - OpenAI\nCreate presentations leveraging AI.\nHit 1 million users in <3 months and then hit $1 million \nrevenue in 12 months (by Jun’24), and founder writes has \ngrown ‘leaps and bounds’ since then to hit “5 million users, \n112 countries, millions in profits”\nIndus Valley - Sector Deep Dives / AI",
            "➔\nThe various India2 Playbooks.\n➔\nHow Indus Valley influenced Indian advertising.\n➔\nReturns, and how Indian startups are addressing \nit.\n➔\nMarketing framework for the Indian diaspora or \nIndia0.\n Indus Valley\nThe various India2 \nPlaybooks.\nHistoric playbooks contrasted with the \nEvolved and Emerging playbooks, \nfollowed by case studies of STAGE, \nKaleidofin, and Voice Club. Why voice, \nand microtransactions are two killer \nfeatures of the Emerging playbook.\nIndus Valley - Funding Trends Pg 95\nIPO Boom Pg 111\nSector Deep Dives Pg 120\nIndus Valley Playbooks \n157",
            "158\nIndus Valley - Playbooks / India2\nThe India2 playbook is evolving\nEmerging Playbook\nRethink the product around the fundamental \nneed to be solved (or job-to-be-done / JTBD)\nEvolved Playbook\nRe-engineer the product for Indian context \nand user behaviour, and margins(!) benefitting \nfrom Jio & UPI boost.\n2015 - 2020\n2020 Onwards\nHistoric OG Playbook\nLaunch a proven western product to suit Indian tastes and language preferences.\nConversations with \nthe opposite sex, \nnot dates.\nAstrological \ncounselling as \ntherapy sessions.\nDriver subs, and not \nuser charges as the \nrevenue model",
            "159\nEvolved Playbook: Re-engineer the product, and price it \naffordably, for India2\n₹20\n₹105\n₹75\n₹10\n₹1,788 \nannual\n₹399\nannual\n➔\nHere the product is re-engineered to suit India2’s language, taste, and price preferences. \n“Our users are happier to pay ₹10 every day for a month than pay ₹300 upfront” \n - Harsh Jain of Dream11 (during a conversation with Blume portfolio founders)\n➔\nThese products have superior unit economics thanks to being rethought from the grounds up for India2; as opposed to being \nworked downward from an India1 product.\nIndus Valley - Playbooks / India2",
            "160\nHow STAGE engineers ultra low-cost content\n➔\nStandardized set of story tropes and templates re-scripted for different languages, designed for low-cost shooting \n(e.g., mostly small sets scripted into storyline).\n➔\nWork with local content creators who don’t have access to other mainstream outlets willing to work for low costs.\n➔\nSignificant amount of pre-planning prior to shoot enabling quick turnarounds. \n=\n+\n+\nLower\nBudgets\nPer Film\nFaster \nShoots\nPer Film\nHighly\nRated\nSource: STAGE\nIndus Valley - Playbooks / India2",
            "161\nSource: Kaleidoﬁn\n ki score is an inclusive supervised AI/ML score developed by Kaleidofin, and used for Credit Decisioning and Risk \nManagement through all stages of the loan lifecycle. It is designed to reduce risk while significantly increasing access to traditionally underserved \ncustomers. It is built on datasets with dimensions including credit history, demographics, customer behaviour and alternate data. It is a powerful tool \nfor increasing access to appropriate credit beyond a credit bureau score.”\nCategory\nPAR 90 %\nki score accept + cb accept\n1.53%\nki score accept + cb reject\n2.51%\nki score reject + cb accept\n4.44%\nki score reject + cb reject \n7.68%\nPAR 90% measures borrowers defaulting on \nprincipal for over 90 days. Customers \napproved by ki score but rejected by credit \nbureaus have lower default rates compared to \nthose rejected by ki score but approved by \ncredit bureaus (cb hereafter).\nki score enabled 42.3% \nadditional loans beyond \ntraditional credit bureau \nratings\nki score has increased loans disbursed \nby 73%\nMonthly household income growth for \nnano-entrepreneurs shows \nki score’s impact\nPAR 90% data validates ki score's \naccuracy and inclusiveness \nFindings from a pool of ki scored nano-entrepreneurs \nshows the impact that access to timely credit may have \non customer resilience and well-being and the ki score \nacts as a key enabler here. “We see an average \nincrease of 26% in monthly HH income, 47% in \nannual business turnover, and 52% in monthly \nbusiness profits.”\nIndus Valley - Playbooks / India2\nHow Kaleidofin reengineered the credit rating product for India2 / India3",
            "162\nEmerging Playbook: Rethink the product for the specific job to be \ndone (JTBD) to fit India2’s context\nJTBD\nHelp me start dating\nJTBD \nI need easy, reliable \naccess to high quality \nmental healthcare.\nJTBD\nI don’t think there is anything wrong with \nme that I need ‘therapy’ (it is not socially \nacceptable in my context). Astrology counselling \nis a safe socially acceptable space for me to \nunburden myself and get some emotional relief.\nHere, founders understand the core Job-To-Be-Done (JTBD) in the context of the India2 user, including how prevalent cultural \npractices will support adoption, and use this to rethink the product itself. \nIndia 1\nIndia 2\nJTBD\nBefore I can think of dating, I need to \nspeak to members of the opposite sex. \nSo the product is to enable better \nconversations, via gamified formats.\nIndus Valley - Playbooks / India2",
            "163\nTwo other core features of the Emerging India2 Playbook:\nVoice and microtransactions\nMicrotransactions-led revenue model (prefilled wallet used for \ngifting) leading to whale + tail model\nFRND, AstroTalk, InstaAstro, Clarity all have 1:1 voice as a key revenue model. India2 (and many India1) users are willing to pay to talk to a stranger \n(expert or member of the opposite sex). The success of this model is attracting apps with a tangential interest in the space (e.g., Lokal) to explore \nthis revenue opportunity.\nHeavy on voice, with 1:1 conversations as a key revenue \ndriver\nwhich enables 1:1 counselling conversations, is an example of a company that exemplifies these features. \nSource: Voice Club\nIndus Valley - Playbooks / India2",
            "164\nSometimes it flips, and you have a India1 offering for what was a \nIndia2 product!\nSource: The Print\nIndus Valley - Playbooks / India2",
            "➔\nThe various India2 Playbooks.\n➔\nHow Indus Valley influenced Indian \nadvertising.\n➔\nReturns, and how Indian startups are addressing \nit.\n➔\nMarketing framework for the Indian diaspora or \nIndia0.\n Indus Valley\nHow Indus Valley \ninfluenced Indian \nadvertising.\nHow Indus Valley rethought the celebrity \nad to generate shock value, and how it \nhas shaped the Indian advertising \nmarket. We also look at the currency of \ntrust-building is diverging between India1 \nand India2 resulting in distinct \ncommunication templates.\nIndus Valley - Funding Trends Pg 95\nIPO Boom Pg 111\nSector Deep Dives Pg 120\nIndus Valley Playbooks \n165",
            "Humanising celebrities, making fun of them, was a new addition to the Indian ad oeuvre. Legacy brands historically kept the \ncelebrity on a near pedestal (with some exceptions).\n166\nIndus Valley - Playbooks / Indus Valley Marketing\nHow Indus Valley pioneered a new ad trope\n➔\nWhat is common to these ads is that their makers are ex-members of AIB (All India Bakchod) a comedy collective that melted down in the \n2018 #metoo wave. Key members include Tanmay Bhatt, Devaiah Bopanna, Vishal Dayama etc. [Tanmay + Devaiah also work together as \nMoonshot.]\n➔\nThey pitched legacy brands who hesitated to sign them given their lack of big agency experience; Startups however found a perfect match in \nthem especially given the comedians’ ability to create attention and shock value by depicting celebrities in a never before light, cutting \nthrough clutter.\nThis and the following slides in this section benefited significantly from inputs gathered during a conversation with Karthik Srinivasan, a leading ad / marketing guru (x.com/beastoftraal).\nI also enjoyed speaking with Arun Iyer (x.com/aruniyer), a seasoned adman who co-founded and is Partner at Spring Marketing Capital.",
            "167\nAs the ‘ComAdians’ went up market, Big Ad stepped down to \npartner with startups\nMoonshot now works with the likes of \nVadilal, Rungta Steel etc. \nDaftar, a smaller creative shop \ndoes work for Pepsi… \nMeanwhile a couple of glimpses of how \nmainstream ad agencies are working with \nscaling startups.\nIndus Valley - Playbooks / Indus Valley Marketing",
            "168\nMeanwhile, Indus Valley likes full stack brand-building\nFounders are building personal brands to canvass for \ntheir startups, or sometimes just to build \npersonal brands.\nZomato inspired the trend of startups setting up \nagencies. That trend has continued to gather strength.\nIndus Valley - Playbooks / Indus Valley Marketing",
            "169\nHighlighting ingredients, clever copy, and use of \ncontent are ways to build trust for India1 products. \nIn the case of India2, trust is mediated through the credibility associated with a \ncelebrity. While celebs are also used for India1 advertising, they are used more to cut \nthrough clutter (e.g., Bold Care, Cred) and less to reinforce or borrow credibility from. \nIndus Valley - Playbooks / Indus Valley Marketing\nHow trust is mediated through communication is diverging between India1 and India2. \nThe currency of trust-building is also diverging between India1 \nand India2",
            "Indus Valley\n➔\n➔\nThe various India2 Playbooks.\n➔\nHow Indus Valley influenced Indian advertising.\n➔\nReturns, and how Indian startups are \naddressing it.\n➔\nMarketing framework for the Indian diaspora or \nIndia0.\nReturns, and how \nIndian startups are \naddressing it.\nIndian startups in the consumer space, \nespecially apparel and footwear brands, \nhave a returns issue. We analyse trends \nand suggest playbooks that Brands are \nadopting / can adopt to overcome these \nchallenges. \nIndus Valley - Funding Trends Pg 95\nIPO Boom Pg 111\nSector Deep Dives Pg 120\nIndus Valley Playbooks \n170",
            "171\nHigh Return rates are a key concern area for Indian online sellers\nSource: Redseer x Ecom Express Report, Unicommerce India Ecommerce Index 2023 Report, Return Prime Report\nReturns can be even higher on \nmarketplaces\nReturns % on marketplaces is 26.3% \nvs for 6.2% on brand’s own website, \nper Unicommerce. \nReturns are higher for Cash-on-Delivery \norders \nvs prepaid orders. COD or Cash on Delivery \norder returns are 20.9% (vs 5.8% for prepaid \norders), per Unicommerce.\nReturns are highest for fashion & \nfootwear \nApparel return rates as high as 30-35% per \nReturn Prime.\nFor COD orders of fashion brands on \nmarketplaces, returns are thus in the \n45-55% range!\nAround a sixth of ecommerce shipment volumes get returned\n16%\nIndus Valley - Playbooks / Returns",
            "172\nUnderstanding Returns\nNote: * The fashion brand wants to remain unnamed\nReturn to Origin (RTO)\nCustomer not at home or \norder not delivered\nA high return rate increases logistics cost, leads to more spoilage due to the \nback-and-forth thereby increasing cost of goods sold. In the process of \ncollection, repair, and clean up it also reduces the inventory available for \nsale. Returns thereby have a corrosive impact on unit economics.\nTwo types of \nReturns\nReturn to Vendor (RTV)\nCustomer collects and \nreturns due to wrong \nitem, damages, or fit \nissues\nHow returns stack up for a fashion brand*\nOwn \nWebsite\nMarketplaces\nRTO\n10%\n9%\nRTV\n14%\n39%\nTotal Returns\n24%\n48%\nMarketplaces encourage returns (to reduce purchase \nfriction), and customer is frequently encouraged to \nbracket, i.e., buying multiple sizes and then returning \nseveral back.\nIndus Valley - Playbooks / Returns",
            "173\nReducing RTO or Return to Origin\nSource: Redseer x Unicommerce Report, Delhivery\nAjith Pai, COO, Delhivery: “There are two factors that determine the extent of RTO \n1/ Speed of fulfillment : faster the delivery, the lower the likelihood of doorstep rejections \n2/ COD vs Prepaid: the higher the Prepaid share of orders, the lower the RTO.”\nThis has been trickier. Regular customers do graduate from COD to Prepaid, but as ecommerce \nexpands to Tier 3 towns / India2, there is a rise in customers who prefer COD. So overall COD has only \nslightly moved down to 65%.\nSuccessfully increased speed of delivery \nSpeed of Fulfillment\nCOD vs Prepaid\n35% of this COD is UPI at \ndoorstep. This is higher than \nDelhivery’s peers (at 5-10%), \nand is largely a function of \ntheir focus in bringing down \ncash handling.\n2024’s avg shipment value of \nCOD is ₹660 and prepaid is \n₹1,850. Clearly richer \ncustomers pay in advance. \nPrepaid shipment value has \nincreased over the years, but \nCOD shipment value is stable.\nRTOs drop sharply with \nprepaid orders! COD order \nRTOs are 6x more likely than \nPrepaid order RTOs!\nIndus Valley - Playbooks / Returns",
            "174\nConsumer Brands (and marketplaces) are nudging buyers to prepay\nSource: Reddit, Dharmesh Ba / The India Notes\nIntroducing friction, creating commitments for COD are ways to nudge customers slowly into prepaid orders \nLevying a ‘handling fee’\n1\nNudging customers to pay in advance \nby charging more for COD\nMaking customers pay a \nsmall advance\n2\n3\nIndus Valley - Playbooks / Returns",
            "175\nD2C / Consumer Brands beginning to see the impact of these nudges\nSource: GoKwik\n an eCommerce enabler brand providing smart checkout and COD-enabler solutions shared data on how COD \nis trending downwards for the brands they support. \nAs we see here, the higher the city \ntier, the lower the COD share of \norders! \nAn interesting data point shared by \nGoKwik team was on the rise of \nCredit as a payment option at \ncheckout. From <1% in ‘22 it is at \n~5.5% in ‘24.\nTier 1 Cities COD Orders %\nTier 2 Cities COD Orders %\nTier 3 Cities COD Orders %\nRemember this was 65% for Delhivery!\nCOD orders trending down\nIndus Valley - Playbooks / Returns",
            "176\nPlaybooks to reduce RTOs: better address management\nA tale of 2 cities. Why are Indian \naddresses so long?\nAnd so hard to locate?\nAnd they cost us money!\nGC & Accel’s Bay Area office addresses \nvs Bangalore, clipped from their websites.\n“Poor addresses cost \nIndia $10 - 14 billion \nannually, ~0.5% of the \nGDP.”\n-\nDr Santanu Bhattacharya, \nMIT Media Lab\nIndus Valley - Playbooks / Returns",
            "177\nHow startups are ‘addressing’ RTOs :)\nThese are 2 interesting demand-side solutions that tackle the \nproblem on the customer’s end (as compiled by Dharmesh Ba) \n●\n Add a video guide (Bharat Agri) \n●\nAdd a pic of your front door (Swiggy)\nThere are 2 supply-side innovations to drive down RTOs\n●\nRTO predictor by Delhivery (below, left image) \n●\nGoKwik’s offering to reduce RTO (below right) \nCustomer-end solution\nSupply-side solution\nSource: Dharmesh Ba / The India Notes, Delhivery, and GoKwik\nIndus Valley - Playbooks / Returns",
            "178\nHow brands are attacking RTV (Return to Vendor)\nSource: Return Prime website, Slikk website\nEncourage exchanges \ninstead of refunds\nOffer store credit / gift \ncards instead of cash \nback, enhancing friction \nto avoid lazy \n‘bracketing’.\nAbove via\nSlikk, a qCom \napparel player offers \na “Try & Buy” option, \nto reduce the \nchances of a misfit. \n~20% of orders are \nvia “Try & Buy” - says \nSlikk cofounder \nAkshay Gulati.\nAbove via\nPromote exchanges over refunds\nTry & Buy\nIndus Valley - Playbooks / Returns\nUltimately the only way to address this is through better fits (the biggest reason for RTB. However, two interesting playbooks \nare shown below",
            "➔\n➔\nThe various India2 Playbooks.\n➔\nHow Indus Valley influenced Indian advertising.\n➔\nReturns, and how Indian startups are addressing \nit.\n➔\nMarketing framework for the Indian diaspora \nor India0.\n Indus Valley\nMarketing framework \nfor the Indian diaspora \nor India0.\nNo report is complete without a 2x2. Here \nis our framework for how brands can \nposition themselves for the Indian \ndiaspora (or India0) basis affluence and \naffiliation (or affinity). We give example of \nstrategies / playbooks for three of the \nfour quadrants.\nIndus Valley - Funding Trends Pg 95\nIPO Boom Pg 111\nSector Deep Dives Pg 120\nIndus Valley Playbooks \n179",
            "180\nIndus Valley - Playbooks / Diaspora Marketing\nIndian Diaspora, and India0\nSource: Indian Express, Ministry of Foreign Affairs, MEA, PHDCCI, IBEF\nThe Indian Diaspora is affluent and influential. Their economic power is reflected in high \nremittance flows into India - the highest in the world ($107 Bn in 2023-24) and interestingly \ngreater than FDI flows into India ($70.9 Bn in 2023-24) . At Blume, we like to use the term India0 \nas a moniker for this economically ascendant community. \nAs of May 2024, the total number \nof overseas Indians worldwide is \napproximately 35.42 million.\nPIOs\nNRIs\nUSA\n5.4 Mn\nMalaysia\n2.9 Mn\nCanada\n2.8 Mn\nMyanmar\n2 Mn\nUK\n1.9 Mn\nSouth Africa\n1.7 Mn\nHow large is the Indian Diaspora?\nThe Indian Diaspora is well spread out across different continents and geographies\n��\nSaudi Arabia\n2.5 Mn\nUAE\n3.6 Mn",
            "181\nIndia0 punches above its population weight class\nSource: Indus Valley Report 2024, Times of India\nIn the US, the Indian community ranks highest in \nmedian household income.\n Indian Diaspora makes up 1.5% of the US \npopulation, and this group accounts for 5-6% of all \nUS taxes.\nIndia0 are the highest earners in \nmost host countries\nIndian culture is breaking out into the \nglobal mainstream\nGlobal players are waking up to the \nspending power of this diaspora\nIndus Valley - Playbooks / Diaspora Marketing",
            "182\nBlume’s Diaspora Marketing Framework\nThe following framework maps out different brands and the diaspora personas they are catering to. We have categorised the diaspora personas \nbased on their income levels (high or low earners) and their level of affiliation to their country of origin (high or low affiliation).\nIndus Valley - Playbooks / Diaspora Marketing",
            "183\nDiaspora marketing: case studies\nSource: Moneycontrol, Fortune India\nIndus Valley - Playbooks / Diaspora Marketing",
            "How Inde Wild broke into the global mainstream\n184\nBrand started out as an influencer \nbrand on the back of founder Diipa \nBüller-Khosla’s following\n1\nFrom here they made their foray into \nthe mainstream\nFrom here, brand expanded to \nmulticultural audiences across four \nkey geos - US, UK, Canada and India\n2\n3\nThe founder, is a \nglobal-Indian influencer. \nShe leveraged her \ncommunity of 2m+ \nindividuals to curate test \ngroups across 4 \ngeographies and identify \nunaddressed gaps in \nthe skincare market.\nSource: Inde wild\n54% from \nIndia\nRest from \nUS + UK\nIndus Valley - Playbooks / Diaspora Marketing",
            "185\nDiaspora marketing channels \nIndus Valley - Playbooks / Diaspora Marketing",
            "186\nAcknowledgements\nAs with all reports, this too rests on the labour of several analysts, researchers and writers whose work we used to \nbuild on. We stand on the shoulders of giants. We have acknowledged the sources and their contributions on each \nof the pages; in particular, a shout out to Jefferies, Bernstein, Goldman, Redseer, UBS, CRIF, Barclays, Nuvama, \nCLSA, Tracxn, for their regular reports enabling greater access to data, and enhancing our understanding of the \nIndian startup ecosystem. We also acknowledge the inputs and insights of Rahul Mathur, Dharmesh Ba, Arindam \nPaul and other astute observers of the Indian startup ecosystem - thank you for your openness in explaining the \nworld from your perspective, and sharing insights that inform this report. This time we also had the participation of \nseveral startups such as Delhivery, GoKwik, MyGate, Stage, Kaleidofin, Salty, Inde Wild, VoiceClub etc., who \nhelped us with their proprietary data sets that we were able to analyse and draw insights from. We thank them \nprofusely for this support!\nFinally, we would also like to thank the wider Blume team, especially Joseph Sebastian, for their inputs.\nAm sure I have possibly left out a lot more names! Apologies in advance for the same!\n-\nSajith, Anurag, Nachammai & Dhruv",
            "187\nAbout Blume Ventures\nBlume Ventures is an early stage venture firm based across Mumbai, Bangalore, Delhi and San Francisco, that \nprovides ‘conviction capital’ to founders across India consumer internet as well as software & enterprise technology.\nWe add value through a platform approach – over 85 specialists across shared CFO services, legal advisory, talent \nacquisition, capital raising, GTM enablement, operations support – who focus entirely on supporting portfolio \ncompanies and helping founders learn, thereby greatly improving their chances of success. Our value-added \napproach has helped us retain board representation in the vast majority of our top companies; with an overall Asset \nunder Management (AUM) upwards of $650M.\nYou can read more about us at blume.vc"
        ],
        "tables": [
            [
                [
                    "Indus Valley Annual Report 2025\nSajith Pai | sp@blume.vc\nAnurag Pagaria | anurag@blume.vc\nNachammai Savithiri | ns@blume.vc\n&\nDhruv Trehan, Editorial Fellow",
                    ""
                ]
            ],
            [
                [
                    "Indus Valley Annual Report 2025",
                    ""
                ]
            ],
            [
                [
                    "Sajith Pai | sp@blume.vc\nAnurag Pagaria | anurag@blume.vc\nNachammai Savithiri | ns@blume.vc\n&\nDhruv Trehan, Editorial Fellow",
                    ""
                ]
            ],
            [
                [
                    "Welcome to the Indus Valley Annual Report 2025\nIndia’s vibrant startup ecosystem, concentrated in the eastern suburbs of Bangalore, the satellite cities of\nGurgaon and Noida in the Delhi National Capital Region (NCR), the districts of Lower Parel & the Andheri East –\nPowai belt in Mumbai, the Southern suburbs of Chennai, and in the various scattered pockets across many other\ncities such as Pune, Hyderabad, Chandigarh etc., has lacked a singular name.\nAt Blume, we like to use Indus Valley as a catch all moniker for the Indian startup ecosystem. It is a twist on the\ntypical Silicon Wadi / Glen / Fen naming convention, as well as a reference to the Indus Valley Civilisation, one of\nthe vibrant centres of the ancient world, and the ancestral civilisation of the Indian people.\nUnlike Silicon Valley which has a geographical connotation, the term Indus Valley has no such overtone. It is\ninstead a reference to the entire Indian startup ecosystem, spread throughout the nation. It is also an attitude, a\nmindset, one of invention, and ‘jugaad’ and chutzpah.\nThe Indus Valley Annual Report published by Blume Ventures, celebrates the rise of Indus Valley, and its\nemergence as one of the centres of innovation and enterprise in the startup world. It gives us a chance to look\nback, and take stock of its evolution, and look ahead to what is coming. We welcome you to the fourth edition of\nthe Indus Valley Annual Report! Our previous editions (2024, 2023, 2022) can be accessed at the website\nindusvalleyreport.com\n2",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "2"
                ]
            ],
            [
                [
                    "India Indus Valley\nIndia - The Last Five Years Pg 7 Indus Valley - Funding Trends Pg 95\nVenture funding trends, and a deep dive, followed by a look at\nA macro-economic account of the Indian economy over the last five\nIndia’s Unicorns, and the Venture Debt market.\nyears, from the COVID-pandemic and bust, to the recent growth taper.\nLong-Term Structural Forces Pg 20\nIPO Boom Pg 111\n➔ Consumption and services dominate our GDP. (21) A d e e p d i v e i n t o I n d i a ' s b o o m i n g I P O market, as well as the SME\n➔ India is formalising, steadily. (29) IPO’s rise, including what it implies for founders.\n➔ India doesn’t save enough. (33)\n➔ Why land issues mean India hoards up on gold. (37)\n➔ India doesn’t invest in human capital. (41)\nSector Deep Dives Pg 120\n➔ India’s manufacturing playbook is good, but not great. (48)\n➔ How DPI made India a Digital Welfare State. (54) ➔ Quick Commerce: Why it works in India, the implications of its\n➔ How India1’s savings surplus spur an Equity and F&O boom. (58) rise, and is there irrational exuberance re QCom? (120)\n➔ AI: Is India getting a foundational model soon? (148)\nConsumption Pg 66\nIndus Valley Playbooks Pg 157\n➔ India’s consumption numbers look good on an overall basis, but\nnot on a per capita basis.\n➔ Why India under consumes. ➔ The various India2 Playbooks. (157)\n➔ How India1, India’s top 10%, drives the Indian economic engine. ➔ How Indus Valley influenced Indian advertising. (165)\n➔ India1 is not widening as much as deepening. ➔ Returns, and how Indian startups are addressing it. (170)\n➔ India1’s high share of consumption shapes the India consumer ➔ Marketing framework for the Indian diaspora or India0. (179)\nmarket in many distinct ways.\n3",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "3"
                ]
            ],
            [
                [
                    "How to read this report\nGiven we have sourced the data across various reports and datasets, consistency in data will always be\na challenge. That said, while sometimes an occasional number or two may not match with the other, the\nbroad direction or narrative of these is consistent and comparable.\nWe have used millions, billions, trillions (vs lacs, crores) where possible. When we use ₹ billion or ₹\ntrillion, it can sometimes be hard to translate it to $. A shorthand for ₹ billion to $ million is that ₹1 billion =\n₹100 crores = $12 million roughly. A shorthand for ₹ trillion to $ billion is ₹1 trillion = $12 billion roughly.\nDespite all the charts and datasets we have listed, this is not a data book. We didn’t create it to serve as\nan exhaustive repository of data or reportage on India. Rather, it is more a narrative, and less a\ndataguide. Or even better, you should see it as a source of perspective on the Indian startup ecosystem.\nAnd as with all perspectives, a lot depends on the vantage point of the observer. As the leading seed\nfund in India, we do think we have a unique perspective and insight into the Indian startup ecosystem, or\nIndus Valley, as we term it. And with The Indus Valley Report, we hope to get you, dear reader, to view\nthe Indian economy through our lens. Do tell us how you see it. Compliments, criticism, feedback all\nwelcome at sp@blume.vc and / or anurag@blume.vc\n4",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "4"
                ]
            ],
            [
                [
                    "India in one tweet\nAI meets caste. Cutting-edge tech-advances in AI collide with that most ancient of Indian institutions, the caste system.\nThe associations in this tweet expose a clear bias.\nMany of these would be considered inappropriate in\ncontemporary Indian discourse.\nYet, the AI completion offers a glimpse at how India’s\ndeeply rooted social structures continue to shape\nperspectives, even when filtered through modern\ntechnologies and global pop culture touchpoints.\n[Redacted]\nSource: Twitter / @dhammainvicta; The tweet was subsequently deleted 6",
                    null,
                    null
                ],
                [
                    "Source: Twitter / @dhammainvicta; The tweet was subsequently deleted",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "6"
                ]
            ],
            [
                [
                    "India\nIndia - The Last Five Years Pg 7\nIndia - The Last 5 Years\nA macro-economic account of the Indian economy over\nthe last five years, since the COVID-pandemic and bust,\nto the recent growth taper.\nHow we got here; a look at the events,\ntrends, policies, and initiatives that\nshaped the Indian economy over the past\nLong-term Structural Forces Pg 20\nfive years through COVID, and after. We\ncover the economic downturn,\ngovernment initiatives to spur recovery,\nConsumption Pg 66\nsubsequent boom, and inflationary\ngrowth, followed by RBI initiatives to\ncontrol inflation, and finally the growth\ntaper as consumption and government\nspends reduced.\n7",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "7"
                ]
            ],
            [
                [
                    "",
                    "8"
                ]
            ],
            [
                [
                    "But how did we get here?\nThe next few slides capture the journey the Indian Economy has been on in the last few years.\n9",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "9"
                ]
            ],
            [
                [
                    "",
                    "10"
                ]
            ],
            [
                [
                    "",
                    "11"
                ]
            ],
            [
                [
                    "",
                    "12"
                ]
            ],
            [
                [
                    "",
                    "13"
                ]
            ],
            [
                [
                    null,
                    null,
                    "Growing money supply",
                    null,
                    "Elevated inflation rates",
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    null,
                    ""
                ],
                [
                    "",
                    "",
                    "",
                    "",
                    "",
                    null
                ],
                [
                    null,
                    null,
                    "",
                    null,
                    null,
                    null
                ]
            ],
            [
                [
                    "",
                    "14"
                ]
            ],
            [
                [
                    "",
                    "15"
                ]
            ],
            [
                [
                    "",
                    "16"
                ]
            ],
            [
                [
                    "",
                    "17"
                ]
            ],
            [
                [
                    "",
                    "18"
                ]
            ],
            [
                [
                    "",
                    "19"
                ]
            ],
            [
                [
                    "India\nConsumption and services dominate our GDP.\nIndia - The Last Five Years Pg 7\nLong-Term Structural Forces India is formalising, steadily.\nThe Indian economy is shaped by the interaction\nbetween, and acting upon of several powerful long-term India doesn’t save enough.\nstructural forces and trends. A closer look at these\nlong-term structural forces!\nWhy land issues mean India hoards up on gold.\nConsumption Pg 66\nIndia doesn’t invest in human capital.\nIndia’s manufacturing playbook is good, but not great.\nHow DPI made India a Digital Welfare State.\nHow India1’s savings surplus spur an equity and F&O boom.\n20",
                    "Consumption and services dominate our GDP.\nIndia is formalising, steadily.\nIndia doesn’t save enough.\nWhy land issues mean India hoards up on gold.\nIndia doesn’t invest in human capital.\nIndia’s manufacturing playbook is good, but not great.\nHow DPI made India a Digital Welfare State.\nHow India1’s savings surplus spur an equity and F&O boom.\n20",
                    null,
                    null,
                    ""
                ],
                [
                    null,
                    null,
                    "",
                    "20",
                    null
                ],
                [
                    null,
                    null,
                    "",
                    null,
                    null
                ]
            ],
            [
                [
                    "India\nIndia - The Last Five Years Pg 7\nConsumption and\nLong-Term Structural Forces\nservices dominate\n➔ Consumption and services dominate our GDP.\nour GDP\n➔ India is formalising, steadily.\n➔ India doesn’t save enough.\n➔ Why land issues mean India hoards up on gold. Consumption and services drive the\n➔ India doesn’t invest in human capital.\nIndian economy, unlike say in China,\n➔ India’s manufacturing playbook is good, but not\ngreat. where investments and manufacturing\n➔ How DPI made India a Digital Welfare State.\nplay a key role.\n➔ How India1’s savings surplus spur an Equity and\nF&O boom.\nConsumption Pg 66\n21",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "21"
                ]
            ],
            [
                [
                    null,
                    "PFCE\n(Consumption)\n56%\nGFCF\n(Investment)\n33%",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    "Services\n54%\nIndustry\n31%",
                    null,
                    null,
                    null
                ],
                [
                    "",
                    "",
                    "Govt. Spends 9%",
                    null,
                    null,
                    null,
                    null,
                    "",
                    "",
                    "",
                    null,
                    null,
                    ""
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    "Govt. Spends 9%",
                    null,
                    null,
                    null,
                    null,
                    null,
                    "",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "",
                    null,
                    "",
                    null,
                    null,
                    null,
                    "",
                    "",
                    "Agriculture\n15%",
                    "",
                    null
                ],
                [
                    null,
                    null,
                    "",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    "",
                    "",
                    null,
                    "",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    "",
                    "",
                    "Others (Exports less\nImports etc ) 2%",
                    "Others (Exports less",
                    null,
                    null,
                    "",
                    null,
                    "",
                    "",
                    "",
                    "",
                    ""
                ],
                [
                    null,
                    null,
                    "",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ]
            ],
            [
                [
                    "Imports etc",
                    ") 2%"
                ]
            ],
            [
                [
                    "",
                    "22"
                ]
            ],
            [
                [
                    "",
                    "",
                    "PFCE has consistently been at 55-60% of Indian GDP through the last decade"
                ],
                [
                    null,
                    "",
                    null
                ]
            ],
            [
                [
                    "",
                    "23"
                ]
            ],
            [
                [
                    "",
                    "",
                    "China\n2000-09 | 37.8%\n2010-19 | 43.2%\n2020-23 | 41.9%"
                ]
            ],
            [
                [
                    "C\n2\n2\n2",
                    "C\n2\n2\n2",
                    "hina\n000-09 | 44.7%\n010-19 | 46.7%\n020-23 | 44.7%"
                ]
            ],
            [
                [
                    "",
                    "24"
                ]
            ],
            [
                [
                    "",
                    "",
                    "Services Labour Force % Split"
                ],
                [
                    null,
                    "Financial &\nProfessional Services,\nReal Estate (23%) Services is a large contributor to India’s\neconomy; unusual for a country with per capita\nincome under $3k.\nPublic Services (13%)\nTrade, Transportation, Hotels,\nCommunication (19%)",
                    null
                ]
            ],
            [
                [
                    "",
                    "Financial &\nProfessional Services,\nReal Estate (23%)"
                ],
                [
                    null,
                    "Public Services (13%)"
                ],
                [
                    null,
                    "Trade, Transportation, Hotels,\nCommunication (19%)"
                ]
            ],
            [
                [
                    "",
                    "",
                    "Mining & Utilities (5%)"
                ],
                [
                    null,
                    "",
                    "Construction (9%)"
                ]
            ],
            [
                [
                    "Mining & Utilities",
                    "(5%)"
                ]
            ],
            [
                [
                    "",
                    "Manufacturing(17%)"
                ]
            ],
            [
                [
                    "46% of Labour",
                    "Force"
                ]
            ],
            [
                [
                    "Source:",
                    "MOSPI, PLFS 23-24"
                ]
            ],
            [
                [
                    "",
                    "25"
                ]
            ],
            [
                [
                    null,
                    "Services dominating Industry is not a new trend",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    "",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    "% Share of Gross Value Added (GVA): Agriculture, Industry and Services FY64-FY24",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    "Industry and manufacturing\nhas consistently been a\nsmaller portion of the\neconomy than services.",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    "Industry and manufacturing\nhas consistently been a\nsmaller portion of the\neconomy than services.",
                    null,
                    null
                ],
                [
                    "",
                    "",
                    "",
                    "",
                    ""
                ],
                [
                    null,
                    "",
                    "",
                    null,
                    null
                ]
            ],
            [
                [
                    "",
                    "26"
                ]
            ],
            [
                [
                    "",
                    "27"
                ]
            ],
            [
                [
                    "",
                    "28"
                ]
            ],
            [
                [
                    "India\nIndia - The Last 5 Years Pg 7\nIndia is formalising\nLong-Term Structural Forces\nsteadily\n➔ Consumption and Services dominate our GDP.\nWe are seeing a steady but firm shift to a\n➔ India is formalising, steadily.\n➔ India doesn’t save enough. organised, branded, formal market, from\n➔ Why land issues mean India hoards up on gold.\nwhat was an unorganised, unbranded,\n➔ India doesn’t invest in human capital.\n➔ India’s manufacturing playbook is good, but not and informal market.\ngreat.\n➔ How DPI made India a Digital Welfare State.\n➔ How India1’s savings surplus spur an Equity and\nF&O boom.\nConsumption Pg 66\n29",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "29"
                ]
            ],
            [
                [
                    "",
                    "30"
                ]
            ],
            [
                [
                    "",
                    "31"
                ]
            ],
            [
                [
                    "Fans market shift",
                    null,
                    null,
                    "Wedding and celebration-wear shift",
                    null,
                    null,
                    null,
                    "Cables and wires shift"
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    ""
                ],
                [
                    "",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    "",
                    null,
                    null,
                    null
                ],
                [
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    ""
                ],
                [
                    "",
                    null,
                    "",
                    "",
                    null,
                    null,
                    "",
                    ""
                ],
                [
                    "",
                    null,
                    "",
                    "",
                    null,
                    null,
                    "",
                    ""
                ]
            ],
            [
                [
                    "",
                    "32"
                ]
            ],
            [
                [
                    "India\nIndia - The Last Five Years Pg 7\nIndia doesn’t save\nLong-Term Structural Forces\nenough\n➔ Consumption and services dominate our GDP\n➔ India is formalising, steadily. India’s savings is good but not\n➔ India doesn’t save enough.\ngreat. A high savings rate is\n➔ Why land issues mean India hoards up on gold.\n➔ India doesn’t invest in human capital necessary given low FDI rates. A\n➔ India’s manufacturing playbook is good, but not\ndeep dive into savings illustrates\ngreat\n➔ How DPI made India a Digital Welfare State\nthat the culprit is financial savings\n➔ How India1’s savings surplus spur an Equity and\nF&O boom (as opposed to physical savings),\nand the reason is rise in financial\nliabilities, chiefly led by rising\nConsumption Pg 66\n(unsecured) personal loans.\n33",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "33"
                ]
            ],
            [
                [
                    null,
                    "",
                    "30%"
                ],
                [
                    null,
                    "",
                    null
                ],
                [
                    "",
                    null,
                    ""
                ]
            ],
            [
                [
                    null,
                    "18.",
                    "4%"
                ],
                [
                    null,
                    "",
                    null
                ],
                [
                    "",
                    null,
                    null
                ]
            ],
            [
                [
                    "",
                    "34"
                ]
            ],
            [
                [
                    "",
                    "35"
                ]
            ],
            [
                [
                    "",
                    "36"
                ]
            ],
            [
                [
                    "India\nIndia - The Last Five Years Pg 7\nWhy land issues mean\nLong-Term Structural Forces\nIndia hoards up on\n➔ Consumption and services dominate our GDP.\ngold.\n➔ India is formalising, steadily.\n➔ India doesn’t save enough.\n➔ Why land issues mean India hoards up on gold. India is the world’s second largest\n➔ India doesn’t invest in human capital.\nconsumer of gold. Behind this are cultural\n➔ India’s manufacturing playbook is good, but not\ngreat. factors, and economic factors, chiefly the\n➔ How DPI made India a Digital Welfare State.\npoor land records, and the challenges in\n➔ How India1’s savings surplus spur an Equity and\ncollateralising land. Gold is a far more\nF&O boom.\nconvenient collateral as we see from\nthese slides.\nConsumption Pg 66\nThis section was authored by\nJoseph Sebastian, from Blume’s\nFintech team\n37",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "37"
                ]
            ],
            [
                [
                    "",
                    "38"
                ]
            ],
            [
                [
                    null,
                    "2\nFor lenders, gold-backed loans offer a\nsignificant advantage since the collateral\nis relatively simple to repossess if\nneeded and It can be quickly sold in\ncase of default."
                ],
                [
                    "Source: Fortune India, Indian Express, Financial Express",
                    ""
                ]
            ],
            [
                [
                    "",
                    "39"
                ]
            ],
            [
                [
                    "#136",
                    "India"
                ]
            ],
            [
                [
                    "",
                    "40"
                ]
            ],
            [
                [
                    "India\nIndia - The Last Five Years Pg 7\nIndia underinvests in\nLong-Term Structural Forces\nits human capital\n➔ Consumption and Services dominate our GDP.\n➔ India is formalising, steadily. Behind India’s underinvestment in human\n➔ India doesn’t save enough. capital, is a set of complex interlinked\n➔ Why land issues mean India hoards up on gold.\nfactors but chiefly path dependence from\n➔ India underinvests in human capital.\n➔ India’s manufacturing playbook is good, but not its decision post-1947 to invest in the\ngreat.\ntertiary education sphere over the\n➔ How DPI made India a Digital Welfare State.\n➔ How India1’s savings surplus spur an Equity and primary and secondary education sphere\nF&O boom. (unlike the Asian Tigers and China which\ninvested in primary and secondary\neducation over tertiary) and developed a\nConsumption Pg 66\nskilled labour force.\n41",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "41"
                ]
            ],
            [
                [
                    "",
                    "",
                    ""
                ],
                [
                    "",
                    "18 Mn",
                    ""
                ]
            ],
            [
                [
                    "326.5 Mn",
                    null
                ],
                [
                    null,
                    "58% Self-Employed\n(33% of self-employed are unpaid helpers in a household enterprise)"
                ]
            ],
            [
                [
                    "110.7 Mn",
                    "20% Casual Workers"
                ]
            ],
            [
                [
                    "",
                    "51.0 Mn",
                    "",
                    "",
                    "9% Regular Salary Employees with job contract"
                ],
                [
                    "",
                    "",
                    "",
                    null,
                    null
                ]
            ],
            [
                [
                    "Peers: % Regular Salary Employees in the Workforce",
                    null
                ],
                [
                    "Russia",
                    "93%"
                ],
                [
                    "Brazil",
                    "68%"
                ],
                [
                    "China",
                    "54%"
                ],
                [
                    "Bangladesh",
                    "42%"
                ]
            ],
            [
                [
                    "",
                    "42"
                ]
            ],
            [
                [
                    "",
                    "intensive, jobless growth is a likely scenario."
                ]
            ],
            [
                [
                    "",
                    "43"
                ]
            ],
            [
                [
                    null,
                    "India’s youth unemployment rate by level of education (%), 2022",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    "",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    "",
                    null,
                    null
                ],
                [
                    "",
                    "",
                    "",
                    "",
                    ""
                ],
                [
                    null,
                    "",
                    "",
                    "",
                    null
                ]
            ],
            [
                [
                    "",
                    "44"
                ]
            ],
            [
                [
                    "",
                    "45"
                ]
            ],
            [
                [
                    "",
                    "46"
                ]
            ],
            [
                [
                    "",
                    "47"
                ]
            ],
            [
                [
                    "India\nIndia - The Last Five Years Pg 7\nIndia’s manufacturing\nLong-Term Structural Forces\nplaybook is good, but\n➔ Consumption and services dominate our GDP.\nnot great.\n➔ India is formalising, steadily.\n➔ India doesn’t save enough.\n➔ Why land issues mean India hoards up on gold.\n➔ India doesn’t invest in human capital. India has struggled to grow its\n➔ India’s manufacturing playbook is good, but\nmanufacturing sector historically, though\nnot great.\n➔ How DPI made India a Digital Welfare State. it is making a spirited attempt now using\n➔ How India1’s savings surplus spur an Equity and important bans, tariffs, and\nF&O boom.\nproduction-linked incentives. The journey\nhas been impressive but not as good as\nsay Vietnam’s.\nConsumption Pg 66\n48",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "48"
                ]
            ],
            [
                [
                    "",
                    "49"
                ]
            ],
            [
                [
                    "Because of land, labour and capital",
                    ""
                ],
                [
                    "",
                    null
                ]
            ],
            [
                [
                    "",
                    "51"
                ]
            ],
            [
                [
                    "And the effects are beginning to be seen in various industries",
                    ""
                ],
                [
                    "",
                    null
                ]
            ],
            [
                [
                    "",
                    "",
                    ""
                ]
            ],
            [
                [
                    "",
                    "52"
                ]
            ],
            [
                [
                    null,
                    null,
                    ""
                ],
                [
                    "",
                    "",
                    ""
                ]
            ],
            [
                [
                    "",
                    "53"
                ]
            ],
            [
                [
                    "India\nIndia - The Last Five Years Pg 7\nDPI has helped India\nLong-term Structural Forces\nbecome a ‘Digital\n➔ Consumption and services dominate our GDP.\nWelfare State’\n➔ India is formalising, steadily.\n➔ India doesn’t save enough.\n➔ Why land issues mean India hoards up on gold.\nA good way to understand India is as a\n➔ India doesn’t invest in human capital.\n➔ India’s manufacturing playbook is good, but not Digital Welfare State, one that leverage\ngreat.\nDPI protocols to deliver cash and in-kind\n➔ How DPI made India a Digital Welfare State.\n➔ How India1’s savings surplus spur an Equity and benefits directly to the end users. Not all\nF&O boom. DPI protocols necessarily succeed, and\nwe are beginning to see second-order\neffects of DPI policies emerge!\nConsumption Pg 66\n54",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "54"
                ]
            ],
            [
                [
                    "",
                    ""
                ],
                [
                    null,
                    "“Today, in just 30 seconds, I can\ndirectly transfer money into the\naccounts of 100 million farmers.\nToday, I can send subsidy to 130\nmillion gas cylinder consumers with\njust one click, in 30 seconds. Billions\nthat were being siphoned out due to\ncorruption are now saved.”\n- PM Narendra Modi"
                ],
                [
                    "People by WTF, Nikhil Kamath",
                    null
                ]
            ],
            [
                [
                    "",
                    "2000",
                    "",
                    "2016",
                    "",
                    "2018",
                    "",
                    "2019",
                    "",
                    "2021"
                ],
                [
                    "Source: Motilal Oswal, DBT Website, People by WTF",
                    "",
                    null,
                    "",
                    null,
                    "",
                    null,
                    "",
                    null,
                    null
                ]
            ],
            [
                [
                    "",
                    "55"
                ]
            ],
            [
                [
                    "# of Mobility Orders",
                    null,
                    null,
                    ""
                ],
                [
                    null,
                    "# of Mobility Orders",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    null,
                    ""
                ],
                [
                    null,
                    "# of Retail Orders",
                    "# of Retail Orders",
                    null
                ]
            ],
            [
                [
                    "",
                    "56"
                ]
            ],
            [
                [
                    null,
                    "June Dec",
                    null
                ],
                [
                    "",
                    "",
                    null
                ],
                [
                    null,
                    null,
                    ""
                ],
                [
                    null,
                    "",
                    ""
                ]
            ],
            [
                [
                    "June",
                    "Dec"
                ]
            ],
            [
                [
                    "June",
                    "Dec"
                ],
                [
                    "2024",
                    "2024"
                ]
            ],
            [
                [
                    "",
                    "57"
                ]
            ],
            [
                [
                    "India\nIndia - The Last Five Years Pg 7\nHow India1’s savings\nLong-term Structural Forces\nsurplus spur an equity\n➔ Consumption and services dominate our GDP.\nand F&O boom.\n➔ India is formalising, steadily.\n➔ India doesn’t save enough.\n➔ Why land issues mean India hoards up on gold.\n➔ India doesn’t invest in human capital.\nIndia1’s surplus savings are finding their\n➔ India’s manufacturing playbook is good, but not\nway into the equity market, creating the\ngreat.\n➔ How DPI made India a Digital Welfare State. 4th largest equity market, and the biggest\n➔ How India1’s savings surplus spur an equity\nequity derivatives market (by volume).\nand F&O boom.\nSEBI has come down hard on the equity\nderivatives market (effectively ‘financial\nConsumption Pg 66 gambling’) and the impact is visible.\n58",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "58"
                ]
            ],
            [
                [
                    null,
                    "Equity’s share of HH savings\nhas more than doubled over\nthe last 10 years."
                ],
                [
                    "",
                    ""
                ]
            ],
            [
                [
                    "",
                    "59"
                ]
            ],
            [
                [
                    "",
                    "60"
                ]
            ],
            [
                [
                    "",
                    "61"
                ]
            ],
            [
                [
                    "Did you know India is the largest derivative market in the world?",
                    ""
                ],
                [
                    "",
                    null
                ]
            ],
            [
                [
                    "",
                    "62"
                ]
            ],
            [
                [
                    "Much of the volume is driven from short term speculative trades",
                    null
                ],
                [
                    "done by retail investors",
                    ""
                ],
                [
                    "",
                    ""
                ]
            ],
            [
                [
                    "",
                    "63"
                ]
            ],
            [
                [
                    "",
                    "64"
                ]
            ],
            [
                [
                    "",
                    "65"
                ]
            ],
            [
                [
                    "India\nIndia - The Last Five Years Pg 7\nConsumption\nLong-Term Structural Forces Pg 20\nIndia’s consumption numbers look good\nConsumption Pg 66\non an overall basis, but not on a per\nA deep dive into India’s consumption patterns, and the capita basis. We take a look at why this\nIndian consumer stack, including India1 and how it\nis so. We look at how India1, India’s top\nshapes the Indian consumer market.\n10%, drives the Indian economic engine,\nand find that India1 is not widening as\nmuch as deepening. Finally, we show\nhow India1’s high share of consumption\nshapes the India consumer market in\nmany distinct ways.\n66",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "66"
                ]
            ],
            [
                [
                    "Source: Twitter / Vivek Raju 67",
                    null,
                    null
                ],
                [
                    "Source: Twitter / Vivek Raju",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "67"
                ]
            ],
            [
                [
                    "",
                    null
                ],
                [
                    "",
                    null
                ],
                [
                    null,
                    "GFCF is essentially creation of productive assets such\nas machinery, infrastructure. Unlike India, investment\n(GFCF) plays a larger role in China’s GDP at 41% vs.\nIndia’s 31%."
                ]
            ],
            [
                [
                    "",
                    "68"
                ]
            ],
            [
                [
                    null,
                    null,
                    "Govt.\npenses",
                    null,
                    ""
                ],
                [
                    "Ex",
                    null,
                    "Govt.\npenses",
                    null,
                    null
                ],
                [
                    null,
                    null,
                    "Govt.",
                    null,
                    null
                ],
                [
                    null,
                    "Ex",
                    "penses",
                    null,
                    null
                ],
                [
                    null,
                    null,
                    "Others\n10%\nGFCF\n30%",
                    "",
                    "C"
                ],
                [
                    null,
                    null,
                    "",
                    "",
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    ""
                ]
            ],
            [
                [
                    "",
                    ""
                ],
                [
                    "Services\n$1 Tn\n40%",
                    "Retail\n$1.1 Tn\n55%"
                ],
                [
                    "",
                    ""
                ]
            ],
            [
                [
                    null,
                    "",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    "Other Retail\n$270 Bn (27%)\n(Consumer Durables, Gems &",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    "$270 Bn (27%)\n(Consumer Durables, Gems &",
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "Jewellery etc)",
                    null,
                    null,
                    null,
                    "",
                    null
                ],
                [
                    null,
                    "Restaurants",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    "Restaurants",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    "",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    "$70 Bn (7%)",
                    null,
                    null,
                    null,
                    "",
                    null,
                    null
                ],
                [
                    null,
                    "Fashion & BPC\n$110 Bn (10%)",
                    null,
                    "Fashion & BP\n$110 Bn (10%)",
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    "",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    "",
                    "Grocery & FMCG\n$550 Bn (50%)",
                    null,
                    null,
                    null,
                    null,
                    null,
                    ""
                ],
                [
                    null,
                    "",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ]
            ],
            [
                [
                    "Online (7%)",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    "Online (7%)",
                    null,
                    "",
                    null,
                    null,
                    null,
                    "",
                    null
                ],
                [
                    null,
                    "",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    "",
                    "",
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    "Unbranded",
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    "",
                    null,
                    "",
                    "Non",
                    "y"
                ],
                [
                    null,
                    null,
                    null,
                    "(63%)",
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    "D",
                    "iscretionar",
                    "y"
                ],
                [
                    null,
                    null,
                    null,
                    "",
                    "",
                    null,
                    null,
                    "(71%)",
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    "",
                    null,
                    null,
                    "",
                    null
                ],
                [
                    null,
                    "Offline\n(93%)",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    "",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    "",
                    "Branded\n(37%)",
                    "",
                    "D",
                    null,
                    "",
                    "y"
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    "D",
                    "iscretionar",
                    "y"
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    "(29%)",
                    null
                ],
                [
                    null,
                    null,
                    null,
                    "",
                    null,
                    null,
                    null,
                    "",
                    null
                ]
            ],
            [
                [
                    "",
                    "70"
                ]
            ],
            [
                [
                    null,
                    "India vs Indonesia vs China: Consumption Expenditure Per Capita (in USD)",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    "",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "We are roughly\nwhere China was\nin 2010",
                    "",
                    null
                ],
                [
                    "",
                    "",
                    "",
                    "",
                    ""
                ],
                [
                    null,
                    "",
                    "",
                    "",
                    null
                ],
                [
                    "",
                    "",
                    "",
                    "",
                    ""
                ],
                [
                    null,
                    "",
                    "",
                    null,
                    null
                ]
            ],
            [
                [
                    "",
                    "71"
                ]
            ],
            [
                [
                    null,
                    "Anon fintech founde\n“35-40M unique card\nholders. But active wil\nin range of 22-28M”"
                ],
                [
                    "Source: FT Partners",
                    ""
                ]
            ],
            [
                [
                    "",
                    "72"
                ]
            ],
            [
                [
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    "India accou\n~7% of glob\nunits sold. C\nwas ~55%.",
                    null,
                    null,
                    null
                ],
                [
                    "Source: Ola DRHP",
                    null,
                    null,
                    null,
                    "Source: Jefef ries",
                    null,
                    "",
                    null,
                    null,
                    null
                ],
                [
                    "",
                    null,
                    "Rural per-capita FMCG\nspends are even lower,\nat one third of urban.",
                    null,
                    "",
                    "",
                    null,
                    null,
                    null,
                    null
                ],
                [
                    "Source: Jefef ries",
                    null,
                    null,
                    null,
                    "",
                    null,
                    null,
                    "",
                    "",
                    "73"
                ],
                [
                    null,
                    "urce: Jefef ries",
                    null,
                    "",
                    "Source: CLSA / Technopak",
                    null,
                    null,
                    "",
                    "",
                    null
                ]
            ],
            [
                [
                    null,
                    ""
                ],
                [
                    "Source: Jefef ries",
                    ""
                ]
            ],
            [
                [
                    null,
                    ""
                ],
                [
                    "Source: CLSA",
                    ""
                ]
            ],
            [
                [
                    null,
                    "",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    "Some of the data on the\ntable will shift post COV\nas numbers are update\nbut in India’s case we d\nestimate the numbers to\nshift much basis recent\ntraffic data."
                ],
                [
                    "",
                    "",
                    "",
                    "",
                    ""
                ],
                [
                    null,
                    "",
                    "",
                    "",
                    ""
                ],
                [
                    "",
                    "",
                    "",
                    "",
                    ""
                ],
                [
                    null,
                    "",
                    null,
                    "",
                    ""
                ],
                [
                    null,
                    null,
                    null,
                    "Source: Jefef ries, KPMG",
                    null
                ]
            ],
            [
                [
                    "",
                    "74"
                ]
            ],
            [
                [
                    "",
                    "75"
                ]
            ],
            [
                [
                    null,
                    "",
                    "India 1\n‘Mexico’",
                    "",
                    "~30m households\n~140m people\n~$15K per person",
                    "India1 is the consuming class, and effectively constitutes the\nmarket for most startups. Also most startups start here and\nthen expand to India2."
                ],
                [
                    null,
                    null,
                    "",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    "India 2\n‘Indonesia’*",
                    "The Aspirant\nClass",
                    "~70m households\n~300m people\n~$3k per person",
                    "India2 is the emerging aspirant class. They are heavy\nconsumers and reluctant payers. OTT / media, gaming,\nedtech and lending are relevant markets for them. UPI and\nAutoPay has unlocked small ticket spends and transactions\nfrom this group."
                ],
                [
                    null,
                    null,
                    "India 3\n‘Sub-Saharan Africa’",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    "Unmonetisable\nUsers\n(& Non-Users)",
                    "~205Mn households\n~1Bn people\n~$1k per person",
                    "India3 doesn’t have the kind of incomes to be able to spend\nanything on discretionary goods. They are beyond the pale,\nas of now, for startups."
                ],
                [
                    null,
                    null,
                    null,
                    "* Indonesia’s per capita income is $5k; strictly this is not the right country analogy for India2, but we couldn’t get a country that has a population of ~300m\nwith a per capita income of $3k. So please bear with us for this.",
                    null,
                    null
                ],
                [
                    "* Indonesia’s per capita income is $5k; strictly this is n\nSource: Blume Research with a per capita income of $3k. So please bear with u",
                    null,
                    null,
                    "* Indonesia’s per capita income is $5k; strictly this is n\nwith a per capita income of $3k. So please bear with u",
                    null,
                    null
                ]
            ],
            [
                [
                    "",
                    "76"
                ]
            ],
            [
                [
                    "",
                    "65 million",
                    ""
                ]
            ],
            [
                [
                    "",
                    null,
                    "35 million",
                    "",
                    null
                ],
                [
                    "",
                    "(Income > $25k)",
                    null,
                    null,
                    ""
                ]
            ],
            [
                [
                    "",
                    "40 million (Income > $10k)"
                ],
                [
                    "79 million (Income $5k - $10k)",
                    null
                ],
                [
                    "193 million\n(Income $2.5k - $5k )\n222 million\n(Income $1.5k - $2.5k)\n538 million\n(Income < $1.5k)",
                    null
                ]
            ],
            [
                [
                    "",
                    "77"
                ]
            ],
            [
                [
                    "",
                    "78"
                ]
            ],
            [
                [
                    "",
                    "79"
                ]
            ],
            [
                [
                    "segment motorcycles FY19 - FY23",
                    null,
                    null,
                    null,
                    "has doubled in last five years",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    "",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    ""
                ],
                [
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    ""
                ],
                [
                    "",
                    null,
                    null,
                    null,
                    "",
                    null,
                    null,
                    null
                ]
            ],
            [
                [
                    "",
                    "80"
                ]
            ],
            [
                [
                    null,
                    "4.5% CAGR",
                    null,
                    "",
                    null
                ],
                [
                    "",
                    "",
                    "",
                    "",
                    ""
                ],
                [
                    null,
                    "",
                    "",
                    "",
                    null
                ]
            ],
            [
                [
                    "",
                    "81"
                ]
            ],
            [
                [
                    "",
                    "82"
                ]
            ],
            [
                [
                    "Top 10%",
                    ""
                ]
            ],
            [
                [
                    "",
                    "83"
                ]
            ],
            [
                [
                    "",
                    "84"
                ]
            ],
            [
                [
                    null,
                    ""
                ],
                [
                    "Source: CEIC",
                    ""
                ]
            ],
            [
                [
                    null,
                    ""
                ],
                [
                    "Source: AMFI",
                    ""
                ]
            ],
            [
                [
                    null,
                    "",
                    null,
                    null,
                    "",
                    null,
                    null,
                    null,
                    null
                ],
                [
                    "",
                    "",
                    "",
                    "",
                    "",
                    null,
                    null,
                    "",
                    null
                ],
                [
                    null,
                    "",
                    null,
                    "",
                    "",
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    "Source: Jefef ries",
                    null,
                    "",
                    "",
                    null,
                    "85"
                ]
            ],
            [
                [
                    null,
                    "",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    "",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    "",
                    null
                ],
                [
                    "",
                    "",
                    "",
                    "",
                    ""
                ],
                [
                    null,
                    "",
                    null,
                    "",
                    null
                ],
                [
                    null,
                    "",
                    null,
                    null,
                    null
                ]
            ],
            [
                [
                    "",
                    "86"
                ]
            ],
            [
                [
                    "",
                    "87"
                ]
            ],
            [
                [
                    null,
                    "textiles and ayurveda, reinterpreting\nit for contemporary India.",
                    null,
                    "class products with an Indian soul and\naesthetic sensibility.",
                    null,
                    null
                ],
                [
                    "",
                    "",
                    "",
                    "",
                    "",
                    ""
                ],
                [
                    null,
                    "",
                    null,
                    "",
                    null,
                    null
                ]
            ],
            [
                [
                    "",
                    "88"
                ]
            ],
            [
                [
                    "",
                    "89"
                ]
            ],
            [
                [
                    null,
                    "community households is on a steady rise"
                ],
                [
                    "Source: MyGate, Redseer",
                    ""
                ]
            ],
            [
                [
                    "",
                    "90"
                ]
            ],
            [
                [
                    "",
                    "91"
                ]
            ],
            [
                [
                    "Source: Twitter / Ritesh Banglani & Anmol Maini 92",
                    null,
                    null
                ],
                [
                    "Source: Twitter / Ritesh Banglani & Anmol Maini",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "92"
                ]
            ],
            [
                [
                    "Indus Valley in one tweet\nUber was forced to make a change to its\ntraditional revenue model (commission on\nthe fare paid) for (3-wheeler) autos in\nIndia.\nNamma Yatri, an Indian startup leveraged\nthe open source Beckn protocol (part of\nIndia Stack / Digital Public Infra ) to build\na mobility solution where the revenue\nmodel was to charge a daily (or monthly)\nfee for drivers for the app, and not take a\nslice of the fare paid. The success of this\nmodel has forced all the other mobility\nplayers (Rapido, Ola, and now Uber to\nfollow suit).\nThe tweet shows how first-world revenue\nmodels have to adapt to the unique\nneeds of the Indian market, the rise of\nDPI, and DPI-native revenue models.\nSource: Twitter / Ashish Sinha 94",
                    null,
                    null
                ],
                [
                    "Source: Twitter / Ashish Sinha",
                    "",
                    "94"
                ]
            ],
            [
                [
                    "Indus Valley\nIndus Valley - Funding Trends\nVenture funding trends, and a deep dive, followed by a\nlook at India’s unicorns, and the venture debt market.\nIndus Valley - Funding Trends\nA deep dive into the Indian venture\nIPO Boom Pg 111\nmarket, including contrasts with China\nand USA, along with stage-wise funding\nSector Deep Dives Pg 120\nanalysis. We then do an analysis of\nunicorns, and attempt a count of the true\nIndus Valley Playbooks Pg 157\nnumber of unicorns. We wrap this with a\nloop at startups flipping back to India, to\nlist here, and finally, track the rise of\nventure debt.\n95",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "95"
                ]
            ],
            [
                [
                    "",
                    null,
                    null,
                    null
                ],
                [
                    "Venture Capital investments in startups over the last 5 years (in USD billion)",
                    null,
                    null,
                    null
                ],
                [
                    "",
                    null,
                    null,
                    null
                ],
                [
                    "",
                    null,
                    null,
                    null
                ],
                [
                    "Source: Dealroom",
                    "",
                    "",
                    "96"
                ]
            ],
            [
                [
                    "",
                    "97"
                ]
            ],
            [
                [
                    "India Venture Capital Investments (in USD billion)",
                    null,
                    null
                ],
                [
                    "Average number of rounds : 2,311 3,435 3,315 2,267 1,721\nSource: Tracxn\nTracxn updates the database continuously and hence the 2024 number may change in the future; still this snapshot should give you a directional sense of funding trends. Pls do note that each database may 98\npresent data difef rently depending on how they categorised certain transactions. You may see numbers difef r from chart to chart depending on the database; that said the broad trendline should hold!",
                    null,
                    null
                ],
                [
                    "Source: Tracxn\nTracxn updates the database continuously and hence the 2024 number may change in the future; still this snapshot should give you a directional sense of funding trends. Pls do note that each database may\npresent data difef rently depending on how they categorised certain transactions. You may see numbers difef r from chart to chart depending on the database; that said the broad trendline should hold!",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "98"
                ]
            ],
            [
                [
                    "A stage-wise analysis of India's VC Market",
                    "",
                    ""
                ],
                [
                    "2024 mirrors 2023 patterns: Seed saw a small drop, Early and Late stages show modest gains but far below peak levels",
                    null,
                    null
                ]
            ],
            [
                [
                    "How Seed, Early, and Late Stage financing stacks up (in USD billion)",
                    null,
                    null,
                    null
                ],
                [
                    "",
                    null,
                    "",
                    null
                ],
                [
                    null,
                    "",
                    "",
                    ""
                ],
                [
                    null,
                    null,
                    "",
                    null
                ],
                [
                    null,
                    "",
                    "",
                    ""
                ],
                [
                    null,
                    null,
                    "",
                    null
                ],
                [
                    "Source: Tracxn",
                    null,
                    "",
                    null
                ]
            ],
            [
                [
                    "",
                    "99"
                ]
            ],
            [
                [
                    "",
                    "100"
                ]
            ],
            [
                [
                    "",
                    "101"
                ]
            ],
            [
                [
                    "",
                    "102"
                ]
            ],
            [
                [
                    "Time between rounds: Seed vs multistage fund-backed startups",
                    ""
                ],
                [
                    "Startups backed by seed funds taking longer to raise follow-on rounds as compared to ones backed by multistage funds",
                    null
                ]
            ],
            [
                [
                    "",
                    "103"
                ]
            ],
            [
                [
                    "",
                    "104"
                ]
            ],
            [
                [
                    "",
                    "105"
                ]
            ],
            [
                [
                    "",
                    "Founder Owned",
                    "(3)"
                ],
                [
                    "",
                    "",
                    ""
                ],
                [
                    null,
                    "Acquired (7)",
                    ""
                ],
                [
                    "",
                    null,
                    null
                ],
                [
                    "Publicly Listed\n(14)",
                    null,
                    null
                ]
            ],
            [
                [
                    "Greater than\n$1Bn",
                    "",
                    "Less than\n$1Bn"
                ]
            ],
            [
                [
                    "Greater than\n$1Bn",
                    ""
                ]
            ],
            [
                [
                    "",
                    "106"
                ]
            ],
            [
                [
                    null,
                    "Phonepe tax bill would make it the 10th\nhighest tax paying company in India in\nFY23",
                    null
                ],
                [
                    null,
                    "",
                    ""
                ],
                [
                    "Even more are in the process of reshoring",
                    "",
                    null
                ]
            ],
            [
                [
                    "Company",
                    "Tax Paid"
                ],
                [
                    "Phonepe",
                    "$1 Bn"
                ],
                [
                    "Groww",
                    "$160 Mn"
                ],
                [
                    "Razorpay",
                    "$200 Mn"
                ],
                [
                    "Zepto",
                    "Undisclosed"
                ]
            ],
            [
                [
                    "",
                    "107"
                ]
            ],
            [
                [
                    null,
                    "Difficulty in raising capital domestically",
                    null,
                    "Planned to list on the US public market",
                    null
                ],
                [
                    "",
                    "",
                    "",
                    "",
                    ""
                ],
                [
                    null,
                    "",
                    "",
                    "",
                    null
                ],
                [
                    "",
                    "",
                    "",
                    "",
                    ""
                ],
                [
                    null,
                    "",
                    null,
                    "",
                    null
                ]
            ],
            [
                [
                    "",
                    "108"
                ]
            ],
            [
                [
                    "",
                    "➔ Higher Liquidation Preference: Venture debt typically comes with priority claims on company assets and cash flows, over equity holders"
                ]
            ],
            [
                [
                    "",
                    "weaken\n➔ Risk of Negative Cycle: As equity funding becomes harder to secure, venture debt capacity may shrink exactly when companies need it most."
                ]
            ],
            [
                [
                    "",
                    "109"
                ]
            ],
            [
                [
                    null,
                    "initiative",
                    null,
                    null
                ],
                [
                    "",
                    "",
                    "",
                    ""
                ]
            ],
            [
                [
                    "",
                    "110"
                ]
            ],
            [
                [
                    "Indus Valley\nIndus Valley - Funding Trends Pg 95\nIPO Boom\nIPO Boom\nA deep dive into India's booming IPO market, as well as\nthe SME IPO’s rise, including what it implies for A deep-dive into India’s record-breaking\nfounders.\nIPO market, looking at the performance\nof IPOs, exploring how barriers to list are\nSector Deep Dives Pg 120\ncoming down, as well as the rise of the\nSME IPO Market.\nIndus Valley Playbooks Pg 157\n111",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "111"
                ]
            ],
            [
                [
                    "",
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "",
                    "",
                    ""
                ],
                [
                    null,
                    "(Japan)",
                    "(Hong Kong",
                    ")",
                    "(Shanghai)"
                ]
            ],
            [
                [
                    "",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    ""
                ],
                [
                    null,
                    "(India)",
                    "(US)",
                    "(U",
                    "S) (H",
                    "ong Kon",
                    "g) (",
                    null
                ]
            ],
            [
                [
                    "",
                    "112"
                ]
            ],
            [
                [
                    "",
                    "113"
                ]
            ],
            [
                [
                    "Market cap data as on 17th January 2025 via NSE. The number of venture funded IPOs here includes post-IPO VC funding. The number includes 3 VC funded companies listed\nabroad - Freshworks, ReNew, and MakeMyTrip. The IPO list was taken from Tracxn. This number includes a total of 14 VC funded SME IPOs.",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "114"
                ]
            ],
            [
                [
                    "",
                    "115"
                ]
            ],
            [
                [
                    "",
                    "116"
                ]
            ],
            [
                [
                    "",
                    ""
                ],
                [
                    "+₹3 Bn\nMarket Cap",
                    null
                ]
            ],
            [
                [
                    "",
                    "117"
                ]
            ],
            [
                [
                    "",
                    "118"
                ]
            ],
            [
                [
                    "Guideline for founders mulling over an SME IPO",
                    ""
                ]
            ],
            [
                [
                    "",
                    "119"
                ]
            ],
            [
                [
                    "Indus Valley\nIndus Valley - Funding Trends Pg 95\nQuick Commerce\nIPO Boom Pg 111\nSector Deep Dives A detailed analysis of the Quick\nCommerce market, its growth, why it\n➔ Quick Commerce: Why it works in India, the\nworks in India, what the vectors of its\nimplications of its rise, and is there irrational\nexuberance re Quick Commerce? growth are, the implications of its rise,\n➔ AI: Is India getting a foundational model soon? and whether there is ‘irrational\nexuberance’ about its prospects?\nIndus Valley Playbooks Pg 157\n120",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "120"
                ]
            ],
            [
                [
                    "",
                    null
                ],
                [
                    "A detailed analysis of the Quick\nCommerce market, its growth, why it\nworks in India, what the vectors of its\ngrowth are, the implications of its rise,\nand whether there is ‘irrational\nexuberance’ about its prospects?",
                    ""
                ],
                [
                    "",
                    null
                ]
            ],
            [
                [
                    "",
                    "121"
                ]
            ],
            [
                [
                    "",
                    "122"
                ]
            ],
            [
                [
                    "",
                    "123"
                ]
            ],
            [
                [
                    "",
                    "124"
                ]
            ],
            [
                [
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    "",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    "Sources for\n₹131 revenue",
                    null,
                    null,
                    null,
                    null,
                    null,
                    "C\n=",
                    "C",
                    null,
                    "ost Breakup\n₹131",
                    null,
                    null,
                    "of"
                ],
                [
                    null,
                    "",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    "",
                    null,
                    null,
                    null
                ],
                [
                    "",
                    "",
                    "",
                    null,
                    "User Fee ₹11",
                    "",
                    null,
                    null,
                    null,
                    null,
                    "Discounts ₹5",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    "",
                    null,
                    null,
                    null,
                    null,
                    null,
                    "Delivery Costs",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    "₹35",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    "",
                    "=",
                    null,
                    null,
                    "",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    "Other Variable\nCosts\n₹61",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    "",
                    "Commission &\nAd Revenue\n₹120",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    "",
                    null,
                    null,
                    null,
                    null,
                    null,
                    "",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    "",
                    null,
                    null,
                    null,
                    ""
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    "",
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    "",
                    "+",
                    "",
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    "",
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    "",
                    null,
                    null
                ]
            ],
            [
                [
                    "Metrics",
                    "FY25E"
                ],
                [
                    "GOV",
                    "₹27,867 Cr"
                ],
                [
                    "% yoy",
                    "123.50%"
                ],
                [
                    "Average MTUs",
                    "9.6 Mn"
                ],
                [
                    "AOV",
                    "₹674"
                ],
                [
                    "Orders",
                    "413 Mn"
                ],
                [
                    "Implied Take Rates",
                    "19.50%"
                ],
                [
                    "Adjusted Revenue",
                    "₹5,420 Cr"
                ],
                [
                    "Contribution Margin\n(as % of GOV)",
                    "4.00%"
                ],
                [
                    "Adjusted EBITDA",
                    "(₹33 Cr)"
                ],
                [
                    "% margin on GOV",
                    "(0.10%)"
                ]
            ],
            [
                [
                    "",
                    "Blinkit Revenue",
                    null,
                    null,
                    null,
                    null,
                    null,
                    ""
                ],
                [
                    null,
                    "",
                    "Blinkit Revenue",
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    "",
                    null,
                    "19.5%",
                    "(",
                    "₹131)",
                    "",
                    null
                ]
            ],
            [
                [
                    "₹",
                    "35"
                ]
            ],
            [
                [
                    "",
                    "125"
                ]
            ],
            [
                [
                    "Why?\nIndia has low car ownership Houses are smaller than in other nations\nWith lack of cars and small houses (lesser storage) - people prefer to shop",
                    null,
                    null
                ],
                [
                    null,
                    "With lack of cars and small houses (lesser storage) - people prefer to shop",
                    null
                ],
                [
                    "",
                    "locally as they cannot go long distance and also not stock up on items",
                    ""
                ],
                [
                    "",
                    "",
                    null
                ]
            ],
            [
                [
                    "",
                    "126"
                ]
            ],
            [
                [
                    "",
                    "127"
                ]
            ],
            [
                [
                    "",
                    "128"
                ]
            ],
            [
                [
                    "",
                    "129"
                ]
            ],
            [
                [
                    null,
                    "",
                    null
                ],
                [
                    null,
                    "",
                    null
                ],
                [
                    null,
                    "",
                    null
                ],
                [
                    "",
                    "",
                    ""
                ],
                [
                    null,
                    "",
                    null
                ]
            ],
            [
                [
                    "",
                    "130"
                ]
            ],
            [
                [
                    "",
                    "131"
                ]
            ],
            [
                [
                    null,
                    "Operating via cloud kitchens situated within dark stores allows them to\nincrease their Average Order Value and margins while utilizing their\nexisting infrastructure and avoiding commission payments to",
                    null,
                    null,
                    "In Nov’24 Zepto Cafe was present in 15% of its dark stores, whereas\nnow it is available in more than 50% of dark stores.",
                    null
                ],
                [
                    "",
                    "intermediaries.",
                    "",
                    "",
                    "",
                    ""
                ]
            ],
            [
                [
                    "",
                    "132"
                ]
            ],
            [
                [
                    "",
                    "133"
                ]
            ],
            [
                [
                    null,
                    "Quick Commerce for Home Services\nSnabbit\nHouse help in minutes",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    null,
                    "Slikk\n60-Min Fashion delivery",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    "",
                    null,
                    null,
                    null,
                    "",
                    null,
                    null,
                    null,
                    "",
                    null
                ],
                [
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    ""
                ],
                [
                    null,
                    "",
                    null,
                    null,
                    null,
                    "",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ]
            ],
            [
                [
                    "",
                    "134"
                ]
            ],
            [
                [
                    null,
                    "1 Flipkart has entered Quick Commerce",
                    null,
                    "2 Amazon has plans to follow",
                    null,
                    "3 Other players are taking notice too"
                ],
                [
                    "",
                    "",
                    "",
                    "",
                    "",
                    ""
                ],
                [
                    null,
                    "",
                    null,
                    "",
                    null,
                    ""
                ]
            ],
            [
                [
                    "",
                    "135"
                ]
            ],
            [
                [
                    "",
                    "136"
                ]
            ],
            [
                [
                    "",
                    "137"
                ]
            ],
            [
                [
                    "",
                    "138"
                ]
            ],
            [
                [
                    "For one Bengaluru-based engineer, his response to\na recent craving for a soft drink made him realise\njust how much quick commerce had reshaped his\nbehaviour. “I randomly order some juice because I\nhave access,” he says. “Earlier, I used to open the\nfridge. Now, I open Instamart, which is like an\nevolved version of checking the fridge.”",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    null
                ],
                [
                    "",
                    "",
                    ""
                ]
            ],
            [
                [
                    "",
                    "139"
                ]
            ],
            [
                [
                    null,
                    "",
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    null,
                    "Trade promotions by FMCG players are\nabsent.\nPreviously, retailers could earn major\nincentives like washing machines for\nmeeting targets - these volume-based\nrewards are now rare.\nMargins on branded products have\ndropped significantly.\nFor instance, biscuit category margins\nhave fallen from 22% to 7-8%, severely\nimpacting retailer profits.\nWeakened demand has forced retailers\nto abandon bulk purchasing in favor of\nsmaller, frequent orders.\nThis shift further reduces margins as they\nlose bulk buying benefits."
                ],
                [
                    null,
                    null,
                    null,
                    "Kirana stores don’t have enough options (SKUs) for brand\nconscious customers. And with free delivery as well as the",
                    null,
                    null
                ],
                [
                    null,
                    "Insights are from an interview with a\nshop owner who has been in\nbusiness for 30 years, currently\noperating in a middle-class\nneighborhood of urban Bangalore.",
                    null,
                    null,
                    null,
                    null
                ],
                [
                    "",
                    "",
                    "",
                    "discounts that QCom offers, online works out cheaper.",
                    "",
                    ""
                ]
            ],
            [
                [
                    "",
                    "140"
                ]
            ],
            [
                [
                    "Brands find it hard to list on Quick Commerce platforms",
                    null,
                    "Dark patterns have started to emerge on the apps",
                    null
                ],
                [
                    "",
                    "",
                    "",
                    ""
                ]
            ],
            [
                [
                    "",
                    "141"
                ]
            ],
            [
                [
                    "",
                    "142"
                ]
            ],
            [
                [
                    "",
                    "143"
                ]
            ],
            [
                [
                    "",
                    "144"
                ]
            ],
            [
                [
                    null,
                    null,
                    "",
                    null
                ],
                [
                    null,
                    null,
                    null,
                    "Added to that is that Orders per Dark Store have\nstabilised. Given this, and the diminishing returns\nof expanding Dark Stores beyond certain areas,\nthe aggressive projections of total orders seem\na tad unrealistic. (80% of Blinkit’s sales come\nfrom the top 8 cities per Albinder (3QFY25\nanalyst call transcript)."
                ],
                [
                    "",
                    "",
                    "",
                    ""
                ],
                [
                    null,
                    null,
                    "",
                    null
                ]
            ],
            [
                [
                    "",
                    "145"
                ]
            ],
            [
                [
                    "",
                    "146"
                ]
            ],
            [
                [
                    "",
                    "147"
                ]
            ],
            [
                [
                    "Indus Valley\nIndus Valley - Funding Trends Pg 95\nAI: Is India getting a\nIPO Boom Pg 111\nfoundational model\nSector Deep Dives\nsoon?\n➔ Quick Commerce: Why it works in India, the\nimplications of its rise, and is there irrational\nWhy China, not India had a DeepSeek\nexuberance re QCom?\nmoment, and whether the recent\n➔ AI: Is India getting a foundational model\nsoon? enthusiasm and initiatives could spur the\ncreation of a foundational model?\nIndus Valley Playbooks Pg 157\n148",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "148"
                ]
            ],
            [
                [
                    null,
                    "…",
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    "",
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    "",
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    "",
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    "…",
                    null,
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    "",
                    null,
                    "",
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    "",
                    "",
                    "",
                    null
                ],
                [
                    "",
                    "",
                    null,
                    "",
                    null,
                    null,
                    ""
                ]
            ],
            [
                [
                    "",
                    "149"
                ]
            ],
            [
                [
                    null,
                    "Pre-DeepSeek default mode",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    ""
                ],
                [
                    null,
                    "",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ]
            ],
            [
                [
                    "",
                    "150"
                ]
            ],
            [
                [
                    "",
                    "151"
                ]
            ],
            [
                [
                    "…",
                    null,
                    null,
                    "",
                    "",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    "The forcing functions that created DeepSeek\nChina being the base for 1/8th of World’s top\n1\nAI researchers (India has none)\nChina has been continuously investing in\n2\nand improving in AI. The Australian Strategic\nPolicy Institute identified that China led in\njust three of 64 critical technologies in the\nyears from 2003 to 2007, but is the leading\ncountry in 57 of 64 technologies over the\npast five years from 2019 to 2023.\nConstraints breed creativity - the challenges\nin accessing GPUs led them to approaches\n3 and tech minimising GPU use\nCrackdown on the finance industry leading\nto the hedge fund High-Flyer deciding to\n4\nredirect its attention towards AI tech, away\nfrom Finance. They also managed to access\ncapital (Govt support?) to undertake the\n$1.6b+ investment to develop the same",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    null,
                    "China being the base for 1/8th of World’s top\nAI researchers (India has none)\nChina has been continuously investing in\nand improving in AI. The Australian Strategic\nPolicy Institute identified that China led in\njust three of 64 critical technologies in the\nyears from 2003 to 2007, but is the leading\ncountry in 57 of 64 technologies over the\npast five years from 2019 to 2023.\nConstraints breed creativity - the challenges\nin accessing GPUs led them to approaches\nand tech minimising GPU use\nCrackdown on the finance industry leading\nto the hedge fund High-Flyer deciding to\nredirect its attention towards AI tech, away\nfrom Finance. They also managed to access\ncapital (Govt support?) to undertake the\n$1.6b+ investment to develop the same",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    null,
                    null,
                    null,
                    null,
                    null,
                    null
                ],
                [
                    "",
                    "",
                    "",
                    "",
                    "",
                    "($1.6b via Semi Analysis)",
                    "",
                    ""
                ],
                [
                    "",
                    "",
                    null,
                    "",
                    "",
                    null,
                    null,
                    null
                ]
            ],
            [
                [
                    "",
                    "152"
                ]
            ],
            [
                [
                    "",
                    "153"
                ]
            ],
            [
                [
                    "Expenditure on Aadhaar (in INR crore)\nYear Amount\n2009-10 ₹26.2 Cr\n2010-11 ₹268.4 Cr\n2011-12 ₹1,187.5 Cr\n2012-13 ₹1,338.7 Cr\n2013-14 ₹1,544.4 Cr\n2014-15 ₹1,615.3 Cr\n2015-16 ₹1680.4 Cr\n2016-17 ₹1132.8 Cr\nWith just over $1b spend, India had onboarded a billion people to the\nAadhar identity initiative; resulting in annual savings of over a billion!",
                    null,
                    null,
                    null,
                    "ISRO is consistently cited as having pioneered the frugal approach to\nspace exploration, cheaper than Hollywood space movies even!",
                    null,
                    null
                ],
                [
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    ""
                ],
                [
                    "",
                    null,
                    null,
                    null,
                    "",
                    null,
                    null
                ]
            ],
            [
                [
                    "Year",
                    "Amount"
                ],
                [
                    "2009-10",
                    "₹26.2 Cr"
                ],
                [
                    "2010-11",
                    "₹268.4 Cr"
                ],
                [
                    "2011-12",
                    "₹1,187.5 Cr"
                ],
                [
                    "2012-13",
                    "₹1,338.7 Cr"
                ],
                [
                    "2013-14",
                    "₹1,544.4 Cr"
                ],
                [
                    "2014-15",
                    "₹1,615.3 Cr"
                ],
                [
                    "2015-16",
                    "₹1680.4 Cr"
                ],
                [
                    "2016-17",
                    "₹1132.8 Cr"
                ]
            ],
            [
                [
                    "₹",
                    "26.2 Cr"
                ]
            ],
            [
                [
                    "₹",
                    "268.4 Cr"
                ]
            ],
            [
                [
                    "₹",
                    "1,187.5 Cr"
                ]
            ],
            [
                [
                    "₹",
                    "1,338.7 Cr"
                ]
            ],
            [
                [
                    "₹",
                    "1,544.4 Cr"
                ]
            ],
            [
                [
                    "₹",
                    "1,615.3 Cr"
                ]
            ],
            [
                [
                    "₹",
                    "1680.4 Cr"
                ]
            ],
            [
                [
                    "₹",
                    "1132.8 Cr"
                ]
            ],
            [
                [
                    "",
                    "154"
                ]
            ],
            [
                [
                    "",
                    "155"
                ]
            ],
            [
                [
                    null,
                    "Video generation via prompts leveraging OpenAI\n“4 million MAUs creating 7 million videos a month” - OpenAI",
                    "",
                    ""
                ],
                [
                    "",
                    "",
                    null,
                    null
                ]
            ],
            [
                [
                    "",
                    "156"
                ]
            ],
            [
                [
                    "Indus Valley\nIndus Valley - Funding Trends Pg 95\nThe various India2\nIPO Boom Pg 111\nPlaybooks.\nSector Deep Dives Pg 120\nHistoric playbooks contrasted with the\nEvolved and Emerging playbooks,\nIndus Valley Playbooks\nfollowed by case studies of STAGE,\n➔ The various India2 Playbooks. Kaleidofin, and Voice Club. Why voice,\n➔ How Indus Valley influenced Indian advertising. and microtransactions are two killer\n➔ Returns, and how Indian startups are addressing\nfeatures of the Emerging playbook.\nit.\n➔ Marketing framework for the Indian diaspora or\nIndia0.\n157",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "157"
                ]
            ],
            [
                [
                    "2020 Onwards",
                    "Re-e\nand us"
                ]
            ],
            [
                [
                    "",
                    "158"
                ]
            ],
            [
                [
                    "",
                    "159"
                ]
            ],
            [
                [
                    null,
                    "How STAGE engineers ultra low-cost content"
                ],
                [
                    null,
                    ""
                ],
                [
                    "➔ Standardized set of story tropes and templates re-scripted for different languages, designed for low-cost shooting\n(e.g., mostly small sets scripted into storyline).\n➔ Work with local content creators who don’t have access to other mainstream outlets willing to work for low costs.\n➔ Significant amount of pre-planning prior to shoot enabling quick turnarounds.",
                    ""
                ]
            ],
            [
                [
                    null,
                    null,
                    null,
                    null,
                    ""
                ],
                [
                    null,
                    null,
                    "",
                    null,
                    ""
                ],
                [
                    "Lower\nBudgets\nPer Film",
                    null,
                    "",
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    ""
                ],
                [
                    null,
                    "",
                    "",
                    null,
                    ""
                ],
                [
                    null,
                    "",
                    "",
                    null,
                    null
                ],
                [
                    null,
                    "+",
                    null,
                    null,
                    ""
                ],
                [
                    null,
                    null,
                    null,
                    "",
                    ""
                ],
                [
                    null,
                    null,
                    null,
                    "",
                    null
                ],
                [
                    "Faster\nShoots\nPer Film",
                    null,
                    null,
                    "",
                    null
                ],
                [
                    null,
                    null,
                    null,
                    "",
                    ""
                ],
                [
                    null,
                    "",
                    null,
                    "",
                    null
                ],
                [
                    null,
                    "+",
                    null,
                    null,
                    ""
                ],
                [
                    "Highly\nRated",
                    "",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    null,
                    null,
                    null,
                    ""
                ]
            ],
            [
                [
                    "=",
                    ""
                ]
            ],
            [
                [
                    "",
                    "160"
                ]
            ],
            [
                [
                    "How",
                    "Kaleidofin r",
                    null,
                    "eengineered the credit rating product for India2 / India3"
                ],
                [
                    "",
                    null,
                    null,
                    null
                ],
                [
                    "",
                    null,
                    "",
                    null
                ]
            ],
            [
                [
                    "Category",
                    "PAR 90 %"
                ],
                [
                    "ki score accept + cb accept",
                    "1.53%"
                ],
                [
                    "ki score accept + cb reject",
                    "2.51%"
                ],
                [
                    "ki score reject + cb accept",
                    "4.44%"
                ],
                [
                    "ki score reject + cb reject",
                    "7.68%"
                ]
            ],
            [
                [
                    "",
                    "161"
                ]
            ],
            [
                [
                    "India 1",
                    "",
                    "India 2"
                ]
            ],
            [
                [
                    "",
                    "162"
                ]
            ],
            [
                [
                    null,
                    "FRND, AstroTalk, InstaAstro, Clarity all have 1:1 voice as a key revenue model. India2 (and many India1) users are willing to pay to talk to a stranger\n(expert or member of the opposite sex). The success of this model is attracting apps with a tangential interest in the space (e.g., Lokal) to explore\nthis revenue opportunity.",
                    null,
                    null,
                    null
                ],
                [
                    "Source: Voice Club",
                    null,
                    "",
                    "",
                    "163"
                ]
            ],
            [
                [
                    "",
                    "164"
                ]
            ],
            [
                [
                    "Indus Valley\nIndus Valley - Funding Trends Pg 95\nHow Indus Valley\nIPO Boom Pg 111\ninfluenced Indian\nSector Deep Dives Pg 120\nadvertising.\nIndus Valley Playbooks\nHow Indus Valley rethought the celebrity\nad to generate shock value, and how it\n➔ The various India2 Playbooks.\n➔ How Indus Valley influenced Indian has shaped the Indian advertising\nadvertising. market. We also look at the currency of\n➔ Returns, and how Indian startups are addressing\ntrust-building is diverging between India1\nit.\n➔ Marketing framework for the Indian diaspora or and India2 resulting in distinct\nIndia0.\ncommunication templates.\n165",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "165"
                ]
            ],
            [
                [
                    null,
                    "How Indus Valley pioneered a new ad trope"
                ],
                [
                    null,
                    "Humanising celebrities, making fun of them, was a new addition to the Indian ad oeuvre. Legacy brands historically kept the\ncelebrity on a near pedestal (with some exceptions)."
                ],
                [
                    "celebrity on a near pedestal (with some exceptions).\n➔ What is common to these ads is that their makers are ex-members of AIB (All India Bakchod) a comedy collective that melted down in the\n2018 #metoo wave. Key members include Tanmay Bhatt, Devaiah Bopanna, Vishal Dayama etc. [Tanmay + Devaiah also work together as\nMoonshot.]\n➔ They pitched legacy brands who hesitated to sign them given their lack of big agency experience; Startups however found a perfect match in\nthem especially given the comedians’ ability to create attention and shock value by depicting celebrities in a never before light, cutting\nthrough clutter.",
                    "celebrity on a near pedestal (with some exceptions)."
                ]
            ],
            [
                [
                    "This and the following slides in this section benefited significantly from inputs gathered during a conversation with Karthik Srinivasan, a leading ad / marketing guru (x.com/beastoftraal).\nI also enjoyed speaking with Arun Iyer (x.com/aruniyer), a seasoned adman who co-founded and is Partner at Spring Marketing Capital.",
                    null,
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "",
                    "166"
                ]
            ],
            [
                [
                    "",
                    "167"
                ]
            ],
            [
                [
                    "",
                    "168"
                ]
            ],
            [
                [
                    "",
                    "The currency of trust-building is also diverging between India1",
                    ""
                ],
                [
                    "and India2",
                    null,
                    null
                ],
                [
                    "",
                    null,
                    null
                ],
                [
                    "How trust is mediated through communication is diverging between India1 and India2.",
                    null,
                    null
                ]
            ],
            [
                [
                    "",
                    "169"
                ]
            ],
            [
                [
                    "Indus Valley\nIndus Valley - Funding Trends Pg 95\nReturns, and how\nIPO Boom Pg 111\nIndian startups are\nSector Deep Dives Pg 120\naddressing it.\nIndus Valley Playbooks\nIndian startups in the consumer space,\n➔\n➔ The various India2 Playbooks. especially apparel and footwear brands,\n➔ How Indus Valley influenced Indian advertising. have a returns issue. We analyse trends\n➔ Returns, and how Indian startups are\nand suggest playbooks that Brands are\naddressing it.\n➔ Marketing framework for the Indian diaspora or adopting / can adopt to overcome these\nIndia0.\nchallenges.\n170",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "170"
                ]
            ],
            [
                [
                    "",
                    "171"
                ]
            ],
            [
                [
                    "",
                    null
                ],
                [
                    "",
                    ""
                ],
                [
                    "",
                    null
                ]
            ],
            [
                [
                    "",
                    "Own\nWebsite",
                    "Marketplaces"
                ],
                [
                    "RTO",
                    "10%",
                    "9%"
                ],
                [
                    "RTV",
                    "14%",
                    "39%"
                ],
                [
                    "Total Returns",
                    "24%",
                    "48%"
                ]
            ],
            [
                [
                    "",
                    "172"
                ]
            ],
            [
                [
                    "",
                    "173"
                ]
            ],
            [
                [
                    "",
                    "174"
                ]
            ],
            [
                [
                    "",
                    "an eCommerce enabler brand providing smart checkout and COD-enabler solutions shared data on how COD"
                ]
            ],
            [
                [
                    "",
                    "175"
                ]
            ],
            [
                [
                    "“Poor addresses cost",
                    null
                ],
                [
                    "India $10 - 14 billion",
                    ""
                ],
                [
                    "annually, ~0.5% of the",
                    null
                ],
                [
                    "GDP.”",
                    null
                ]
            ],
            [
                [
                    "-",
                    "Dr Santanu Bhattacharya",
                    ",",
                    ""
                ],
                [
                    null,
                    "MIT Media Lab",
                    null,
                    null
                ]
            ],
            [
                [
                    "",
                    "176"
                ]
            ],
            [
                [
                    "",
                    null
                ],
                [
                    "These are 2 interesting demand-side solutions that tackle the\nproblem on the customer’s end (as compiled by Dharmesh Ba)\n● Add a video guide (Bharat Agri)",
                    ""
                ],
                [
                    "● Add a pic of your front door (Swiggy)",
                    null
                ]
            ],
            [
                [
                    "Source: Dharmesh Ba / The India Notes, Delhivery, and GoKwik",
                    "",
                    "",
                    "177"
                ]
            ],
            [
                [
                    null,
                    "How brands are attacking RTV (Return to Vendor)",
                    null
                ],
                [
                    "",
                    "Ultimately the only way to address this is through better fits (the biggest reason for RTB. However, two interesting playbooks",
                    ""
                ],
                [
                    null,
                    "are shown below",
                    ""
                ]
            ],
            [
                [
                    "",
                    "178"
                ]
            ],
            [
                [
                    "Indus Valley\nIndus Valley - Funding Trends Pg 95\nMarketing framework\nIPO Boom Pg 111\nfor the Indian diaspora\nSector Deep Dives Pg 120\nor India0.\nIndus Valley Playbooks\nNo report is complete without a 2x2. Here\n➔\n➔ The various India2 Playbooks. is our framework for how brands can\n➔ How Indus Valley influenced Indian advertising. position themselves for the Indian\n➔ Returns, and how Indian startups are addressing\ndiaspora (or India0) basis affluence and\nit.\n➔ Marketing framework for the Indian diaspora affiliation (or affinity). We give example of\nor India0.\nstrategies / playbooks for three of the\nfour quadrants.\n179",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "179"
                ]
            ],
            [
                [
                    null,
                    "Canada\n2.8 Mn"
                ],
                [
                    "USA\n5.4 Mn",
                    ""
                ]
            ],
            [
                [
                    "Saudi Arabia\n2.5 Mn",
                    "Saudi Arabia",
                    null,
                    null,
                    null,
                    ""
                ],
                [
                    null,
                    null,
                    "2.5 M",
                    "n",
                    "",
                    null
                ]
            ],
            [
                [
                    "",
                    "Myanma",
                    "r"
                ]
            ],
            [
                [
                    "",
                    "180"
                ]
            ],
            [
                [
                    "",
                    "181"
                ]
            ],
            [
                [
                    "",
                    null,
                    null
                ],
                [
                    "182",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "182"
                ]
            ],
            [
                [
                    "",
                    "183"
                ]
            ],
            [
                [
                    "",
                    "184"
                ]
            ],
            [
                [
                    "",
                    null,
                    null
                ],
                [
                    "",
                    "",
                    "185"
                ]
            ],
            [
                [
                    "Acknowledgements\nAs with all reports, this too rests on the labour of several analysts, researchers and writers whose work we used to\nbuild on. We stand on the shoulders of giants. We have acknowledged the sources and their contributions on each\nof the pages; in particular, a shout out to Jefferies, Bernstein, Goldman, Redseer, UBS, CRIF, Barclays, Nuvama,\nCLSA, Tracxn, for their regular reports enabling greater access to data, and enhancing our understanding of the\nIndian startup ecosystem. We also acknowledge the inputs and insights of Rahul Mathur, Dharmesh Ba, Arindam\nPaul and other astute observers of the Indian startup ecosystem - thank you for your openness in explaining the\nworld from your perspective, and sharing insights that inform this report. This time we also had the participation of\nseveral startups such as Delhivery, GoKwik, MyGate, Stage, Kaleidofin, Salty, Inde Wild, VoiceClub etc., who\nhelped us with their proprietary data sets that we were able to analyse and draw insights from. We thank them\nprofusely for this support!\nFinally, we would also like to thank the wider Blume team, especially Joseph Sebastian, for their inputs.\nAm sure I have possibly left out a lot more names! Apologies in advance for the same!\n- Sajith, Anurag, Nachammai & Dhruv\n186",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "186"
                ]
            ],
            [
                [
                    "About Blume Ventures\nBlume Ventures is an early stage venture firm based across Mumbai, Bangalore, Delhi and San Francisco, that\nprovides ‘conviction capital’ to founders across India consumer internet as well as software & enterprise technology.\nWe add value through a platform approach – over 85 specialists across shared CFO services, legal advisory, talent\nacquisition, capital raising, GTM enablement, operations support – who focus entirely on supporting portfolio\ncompanies and helping founders learn, thereby greatly improving their chances of success. Our value-added\napproach has helped us retain board representation in the vast majority of our top companies; with an overall Asset\nunder Management (AUM) upwards of $650M.\nYou can read more about us at blume.vc\n187",
                    null,
                    null
                ],
                [
                    null,
                    "",
                    "187"
                ]
            ]
        ],
        "total_pages": 188
    },
    "file_type": "pdf",
    "filename": "Indus Valley Annual Report 2025.pdf",
    "success": true
}


---

### Frontend

```bash
# In a separate terminal, enter the frontend folder
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

Frontend runs at `http://localhost:3001`

The Vite dev server proxies all `/api/*` requests to `http://127.0.0.1:5000`, so no CORS issues during development. Both servers must be running at the same time.

---

## Using the Tool

**Upload screen** — drag and drop a `.pdf` or `.docx` file, or click to browse. Once a file is selected, click "Analyze document". The UI shows live step progress:

```
Parsing document...  →  Extracting metrics...  →  Running AI analysis...
```

**Results dashboard** — the readiness banner at the top answers the core question immediately. The colour tells you the verdict at a glance: green for ready, amber for minor fixes needed, red for major rework. Everything below provides the supporting detail.

The dashboard has three tabs:

- **Overview** — readiness score (ring chart), migration effort by content type (bar chart), blockers and warnings, AI content analysis key-values, and visual content assessment
- **Content Debt** — table of undefined acronyms with suggested actions, outdated references, unresolved placeholders
- **Raw JSON** — the full API response with syntax highlighting and a one-click copy button

The action bar at the bottom lets you export the complete report as a JSON file or start a new analysis.

---

## API Endpoints

### Main — `POST /api/report`

The single endpoint the frontend calls. Runs parsing, metrics, and AI analysis in one request and returns everything merged.

```bash
curl -X POST -F "file=@your-document.pdf" http://127.0.0.1:5000/api/report
```

```json
{
  "success": true,
  "report_id": "e2c0da7af1db",
  "summary": {
    "filename": "product-guide.pdf",
    "readiness_grade": "C",
    "readiness_score": 65,
    "status_label": "Major rework required",
    "auto_migratable": false,
    "overall_effort": "High",
    "person_days": 2.5,
    "blocker_count": 2,
    "top_blockers": [
      "16 broken links detected — must be fixed before migration",
      "2 complex tables (>6 cols or >20 rows) — need restructuring"
    ],
    "warning_count": 1,
    "top_warnings": [
      "Long paragraphs (avg 93 words) — consider splitting"
    ]
  },
  "metrics": { "...full metrics dict..." },
  "analysis": { "...full AI analysis dict..." }
}
```



---

### Supporting endpoints

| Endpoint | What it does |
|---|---|
| `POST /api/parse` | Extract raw structure — headings, paragraphs, tables, images |
| `POST /api/metrics` | Metrics extraction only, no AI call, fast |
| `POST /api/analyze` | AI analysis only |
| `GET /api/report` | Feeds UI with all other three routes |
| `GET /api/health` | Check server and Groq API status |

---

## Metrics Extracted

The five metrics the task requires, plus bonus fields relevant to Document360 migration:

| Metric | Required / Bonus | Why it matters for migration |
|---|---|---|
| Word count | ✅ Required | Scoping — larger docs need more effort |
| Total pages | ✅ Required | Direct input to effort estimation |
| Paragraph count | ✅ Required | High counts with low word counts = fragmented content |
| Heading count + distribution | ✅ Required | Reveals how the doc maps to D360 articles |
| Average words per paragraph | ✅ Required | Values >80 mean content needs splitting before import |
| Broken link count | ⭐ Bonus | Broken links become 404s in D360 — must fix before migration |
| Image count + format + size | ⭐ Bonus | Images need CDN hosting; large counts drive up effort |
| Table count + complexity | ⭐ Bonus | Complex tables (merged cells, >6 cols) don't render in D360's editor |
| Duplicate sections | ⭐ Bonus | Duplicated content fragments the knowledge base |
| Undefined acronyms | ⭐ Bonus | Readers in the new platform won't have the original context |
| Content age / staleness | ⭐ Bonus | Stale docs should be archived, not migrated |
| Language detection | ⭐ Bonus | Flags multilingual docs needing localisation handling |

---

## AI Analysis Output

The model receives the document text and extracted metrics as context, and returns:

- **Readability level** — Easy / Medium / Complex with explanation
- **Content clarity** — score out of 10 with assessment
- **Structural quality** — score out of 10, well-organized vs. fragmented
- **Tone analysis** — formal/conversational, consistency
- **Content classification** — document type, domain, audience
- **Content debt** — undefined acronyms, outdated references, unresolved placeholders
- **Migration readiness** — status label with specific details
- **Effort breakdown** — per content type with one-line reasoning per category
- **Suggestions** — each one cites a specific section title or acronym from the document

---



---



## Tools & Libraries

### Backend

| Library | Purpose |
|---|---|
| Flask | REST API framework |
| Flask-CORS | Allows the frontend to call the API from a different port |
| python-docx | Parses `.docx` files |
| PyMuPDF (fitz) | Parses `.pdf` files — text, images, tables, metadata |
| Groq SDK | LLaMA 3.3 70B for AI analysis |
| python-dotenv | Loads the Groq API key from `.env` |
| langdetect | Detects document language |
| Pygments | Detects programming languages in code blocks |
| Werkzeug | Secure file upload handling |

### Frontend

| Library | Purpose |
|---|---|
| React 18 | UI framework |
| Vite | Dev server with `/api` proxy to Flask on port 5000 |
| Tailwind CSS | Styling — Document360-inspired design system |
| Fetch API | HTTP calls to the backend (no extra dependencies) |

---

## Evaluation Criteria Coverage

| Criterion | How this submission addresses it |
|---|---|
| Accuracy of document parsing | Separate parsers for DOCX and PDF; headings extracted by paragraph style (DOCX) and font-size heuristics (PDF); tables detected via PyMuPDF's `find_tables()` |
| Relevance of metrics for migration | All 5 required metrics present + 8 bonus metrics directly relevant to Document360 migration (broken links, table complexity, image formats, content age, duplication) |
| Quality of AI-driven insights | Prompt instructs the model to cite specific section titles and acronyms found in the document; generic advice is explicitly prohibited in the system prompt |
| Practical usefulness | Single `/api/report` endpoint returns a grade, score, effort estimate, and prioritised blocker list — the exact output a migration lead needs to scope a project; React dashboard surfaces this without requiring the user to read raw JSON |
| Code quality | Parsers, metrics, analysis, services, and routes are fully separated; each module is independently importable and testable |
| Real-world scenario handling | Tested on a 132-page PDF with 639 images and 16 broken links; empty documents and corrupted files handled with graceful fallbacks throughout |

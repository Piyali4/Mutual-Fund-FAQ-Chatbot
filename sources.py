"""Official public sources only — AMC (SBI MF), AMFI, SEBI.

Every URL here is verified to return HTTP 200 from the public web. The loader
in rag_engine.py also re-checks status before embedding, so any URL that goes
404 in the future will simply be skipped instead of polluting the index with
'Page Not Found' boilerplate.
"""

URLS = [
    # ---------- SBI Mutual Fund — scheme pages ----------
    "https://www.sbimf.com/en-us/equity-schemes/sbi-blue-chip-fund",
    "https://www.sbimf.com/en-us/equity-schemes/sbi-flexicap-fund",
    "https://www.sbimf.com/en-us/equity-schemes/sbi-long-term-equity-fund",
    "https://www.sbimf.com/en-us/equity-schemes/sbi-small-cap-fund",
    "https://www.sbimf.com/mutual-fund/equity-mutual-funds",

    # ---------- SBI MF — investor service / docs ----------
    "https://www.sbimf.com/factsheets",
    "https://www.sbimf.com/faq",
    "https://www.sbimf.com/sip",
    "https://www.sbimf.com/tax-planning-calculator",

    # ---------- AMFI ----------
    "https://www.amfiindia.com/",
    "https://www.amfiindia.com/articles/mutual-fund",

    # ---------- AMFI Investor Education ----------
    "https://www.mutualfundssahihai.com/",

    # ---------- SEBI ----------
    "https://www.sebi.gov.in/",
    "https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doRecognisedFpi=yes&type=mutual_funds",
    "https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=1&ssid=4&smid=0",
    "https://investor.sebi.gov.in/elss.html",
]

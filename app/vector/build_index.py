import pickle
import faiss
from sentence_transformers import SentenceTransformer

DOCS_PICKLE = "app/data/docs.pkl"
INDEX_PATH = "app/data/index.faiss"

# -----------------------------
# Curated high-quality docs
# -----------------------------#
pixelweb_docs = [

    # --------------------
    # About Pixel Web Solutions
    # --------------------
    "About Pixel Web Solutions: Pixel Web Solutions is a team of thinkers, makers, and doers.",
    "About Pixel Web Solutions: The team is passionate about building digital solutions.",
    "About Pixel Web Solutions: Solutions help businesses grow and stand out in a competitive global market.",

    # --------------------
    # Company Overview – Strategic Digital Partner
    # --------------------
    "Company Overview: Pixel Web Solutions is a trusted software development company.",
    "Company Overview: The company is located in Madurai.",
    "Company Overview: Pixel Web Solutions delivers innovative end-to-end digital solutions.",
    "Company Overview: Solutions enable businesses to grow and thrive digitally.",
    "Company Overview: Pixel Web Solutions serves startups, SMBs, and large enterprises.",
    "Company Overview: Solutions combine creativity, modern technology, and strategic thinking.",
    "Company Overview: Development starts by understanding unique business goals.",
    "Company Overview: The company delivers measurable and quantifiable value.",
    "Company Overview: Custom solutions address specific challenges.",
    "Company Overview: Solutions promote growth, innovation, and long-term success.",

    # --------------------
    # Service Expertise and Market Focus
    # --------------------
    "Service Expertise: Pixel Web Solutions offers services across multiple industries.",
    "Service Expertise: The company develops blockchain applications.",
    "Service Expertise: The company builds cryptocurrency exchange platforms.",
    "Service Expertise: The company develops NFT marketplace software.",
    "Service Expertise: The company builds fantasy sports applications.",
    "Service Expertise: Services are future-focused and high-demand.",
    "Service Expertise: The company stays ahead of evolving technology trends.",
    "Service Expertise: Every solution emphasizes quality and scalability.",
    "Service Expertise: User experience is a core priority.",
    "Service Expertise: Solutions align with client business vision.",
    "Service Expertise: The company builds new software solutions.",
    "Service Expertise: The company launches digital applications.",
    "Service Expertise: The company enhances existing systems.",
    "Service Expertise: Solutions establish strong digital foundations.",

    # --------------------
    # Decades of Digital Excellence
    # --------------------
    "Years of Experience: 12+.",
    "Completed Projects: 560+.",
    "Happy Clients: 350+.",
    "Team Members: 120+.",

    # --------------------
    # Vision Beyond Boundaries
    # --------------------
    "Company Vision: To become the most reliable open-source software development company.",
    "Company Vision: To create world-class digital products.",
    "Company Vision: To build a global footprint.",
    "Company Vision: To remain deeply rooted in the local community.",
    "Company Vision: Workplace culture unites innovation, stability, and purpose.",
    "Company Vision: To deliver meaningful experiences for clients and employees.",

    # --------------------
    # Mission to Elevate Brands
    # --------------------
    "Company Mission: To establish a strong and growth-oriented team culture.",
    "Company Mission: To promote collaboration and continuous improvement.",
    "Company Mission: To drive business growth through scalable software solutions.",
    "Company Mission: To deliver solutions from Madurai to the global market.",
    "Company Mission: To offer Tier-1 benefits in a Tier-2 city.",
    "Company Mission: To provide equal professional opportunities.",
    "Company Mission: To enable passion and excellence to coexist.",

    # --------------------
    # Blockchain Solutions and Services
    # --------------------
    "Blockchain Service: Bespoke blockchain development services.",
    "Blockchain Service: Secure smart contract development.",
    "Blockchain Service: Blockchain-based application development.",
    "Blockchain Service: Seamless system integration.",
    "Blockchain Service: Trust and transparency focused solutions.",

    # --------------------
    # Web Development Services
    # --------------------
    "Web Development Service: High-performance website development.",
    "Web Development Service: Responsive website design.",
    "Web Development Service: Custom web application development.",
    "Web Development Service: Scalable and fast web solutions.",
    "Web Development Service: Focus on usability and aesthetics.",

    # --------------------
    # App Development Services
    # --------------------
    "App Development Service: iOS mobile application development.",
    "App Development Service: Android mobile application development.",
    "App Development Service: Cross-platform application development.",
    "App Development Service: Scalable and high-performing apps.",
    "App Development Service: User-friendly mobile experiences.",

    # --------------------
    # IT Technology and Consulting Services
    # --------------------
    "IT Consulting Service: Technology decision support.",
    "IT Consulting Service: System evaluation and optimization.",
    "IT Consulting Service: Digital transformation guidance.",
    "IT Consulting Service: Operational efficiency improvement.",

    # --------------------
    # AI and Machine Learning Solutions
    # --------------------
    "AI Solution: Artificial Intelligence driven automation.",
    "AI Solution: Machine Learning powered insights.",
    "AI Solution: Predictive analytics solutions.",
    "AI Solution: Intelligent automation systems.",
    "AI Solution: Personalization and anomaly detection tools.",

    # --------------------
    # UI and UX Designing Services
    # --------------------
    "UI/UX Service: Intuitive user interface design.",
    "UI/UX Service: Accessible design solutions.",
    "UI/UX Service: User-friendly experiences.",
    "UI/UX Service: Research-driven design processes.",
    "UI/UX Service: Consistency and usability focus.",

    # --------------------
    # Digital Solutions for All Walks of Business
    # --------------------
    "Target Client: Startups.",
    "Target Client: Small and Medium Businesses.",
    "Target Client: Enterprises.",
    "Target Client: Global Brands.",
    "Target Client: Agencies and Consultants.",
    "Target Client: Corporate Teams.",

    # --------------------
    # Delivery and Capability Metrics
    # --------------------
    "Projects Delivered: 560+.",
    "Developers: 120+.",
    "Technologies and Tools: 18+.",
    "Client Fund Raised: 80%.",

    # --------------------
    # Portfolio – Zedxion
    # --------------------
    "Project Zedxion: Cryptocurrency exchange platform.",
    "Project Zedxion: Supports spot, futures, margin, ETF, and IEO trading.",
    "Project Zedxion: Expanded into NFT marketplace and DEX.",
    "Project Zedxion: Provides advanced financial tools.",
    "Project Zedxion: Token-driven ecosystem growth.",

    # --------------------
    # Portfolio – Coinlocally
    # --------------------
    "Project Coinlocally: Centralized cryptocurrency exchange.",
    "Project Coinlocally: Decentralized exchange platform.",
    "Project Coinlocally: NFT marketplace integration.",
    "Project Coinlocally: Supports spot and futures trading.",
    "Project Coinlocally: CYLC token benefits.",

    # --------------------
    # Portfolio – Bankto
    # --------------------
    "Project Bankto: Crypto payment gateway platform.",
    "Project Bankto: Supports OTC trading.",
    "Project Bankto: Crypto ATM integration.",
    "Project Bankto: Crypto-to-fiat withdrawal support.",

    # --------------------
    # Portfolio – Manilla
    # --------------------
    "Project Manilla: P2P-based crypto exchange.",
    "Project Manilla: Fintech and blockchain integration.",
    "Project Manilla: Supports bill payments and transfers.",
    "Project Manilla: Unified payment ecosystem.",

    # --------------------
    # Portfolio – Savita
    # --------------------
    "Project Savita: Global P2P crypto exchange.",
    "Project Savita: Order-book trading model.",
    "Project Savita: Serves thousands of daily traders.",
    "Project Savita: Operates in over 195 countries.",
    "Project Savita: Minimal KYC and low trading fees.",

    # --------------------
    # Hurdles Faced
    # --------------------
    "Challenge: Limited OTC crypto liquidity.",
    "Challenge: Complex security protocol integration.",
    "Challenge: Secure crypto ATM deployment.",
    "Challenge: Legal and regulatory compliance.",

    # --------------------
    # Research Findings and Solutions
    # --------------------
    "Solution: Secure crypto transaction focus.",
    "Solution: KYB verification for merchants.",
    "Solution: Advanced OTC trading modules.",
    "Solution: Crypto ATM cash withdrawal feature.",

    # --------------------
    # Bankto Milestones
    # --------------------
    "Bankto Achievement: Global business approval.",
    "Bankto Achievement: Customer choice awards.",
    "Bankto Achievement: Ransomware protection recognition.",
    "Bankto Achievement: 5,000+ monthly views.",
    "Bankto Achievement: 16,000+ website visits.",
    "Bankto Achievement: $100,000 revenue from $10,000 investment.",

    # --------------------
    # Client Reviews
    # --------------------
    "Client Review: Chiagozie Iwu praised continuous product improvement.",
    "Client Review: Maasakis Taguchi appreciated usability and reliability.",
    "Client Review: Samran Habib praised blockchain expertise.",
    "Client Review: Marco Tosoni praised full-cycle crypto exchange development.",
    "Client Review: Smart Akukoma recommended the team for crypto projects.",

    # --------------------
    # Industries Served
    # --------------------
    "Industry Served: Fintech.",
    "Industry Served: Real Estate.",
    "Industry Served: Healthcare.",
    "Industry Served: Retail and E-commerce.",
    "Industry Served: Gaming.",
    "Industry Served: Education.",

    # --------------------
    # Company Values
    # --------------------
    "Company Value: Authenticity.",
    "Company Value: Innovation.",
    "Company Value: Transparency.",
    "Company Value: Collaboration.",
    "Company Value: Positive Results.",
    "Company Value: Integrity.",
    "Company Value: Client-Centric Approach.",
    "Company Value: Quality Assurance.",
    "Company Value: Continuous Evolution.",

    # --------------------
    # Contact Information
    # --------------------
    "Company Address: No-4, Ram Towers, Melakkal Main Road, Near Seventh Day School, Kochadai, Madurai – 625016.",
    "Contact Email Address: sales@pixelwebsolutions.com.",
    "Contact Phone Number: +91 95002 69409."
]


# -----------------------------
# Save documents
# -----------------------------
with open(DOCS_PICKLE, "wb") as f:
    pickle.dump(pixelweb_docs, f)

# -----------------------------
# Create FAISS index
# -----------------------------
model = SentenceTransformer("app/models/all-MiniLM-L6-v2")

embeddings = model.encode(
    pixelweb_docs,
    convert_to_numpy=True,
    normalize_embeddings=True
)

dim = embeddings.shape[1]
index = faiss.IndexFlatIP(dim)  # cosine similarity
index.add(embeddings)

faiss.write_index(index, INDEX_PATH)

print(f"✅ FAISS index created with {len(pixelweb_docs)} semantic chunks")

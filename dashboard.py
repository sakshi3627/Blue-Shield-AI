import streamlit as st

# Set page layout and title
st.set_page_config(page_title="Abyssal Blue Shield AI", layout="centered")

# Inject HTML and CSS into Streamlit
st.markdown("""
<style>
    /* Dark background override for Streamlit app container */
    .stApp {
        background-color: #010410; /* Extra dark abyss black */
    }

    :root {
        /* Revised Ocean & Deep Teal Palette */
        --abyss-black: #010410;
        --primary-ocean: #00d2ff;
        --deep-ocean: #004785;
        --teal-glow: rgba(0, 210, 255, 0.6);
        --glass-bg: rgba(6, 26, 48, 0.7);
        --glass-border: rgba(0, 210, 255, 0.25);
        --text-subtle: #809bb0;
    }

    /* Full Ocean-Themed Background environment */
    .ocean-abyss {
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 60px 0;
        overflow: hidden; /* Contains bubbles and networks */
        border-radius: 30px;
    }

    /* Ambient Bioluminescent Glow */
    .ocean-abyss::before {
        content: '';
        position: absolute;
        width: 450px;
        height: 450px;
        background: radial-gradient(circle, var(--deep-ocean) 0%, transparent 80%);
        opacity: 0.6;
        filter: blur(100px);
        z-index: 0;
    }

    /* Animated Digital Abyssal Network */
    .ocean-abyss::after {
        content: '';
        position: absolute;
        inset: 0;
        background-image: 
            radial-gradient(var(--teal-glow) 1px, transparent 1px),
            linear-gradient(rgba(0, 210, 255, 0.05) 1px, transparent 1px);
        background-size: 50px 50px, 100px 100px;
        background-position: center;
        opacity: 0.2;
        filter: blur(1px);
        z-index: -1;
        animation: digital-drift 20s linear infinite;
    }

    /* Rising Bubble Graphics */
    .bubble {
        position: absolute;
        background: rgba(0, 210, 255, 0.3);
        border: 1px solid rgba(0, 210, 255, 0.5);
        border-radius: 50%;
        animation: bubble-rise 8s infinite ease-in;
        z-index: -2; /* Behind the drift and glow */
    }

    /* Advanced Shield Container Card with Shimmer */
    .shield-card {
        position: relative;
        z-index: 10;
        width: 360px;
        padding: 50px 35px;
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 28px;
        border: 1px solid var(--glass-border);
        box-shadow: 
            0 25px 60px rgba(0, 0, 0, 0.8),
            inset 0 2px 10px rgba(0, 210, 255, 0.1),
            0 0 15px rgba(0, 210, 255, 0.1);
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        margin: 0 auto;
        overflow: hidden; /* For shimmer */
    }

    /* Continuous Hydro-static Shimmer Effect */
    .shield-card::after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(
            135deg,
            transparent 0%,
            transparent 45%,
            rgba(255, 255, 255, 0.08) 50%,
            transparent 55%,
            transparent 100%
        );
        background-size: 200% 200%;
        animation: shimmer 6s infinite;
        z-index: 11; /* Above title and description */
    }

    /* Advanced Oceanic SVG Grid Overlay (subtle) */
    .svg-grid-overlay {
        position: absolute;
        inset: -20%;
        opacity: 0.08;
        z-index: -1;
        transform: rotate(-10deg);
    }

    /* Outer Energy Ring - Bioluminescent Pulse */
    .shield-wrapper {
        position: relative;
        width: 150px;
        height: 150px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 28px;
        z-index: 5;
    }

    .shield-wrapper::before,
    .shield-wrapper::after {
        content: '';
        position: absolute;
        inset: -12px;
        border-radius: 50%;
        border: 2px solid var(--primary-ocean);
        opacity: 0;
        animation: bioluminescent-pulse 3.5s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
        filter: blur(1px);
    }

    .shield-wrapper::after {
        animation-delay: 1.75s;
    }

    /* Glowing Shield Box - Abyssal Depth */
    .shield-icon {
        position: relative;
        width: 125px;
        height: 125px;
        background: radial-gradient(circle at 50% 30%, rgba(0, 71, 133, 0.5), var(--abyss-black) 80%);
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        box-shadow: 
            0 0 40px var(--teal-glow),
            inset 0 0 20px rgba(0, 210, 255, 0.3),
            0 0 100px rgba(0, 71, 133, 0.4);
        border: 1px solid rgba(0, 210, 255, 0.5);
        overflow: hidden;
    }

    .shield-svg {
        width: 65px;
        height: 65px;
        fill: none;
        stroke: var(--primary-ocean);
        stroke-width: 1.5;
        filter: drop-shadow(0 0 10px var(--primary-ocean));
        z-index: 2;
    }

    /* Sonic Echo Beam Effect (Modified scan) */
    .scanner-line {
        position: absolute;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, transparent, #ffffff, transparent);
        box-shadow: 0 0 20px var(--primary-ocean), 0 0 10px #ffffff;
        top: 0;
        z-index: 3;
        animation: sonic-echo 3s ease-in-out infinite alternate;
        opacity: 0.8;
    }

    /* Advanced AI Status Badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: rgba(0, 210, 255, 0.08);
        border: 1px solid var(--primary-ocean);
        color: var(--primary-ocean);
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 2px;
        padding: 8px 18px;
        border-radius: 25px;
        text-transform: uppercase;
        margin-bottom: 15px;
        box-shadow: 0 0 15px rgba(0, 210, 255, 0.3);
        z-index: 5;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        background-color: var(--primary-ocean);
        border-radius: 50%;
        box-shadow: 0 0 12px var(--primary-ocean), 0 0 6px #ffffff;
        animation: abyssal-blink 1.2s infinite alternate;
    }

    .title {
        color: #ffffff;
        font-size: 1.6rem;
        font-weight: 700;
        margin-bottom: 10px;
        letter-spacing: 1px;
        text-shadow: 0 0 10px rgba(0, 210, 255, 0.7);
        z-index: 5;
    }

    .description {
        color: var(--text-subtle);
        font-size: 0.9rem;
        line-height: 1.6;
        font-weight: 400;
        max-width: 90%;
        z-index: 5;
    }

    /* --- Detailed Animations --- */

    /* Digital network drifting deep underwater */
    @keyframes digital-drift {
        0% { background-position: center; transform: translateY(0); }
        100% { background-position: center 200px; transform: translateY(-50px); }
    }

    /* Rising bubble effect with opacity change */
    @keyframes bubble-rise {
        0% { transform: translateY(100vh) scale(1); opacity: 0; }
        20% { opacity: 1; }
        80% { opacity: 1; }
        100% { transform: translateY(-20vh) scale(1.5); opacity: 0; }
    }

    /* Continuous Hydro-static Shimmer across the card */
    @keyframes shimmer {
        0% { background-position: -200% -200%; }
        100% { background-position: 200% 200%; }
    }

    /* Sonic Echo Beam/Scan animation */
    @keyframes sonic-echo {
        0% { top: 0%; opacity: 0.3; }
        50% { opacity: 1; }
        100% { top: 100%; opacity: 0.3; }
    }

    /* Bioluminescent pulse effect for energy rings */
    @keyframes bioluminescent-pulse {
        0% {
            transform: scale(0.8);
            opacity: 0.9;
            box-shadow: 0 0 10px var(--teal-glow);
        }
        80%, 100% {
            transform: scale(1.4);
            opacity: 0;
            box-shadow: 0 0 30px transparent;
        }
    }

    /* Slower, deep blink for the status indicator */
    @keyframes abyssal-blink {
        0% { opacity: 0.2; transform: scale(0.9); }
        100% { opacity: 1; transform: scale(1.1); }
    }
</style>

<div class="ocean-abyss">
    <!-- Bubble graphics - different sizes/speeds -->
    <div class="bubble" style="width: 15px; height: 15px; left: 10%; animation-delay: 0s; animation-duration: 9s;"></div>
    <div class="bubble" style="width: 8px; height: 8px; left: 25%; animation-delay: 2s; animation-duration: 7s;"></div>
    <div class="bubble" style="width: 20px; height: 20px; left: 40%; animation-delay: 1s; animation-duration: 10s;"></div>
    <div class="bubble" style="width: 12px; height: 12px; left: 60%; animation-delay: 3s; animation-duration: 8s;"></div>
    <div class="bubble" style="width: 18px; height: 18px; left: 85%; animation-delay: 0.5s; animation-duration: 9s;"></div>

    <div class="shield-card">
        <!-- Subtle Oceanic Topographic Grid Overlay SVG -->
        <svg class="svg-grid-overlay" width="100%" height="100%" viewBox="0 0 100 100">
            <defs>
                <pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">
                    <path d="M 10 0 L 0 0 0 10" fill="none" stroke="currentColor" stroke-width="0.5"/>
                </pattern>
            </defs>
            <rect width="100" height="100" fill="url(#grid)" />
            <circle cx="50" cy="50" r="40" stroke="currentColor" stroke-width="0.2" fill="none"/>
            <path d="M 20 20 Q 50 80 80 20" stroke="currentColor" stroke-width="0.2" fill="none"/>
        </svg>

        <div class="shield-wrapper">
            <div class="shield-icon">
                <div class="scanner-line"></div>
                <!-- Shield SVG Icon with slight bioluminescent shift -->
                <svg class="shield-svg" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
                    <path d="M9 12l2 2 4-4" stroke="#ffffff" stroke-width="2.5"></path>
                </svg>
            </div>
        </div>

        <div class="status-badge">
            <span class="status-dot"></span> Abyssal Protocol Active
        </div>

        <h2 class="title">Oceanic Blue Shield AI</h2>
        <p class="description">Neural threat detection and deep-sea system defense protocols operational.</p>
    </div>
</div>
""", unsafe_allow_html=True)
                 
        

        
          
   
  

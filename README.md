# TradeAnalyst Screener

TradeAnalyst Screener is a Telegram Mini App designed to help traders quickly scan Forex and cryptocurrency markets through a clean, mobile-friendly interface. Built primarily with `HTML`, `CSS`, and `JavaScript`, the project focuses on market screening, watchlist management, AI-powered market analysis, and a simple PRO subscription experience using Telegram Stars.

### 📦 Technologies

* `Main`
* `ENV`
* `HTML`


### 🦄 Features

Here's what you can do with TradeAnalyst Screener:

* **📊 Forex Screener:** Scan selected Forex pairs and view their current trend and market strength.
* **₿ Crypto Screener:** Browse cryptocurrency markets and quickly identify bullish or bearish assets.
* **🔎 Market Search:** Search for specific Forex pairs or cryptocurrencies and add interesting assets to your watchlist.
* **⭐ Watchlists:** Add or remove assets from personalized Forex and Crypto watchlists using browser storage.
* **📈 Trend Detection:** View whether an asset is currently classified as bullish or bearish.
* **💪 Strength Indicator:** See market strength represented through visual strength bars and percentage values.
* **🤖 AI Market Analysis:** Enter a trading pair such as `EURUSD` or `SOL` and request an AI-generated market breakdown.
* **⏱️ AI Usage Limits:** Free users receive three AI analyses within a six-hour period, with an automatic usage reset.
* **👑 PRO Membership:** Upgrade to PRO for unlimited AI analysis and additional premium functionality.
* **⭐ Telegram Stars Payment:** Includes a Telegram-based PRO subscription interface using Telegram Stars.
* **👤 Telegram Profile:** Automatically detects the Telegram user's first name when the Mini App is opened inside Telegram.
* **📱 Responsive Interface:** The layout adapts specifically to smaller mobile screens while maintaining a desktop-friendly design.
* **🧭 Bottom Navigation:** Quickly switch between Forex, Crypto, AI Analysis, PRO, and Profile sections.
* **🌙 Dark Trading Interface:** Uses a dark, trading-focused UI with purple, gold, green, and red visual accents.
* **⚡ Loading & Error States:** Displays loading indicators and basic error feedback while market or AI data is being retrieved.

### 🧑‍🍳 The Process

I started by building the core interface and structuring the application into separate screens for Forex, Crypto, AI Analysis, PRO, and the user profile. I wanted the project to feel more like a real trading application than a simple webpage, so I focused heavily on creating a responsive card-based interface and a persistent bottom navigation system.

Next, I worked on the market screener functionality. I created separate Forex and Crypto data flows, connected them to API endpoints, and built reusable rendering logic that could display each asset's symbol, name, trend, strength percentage, and visual indicators. I also added search functionality so users could look for individual assets instead of only viewing the default watchlist.

After that, I implemented user controls around the screener. Users can add assets to their watchlists, remove them, and have those selections persisted through `localStorage`. I also built the AI Analysis section with symbol searching, market-type selection, loading states, generated analysis results, confidence percentages, and a usage counter.

One of the more interesting parts was implementing the free-versus-PRO system. I created a six-hour AI usage window for free users and added logic that tracks their remaining analyses. I then built the PRO screen, profile status, unlimited-use state, and Telegram confirmation/payment flow so the application could behave more like a monetized Mini App.

Finally, I spent time refining the UI and fixing responsive issues, particularly on smaller screens. I adjusted the table grids, asset cards, flags, strength indicators, AI controls, buttons, and navigation so the interface would remain usable inside a Telegram Mini App. Testing these different states helped me catch layout problems and improve how the different screens interact with each other.

### 📚 What I Learned

During this project, I've picked up important skills and a better understanding of complex ideas, which improved my logical thinking.

* **🧠 State Management with JavaScript:** I learned how to maintain application state for different market categories, search modes, watchlists, and PRO status while keeping the UI synchronized with those changes.

* **💾 LocalStorage & Persistent User Data:** I learned how browser storage can be used to preserve watchlists and AI usage information between sessions without requiring a database for every piece of client-side state.

* **🤖 API Integration & Asynchronous JavaScript:** I gained more experience working with `fetch()`, asynchronous functions, API responses, loading states, and error handling while connecting the frontend to market and AI endpoints.

**📈 Overall Growth:** This project helped me move beyond building static interfaces and gave me more experience thinking about an application as a complete system — from the UI and API communication to user limits, persistent data, subscriptions, and mobile interaction.

### 💭 How can it be improved?

* **📡 Real-Time Market Data:** Add WebSocket-based market updates instead of relying entirely on API requests.
* **📊 Advanced Technical Indicators:** Add RSI, MACD, moving averages, ATR, volume, and other technical indicators.
* **📈 Interactive Charts:** Add interactive price charts for individual Forex pairs and cryptocurrencies.
* **🧠 More Advanced AI Analysis:** Expand the AI response to include market structure, support/resistance, momentum, potential setups, and risk considerations.
* **🔐 Backend Authentication:** Move PRO status and usage tracking from `localStorage` to a secure backend so users cannot modify their subscription status locally.
* **💳 Real Telegram Payments:** Connect the PRO purchase flow to a backend payment verification system instead of relying solely on client-side state.
* **🔔 Telegram Notifications:** Allow users to receive alerts when watchlisted assets change trend or reach a specific strength level.
* **🎨 UI Enhancements:** Add animations, skeleton loaders, improved empty states, and more detailed asset cards to make the interface feel even more polished.
* **⚙️ Better Error Handling:** Provide more specific feedback for invalid symbols, unavailable market data, API failures, and network problems.

### 🚦 Running the Project

To run the project in your local environment, follow these steps:

1. Clone the repository:

   `git clone https://github.com/YOUR-USERNAME/TradeAnalyst-Screener.git`

2. Enter the project directory:

   `cd TradeAnalyst-Screener`

3. Install the required dependencies if the backend contains a `package.json`:

   `npm install`

4. Start the local development server:

   `npm start`

5. Open the application locally in your browser or connect the project to your Telegram Mini App configuration.

> **Note:** The exact installation and startup commands may need to be adjusted depending on the backend/server implementation used with the project.

### 🍿 Video / Screenshots

> 🎥 **Demo Video:** 
**https://t.me/miniapplovers/13**

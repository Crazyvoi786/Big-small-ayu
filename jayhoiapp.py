// Automated Live Cricket Prediction System with Telegram Alerts

import axios from "axios";

export default defineComponent({
  async run({ steps, $ }) {
    const TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN";
    const CHAT_ID = "YOUR_TELEGRAM_CHAT_ID";
    const CRICBUZZ_API_KEY = "YOUR_RAPIDAPI_KEY";

    // Step 1: Get Live Match Data from Cricbuzz
    const response = await axios.get("https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live", {
      headers: {
        'X-RapidAPI-Key': CRICBUZZ_API_KEY,
        'X-RapidAPI-Host': 'cricbuzz-cricket.p.rapidapi.com'
      }
    });

    const matches = response.data.matches;
    if (!matches || matches.length === 0) {
      await axios.post(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`, {
        chat_id: CHAT_ID,
        text: "⚠️ No live matches found currently."
      });
      return;
    }

    // Step 2: Select Active Match
    const match = matches.find(m => m.matchInfo && m.matchInfo.status === "Live");
    if (!match) {
      await axios.post(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`, {
        chat_id: CHAT_ID,
        text: "🚫 No currently live match detected."
      });
      return;
    }

    const team1 = match.matchInfo.team1.teamName;
    const team2 = match.matchInfo.team2.teamName;
    const status = match.matchInfo.status;
    const score = match.liveScore?.inningsScoreList?.[0];

    if (!score) {
      await axios.post(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`, {
        chat_id: CHAT_ID,
        text: `⚠️ Live score not available for ${team1} vs ${team2}`
      });
      return;
    }

    const batsman = score.batsmanStrike?.batName || "Unknown";
    const bowler = score.bowler?.bowlName || "Unknown";

    const prompt = `Current Score: ${score.score}/${score.wickets} in ${score.overs} overs\nBatsman: ${batsman}, Bowler: ${bowler}\nGive betting suggestion, risk alert and expected over runs.`;

    const aiRes = await axios.post(
      "https://api.openai.com/v1/chat/completions",
      {
        model: "gpt-3.5-turbo",
        messages: [
          { role: "system", content: "You are an expert betting AI assistant." },
          { role: "user", content: prompt }
        ],
        temperature: 0.5
      },
      {
        headers: {
          Authorization: `Bearer YOUR_OPENAI_API_KEY`,
          "Content-Type": "application/json"
        }
      }
    );

    const prediction = aiRes.data.choices[0].message.content;

    await axios.post(`https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`, {
      chat_id: CHAT_ID,
      text: `🎯 *Live Prediction*\n\n${prediction}`,
      parse_mode: "Markdown"
    });

    return { status: "Prediction sent ✅" };
  }
});

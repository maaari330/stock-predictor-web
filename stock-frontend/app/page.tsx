'use client'
import { useState } from "react";

export default function Home() {
  const [Ticker, setTicker] = useState("")
  const [TickerSymbol, setTickerSymbol] = useState("")
  const [Days, setDays] = useState("")
  const [UpPercent, setUpPercent] = useState(0.0)
  const [DownPercent, setDownPercent] = useState(0.0)
  const [Direction, setDirection] = useState("")
  const [Strength, setStrength] = useState(0.0)

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const main_api_url = `${process.env.NEXT_PUBLIC_HOST}/api/predict/`
    const response = await fetch(main_api_url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ticker: Ticker, symbol: TickerSymbol, days: parseInt(Days) })
    })
    const response_body = await response.json()
    setUpPercent(response_body.UpPercent)
    setDownPercent(response_body.DownPercent)
    setDirection(response_body.Direction)
    setStrength(response_body.Strength)
  }

  return (
    <main>
      <div>
        株価予測実行
      </div>
      <form method="post" onSubmit={handleSubmit} className="forms">
        <label>
          銘柄コード/Ticker:
          <input type="text" required value={Ticker} onChange={e => setTicker(e.target.value)} />
        </label>
        <label>
          ティッカーシンボル/Ticker Symbol:
          <input type="text" required value={TickerSymbol} onChange={e => setTickerSymbol(e.target.value)} />
        </label>
        <label>
          日数:
          <input type="number" min={11} required value={Days}
            onChange={e => {
              const v = e.target.value
              v == "" ? setDays("") : setDays(v)
            }}
          />
        </label>
        <button type="submit">株価予測</button>
      </form>


      <div>
        <p>翌営業日の株価 上昇確率：{UpPercent} 下落確率：{DownPercent}</p>
        <p>判定：{Direction}</p>
        <p>予測の強さ（しきい値との差。モデルの迷いの少なさ）：{Strength}%</p>
      </div>
    </main>
  );
}

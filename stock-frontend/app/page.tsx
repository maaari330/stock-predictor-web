'use client'
import { useState } from "react";
import dynamic from "next/dynamic"

export default function Home() {
  const [Ticker, setTicker] = useState("7203.T")
  const [TickerSymbol, setTickerSymbol] = useState("USDJPY=X")
  const [Days, setDays] = useState("")
  const [UpPercent, setUpPercent] = useState(0.0)
  const [DownPercent, setDownPercent] = useState(0.0)
  const [Direction, setDirection] = useState("")
  const [Strength, setStrength] = useState(0.0)

  const HeavyComponent = dynamic(() => import('../components/StockChart').then((mod) => mod.default), {
    ssr: false,
    loading: () => <p>Loading...</p>,
  });

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
    <main className="page">
      <section className="card">
        <h2 className="pageHeader">
          株価予測実行
        </h2>
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
          <button type="submit" className="btn">株価予測</button>
        </form>

        <div className="result">
          翌営業日の株価 予測結果
          <div className="resultRow">
            <dt>上昇確率：</dt> <dd>{UpPercent}%</dd>
            <dt>下落確率：</dt> <dd>{DownPercent}%</dd>
          </div>
          <div className="resultRow">
            <dt>判定：</dt> <dd>{Direction}</dd>
          </div>
          <div className="resultRow">
            <dt>予測の強さ*：</dt> <dd>{Strength}%</dd>
          </div>
          <span className="note">*しきい値との差（モデルの迷いの少なさ）を表す。</span>
        </div>
      </section>

      <section className="card">
        <h2 className="pageHeader">
          株価情報取得
        </h2>
        <div>
          <HeavyComponent ticker="7203.T"></HeavyComponent>
        </div>
      </section>
    </main>
  );
}

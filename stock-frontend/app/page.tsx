'use client'
import { useState } from "react";
import { BsGraphUpArrow } from "react-icons/bs";
import { BsGraphDownArrow } from "react-icons/bs";

export default function Home() {
  const [Ticker, setTicker] = useState("")
  const [Days, setDays] = useState("")
  const [PredictionLabel, setPredictionLabel] = useState("")
  const [Confidence, setConfidence] = useState(0)

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const main_api_url = `${process.env.NEXT_PUBLIC_HOST}/predict/`
    const res = await fetch(main_api_url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ticker: Ticker, days: parseInt(Days) })
    })
    const resBody = await res.json()
    setPredictionLabel(resBody.PredictionLabel)
    setConfidence(resBody.Confidence)
  }

  return (
    <main className="page">
      <div>
        株価予測アプリ
      </div>
      <form method="post" onSubmit={handleSubmit} className="forms">
        <label>
          銘柄コード/Ticker:
          <input type="text" required value={Ticker} onChange={e => setTicker(e.target.value)} />
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
      {PredictionLabel &&
        <div className="result">
          {PredictionLabel == "UP" ? (
            <p className="res-letter">明日の株価予測：<span className="res-res up">{PredictionLabel}<BsGraphUpArrow /></span></p>
          ) : (
            <p className="res-letter">明日の株価予測：<span className="res-res down">{PredictionLabel}<BsGraphDownArrow /></span></p>
          )}
          <p>予測精度：{Math.round(Confidence * 100)}%</p>
          <progress value={Confidence * 100} max={100} />
        </div>
      }
    </main>
  );
}

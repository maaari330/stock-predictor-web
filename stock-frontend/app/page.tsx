'use client'
import { useState } from "react";

export default function Home() {
  const [Return,setReturn]=useState(0)
  const [Volatility,setVolatility]=useState(0)
  const [Volume_change,setVolume_change]=useState(0)
  const [Roll_5,setRoll_5]=useState(0)
  const [Roll_10,setRoll_10]=useState(0)
  const [MA_Ratio,setMA_Ratio]=useState(0)
  const [PredictionLabel,setPredictionLabel]=useState()
  const [Confidence,setConfidence]=useState(0)


  async function handleSubmit(e: React.FormEvent<HTMLFormElement>){
    e.preventDefault();
    const res=await fetch('http://localhost:8000/predict',{method:'POST',headers: {'Content-Type': 'application/json'},body:JSON.stringify({Return:Return,Volatility:Volatility,Volume_change:Volume_change,Roll_5:Roll_5,Roll_10:Roll_10,MA_Ratio:MA_Ratio})})
    const resBody= await res.json()
    setPredictionLabel(resBody.PredictionLabel)
    setConfidence(resBody.Confidence)
    return (
      {PredictionLabel && 
        <div>
          <p>明日の株価予測：</p>
          <p>予測精度：</p>
        </div>
      }
    );
  }

  return (
    <>
      <div>
        株価予測アプリ
      </div>
      <form method="post" onSubmit={handleSubmit}>
        <label>
          前日からの終値の変化率:
          <input type="number" name="return" value={Return} onChange={e => setReturn(Number(e.target.value))}/>
        </label>
        <label>
          ボラティリティ(価格の揺れ幅):
          <input type="number" name="volatility" value={Volatility} onChange={e => setVolatility(Number(e.target.value))}/>
        </label>
        <label>
          出来高（当日に取引された株の数）:
          <input type="number" name="volume_change" value={Volume_change} onChange={e => setVolume_change(Number(e.target.value))}/>
        </label>
        <label>
          直近5日間の終値平均:
          <input type="number" name="rool_5" value={Roll_5} onChange={e => setRoll_5(Number(e.target.value))}/>
        </label>
        <label>
          直近10日間の終値平均:
          <input type="number" name="rool_10" value={Roll_10} onChange={e => setRoll_10(Number(e.target.value))}/>
        </label>
        <label>
          （直近5日間の終値平均）/（直近10日間の終値平均）:
          <input type="number" name="ma_ratio" value={MA_Ratio} onChange={e => setMA_Ratio(Number(e.target.value))}/>
        </label>
        <button type="submit">株価予測</button>
      </form>
    </>
  );
}
